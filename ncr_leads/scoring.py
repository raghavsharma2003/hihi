"""ICP scoring per the brief. Commercial and society scores both cap at 100."""
import os
import re

import yaml

from .schema import category_rank

_CFG = None


def config() -> dict:
    global _CFG
    if _CFG is None:
        path = os.path.join(os.path.dirname(__file__), "..", "config", "scoring.yml")
        with open(path, encoding="utf-8") as f:
            _CFG = yaml.safe_load(f)
    return _CFG


def _int(s, default=0):
    try:
        return int(float(str(s).strip()))
    except (TypeError, ValueError):
        return default


def _float(s, default=None):
    try:
        return float(str(s).replace("₹", "").replace("rs", "").replace("Rs", "").strip())
    except (TypeError, ValueError):
        return default


def count_outage_hits(row: dict) -> int:
    """Prefer the collector's counted hits; otherwise count keywords in quotes."""
    n = _int(row.get("outage_keyword_hits"), -1)
    if n >= 0:
        return n
    text = (row.get("outage_quotes") or "").lower()
    kws = config()["outage_keywords"]
    return sum(len(re.findall(re.escape(k), text)) for k in kws)


# ---------------------------------------------------------------- ICP-1

_SIZE_NUM = re.compile(r"(\d[\d,]*)\s*(bed|room|sq\s*ft|sqft|seat)", re.I)

def _commercial_size_in_band(row: dict) -> bool:
    """15-100 beds / 20-80 rooms / >=3000 sqft; dealerships & banquets pass on
    category alone (brand franchise page or venue listing is the size proxy)."""
    rank = category_rank(row.get("category", ""))
    proxy = (row.get("size_proxy") or "").lower()
    if rank in (2, 3):
        return True  # dealership/banquet category itself is the size proxy
    m = _SIZE_NUM.search(proxy)
    if not m:
        return False
    n = _int(m.group(1).replace(",", ""))
    unit = m.group(2).lower()
    if "bed" in unit:
        return 15 <= n <= 100
    if "room" in unit:
        return 20 <= n <= 80
    if "sq" in unit:
        return n >= 3000
    return False


def score_commercial(row: dict) -> tuple[int, str]:
    w = config()["commercial"]
    score = 0
    if row.get("corridor"):
        score += w["corridor_pincode"]
    rank = category_rank(row.get("category", ""))
    score += w["category_priority"][rank]
    if _commercial_size_in_band(row):
        score += w["size_in_band"]
    if count_outage_hits(row) >= 3:
        score += w["outage_keywords_min3"]
    if (row.get("owner_or_chain") or "").lower() in ("owner", "owner_operated", "franchise"):
        score += w["owner_operated"]
    tier = _tier(score, w["tiers"])
    if (row.get("owner_or_chain") or "").lower() == "national_chain":
        tier = "C"  # brief: national chain procurement disqualifies
    return score, tier


# ---------------------------------------------------------------- ICP-2

_FLATS = re.compile(r"flats?\s*=?\s*(\d[\d,]*)|(\d[\d,]*)\s*(?:flats|units|apartments)", re.I)
_POSSESSION = re.compile(r"possession\s*=?\s*(\d{4})|(?:since|built|completed)\s*(\d{4})", re.I)

def _society_flats(row: dict) -> int:
    m = _FLATS.search(row.get("size_proxy") or "")
    if not m:
        return 0
    return _int((m.group(1) or m.group(2)).replace(",", ""))


def _society_possession(row: dict) -> int:
    m = _POSSESSION.search(row.get("size_proxy") or "")
    return _int(m.group(1) or m.group(2)) if m else 0


def score_society(row: dict) -> tuple[int, str]:
    w = config()["society"]
    score = 0
    flats = _society_flats(row)
    if flats >= 200:
        score += w["flats_200_plus"]
    possession = _society_possession(row)
    if 2008 <= possession <= 2019:
        score += w["possession_2008_2019"]
    if row.get("corridor"):
        score += w["corridor"]
    backup = (row.get("amenity_power_backup") or "").lower()
    if "full" in backup or "100" in backup:
        score += w["full_power_backup"]
    if count_outage_hits(row) >= 3:
        score += w["dg_complaint_keywords_min3"]
    rate = _float(re.sub(r"[^\d.]", "", row.get("maintenance_rate") or "") or None)
    if rate is not None and rate >= 2.5:
        score += w["maintenance_2_5_plus"]
    tier = _tier(score, w["tiers"])
    if 150 <= flats < 200 and tier == "A":
        tier = "B"  # brief: 150-199 flats caps at Tier B
    if possession >= 2021 and tier == "A":
        tier = "C"  # brief: >=2021 possession = weaker urgency
    return score, tier


def _tier(score: int, tiers: dict) -> str:
    if score >= tiers["A"]:
        return "A"
    if score >= tiers["B"]:
        return "B"
    return "C"
