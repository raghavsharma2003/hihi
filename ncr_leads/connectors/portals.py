"""Society-page connector for real-estate portals (MagicBricks, 99acres,
Housing.com, NoBroker) — robots.txt-aware, best-effort HTML parsing.

These portals change markup often and several disallow bots on project pages;
this connector checks robots.txt per URL and SKIPS anything disallowed rather
than working around it. Expect partial coverage — Google Places + RERA +
manual portal exports fill the gaps.

Run: python -m ncr_leads.connectors.portals
"""
import json
import os
import re
import time

import requests

from ..geography import config as geo_config
from ..robots import USER_AGENT, allowed

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

# Locality search-index pages (listing pages, not login-walled detail pages).
SEARCH_TEMPLATES = [
    "https://www.magicbricks.com/new-projects-{locality_slug}",
    "https://www.nobroker.in/property/sale/{city_slug}/{locality_slug}",
    "https://housing.com/in/buy/projects/searches/{locality_slug}",
]

# Best-effort extraction of society facts from project-page text.
PATTERNS = {
    "flats": re.compile(r"(\d{2,4})\s*(?:units|flats|apartments)", re.I),
    "towers": re.compile(r"(\d{1,3})\s*towers?", re.I),
    "floors": re.compile(r"(?:G\s*\+\s*|)(\d{1,2})\s*(?:floors|storey)", re.I),
    "possession": re.compile(r"possession[^0-9]{0,20}(20[0-2]\d)", re.I),
    "maintenance": re.compile(r"(?:₹|rs\.?)\s*([\d.]+)\s*(?:/|per)\s*sq\.?\s*ft", re.I),
    "backup": re.compile(r"(full|100%|partial|24x7)\s*power\s*back", re.I),
}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fetch_text(session: requests.Session, url: str) -> str:
    if not allowed(url):
        print(f"  robots.txt disallows, skipping: {url}")
        return ""
    try:
        resp = session.get(url, timeout=30, headers={"User-Agent": USER_AGENT})
        if resp.status_code != 200:
            return ""
        return re.sub(r"<[^>]+>", " ", resp.text)
    except requests.RequestException:
        return ""


def extract_society(text: str, name: str, locality: str, corridor: str, url: str) -> dict:
    facts = {}
    for key, pattern in PATTERNS.items():
        m = pattern.search(text)
        if m:
            facts[key] = m.group(1)
    size = "; ".join(f"{k}={v}" for k, v in facts.items()
                     if k in ("flats", "towers", "floors", "possession"))
    return {
        "name": name, "category": "housing_society", "address": "",
        "locality": locality, "pincode": "", "lat": "", "lng": "",
        "phone": "", "website": "", "google_rating": "", "review_count": "",
        "first_review_year": "", "size_proxy": size,
        "owner_or_chain": "", "standalone_building": "",
        "amenity_power_backup": facts.get("backup", ""),
        "maintenance_rate": facts.get("maintenance", ""),
        "outage_keyword_hits": "0", "outage_quotes": "", "solar_visible": "",
        "fm_company": "", "rera_id": "", "source_urls": [url],
        "corridor": corridor, "icp": "society",
    }


def run() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    session = requests.Session()
    rows = []
    for ckey, c in geo_config()["corridors"].items():
        city = c["city_hint"].split("|")[0]
        city_slug = slug(city)
        for locality in c["localities"]:
            for template in SEARCH_TEMPLATES:
                url = template.format(locality_slug=slug(f"{locality} {city}"),
                                      city_slug=city_slug)
                text = fetch_text(session, url)
                if not text:
                    continue
                # Project names on listing pages: capture "<Name> ... units" windows.
                for m in re.finditer(r"([A-Z][A-Za-z0-9&.' ]{4,60}?)\s+(?:by|offers|has)\s", text):
                    name = m.group(1).strip()
                    window = text[m.start():m.start() + 1200]
                    row = extract_society(window, name, locality, ckey, url)
                    if row["size_proxy"]:
                        rows.append(row)
                time.sleep(2)
    path = os.path.join(RAW_DIR, "portals_societies.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{len(rows)} society rows -> {path}")


if __name__ == "__main__":
    run()
