"""Corridor matching: locality-name match first, pincode second, bbox third."""
import os
import re

import yaml

_CFG = None


def config() -> dict:
    global _CFG
    if _CFG is None:
        path = os.path.join(os.path.dirname(__file__), "..", "config", "geography.yml")
        with open(path, encoding="utf-8") as f:
            _CFG = yaml.safe_load(f)
    return _CFG


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def is_excluded(text: str) -> bool:
    t = _norm(text)
    cfg = config()
    for ex in cfg.get("global_exclusions", []):
        if _norm(ex) in t:
            return True
    return False


def match_corridor(locality: str = "", address: str = "", pincode: str = "",
                   lat: str = "", lng: str = "", corridor_hint: str = "") -> str:
    """Return corridor key ('' if outside the whitelist)."""
    cfg = config()
    text = _norm(f"{locality} {address}")
    if is_excluded(text):
        return ""

    corridors = cfg["corridors"]

    # Per-corridor exclusions (e.g. Cyber City inside Gurgaon).
    def excluded_in(key):
        for ex in corridors[key].get("exclusions", []):
            if _norm(ex) in text:
                return True
        return False

    # 1. locality-name match, anchored by city hint when sectors are ambiguous
    for key, c in corridors.items():
        if excluded_in(key):
            continue
        hints = [_norm(h) for h in (c.get("city_hint", "")).split("|") if h]
        city_in_text = any(h in text for h in hints)
        if any(_norm(bad) in text for bad in c.get("city_hint_not", [])):
            city_in_text = False
        for loc in c["localities"]:
            loc_n = _norm(loc)
            if loc_n in text:
                # "Sector N" appears in every NCR city — require the city name too
                if loc_n.startswith("sector") and not city_in_text:
                    continue
                return key

    # 2. pincode
    if pincode:
        for key, c in corridors.items():
            if str(pincode).strip() in c.get("pincodes_seed", []):
                return key

    # 3. bbox
    try:
        la, ln = float(lat), float(lng)
        for key, c in corridors.items():
            s, w, n, e = c["bbox"]
            if s <= la <= n and w <= ln <= e and not excluded_in(key):
                return key
    except (TypeError, ValueError):
        pass

    # 4. trust an explicit hint from the collector if city hint corroborates
    aliases = {"gnw": "gn_west", "noida_ext": "gn_west", "gurugram": "gurgaon"}
    corridor_hint = aliases.get(corridor_hint, corridor_hint)
    if corridor_hint in corridors:
        city = _norm(corridors[corridor_hint].get("city_hint", ""))
        if not text or (city and city in text):
            return corridor_hint

    return ""
