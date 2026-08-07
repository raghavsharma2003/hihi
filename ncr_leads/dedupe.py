"""Dedup on (normalized name + pincode) and on lat/lng within 50 m."""
import math
import re


def _norm_name(name: str) -> str:
    s = (name or "").lower()
    s = re.sub(r"\b(pvt|private|ltd|limited|the|hospital|hospitals)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _dist_m(lat1, lng1, lat2, lng2) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _coords(row):
    try:
        return float(row.get("lat")), float(row.get("lng"))
    except (TypeError, ValueError):
        return None


def _merge(keep: dict, other: dict) -> None:
    """Fill blanks in the kept row from the duplicate; union source URLs."""
    for k, v in other.items():
        if k == "source_urls":
            continue
        if not keep.get(k) and v:
            keep[k] = v
    a = keep.get("source_urls") or []
    b = other.get("source_urls") or []
    if isinstance(a, str):
        a = [a]
    if isinstance(b, str):
        b = [b]
    keep["source_urls"] = list(dict.fromkeys(a + b))


def dedupe(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    by_key: dict[tuple, dict] = {}
    for row in rows:
        key = (_norm_name(row.get("name", "")), str(row.get("pincode", "")).strip())
        if key[0] and key in by_key:
            _merge(by_key[key], row)
            continue
        c = _coords(row)
        dup = None
        if c:
            for kept in out:
                kc = _coords(kept)
                if kc and _dist_m(c[0], c[1], kc[0], kc[1]) <= 50 and \
                        _norm_name(kept.get("name", ""))[:6] == key[0][:6]:
                    dup = kept
                    break
        if dup is not None:
            _merge(dup, row)
            continue
        by_key[key] = row
        out.append(row)
    return out
