"""OpenStreetMap Overpass connector — free seed layer, no key, ODbL licence.

Pulls POIs per corridor bbox: hospitals/clinics/labs, car/bike shops, banquet
halls, hotels, schools, supermarkets/electronics/furniture, and apartment
complexes. Throttled to be polite (Overpass fair-use: ~2 concurrent max; we
run sequentially with sleeps).

Run: python -m ncr_leads.connectors.overpass
"""
import json
import os
import time

import requests

from ..geography import config as geo_config
from ..robots import USER_AGENT

ENDPOINT = "https://overpass-api.de/api/interpreter"
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

QUERIES = {
    "hospital": '["amenity"~"hospital|clinic|doctors"]',
    "diagnostic lab": '["healthcare"~"laboratory|diagnostic"]',
    "dealership": '["shop"~"car|motorcycle|car_repair"]',
    "banquet hall": '["amenity"="events_venue"]',
    "hotel": '["tourism"="hotel"]',
    "school": '["amenity"~"school|college"]["operator:type"!="government"]',
    "supermarket": '["shop"~"supermarket|electronics|furniture"]',
    "housing_society": '["building"="apartments"]["name"]',
}


def fetch(session: requests.Session, selector: str, bbox) -> list[dict]:
    s, w, n, e = bbox
    q = f"""[out:json][timeout:90];
(nwr{selector}({s},{w},{n},{e}););
out center tags;"""
    resp = session.post(ENDPOINT, data={"data": q}, timeout=120,
                        headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp.json().get("elements", [])


def to_row(el: dict, category: str, corridor: str) -> dict:
    tags = el.get("tags", {})
    lat = el.get("lat") or (el.get("center") or {}).get("lat", "")
    lng = el.get("lon") or (el.get("center") or {}).get("lon", "")
    addr = ", ".join(filter(None, [
        tags.get("addr:housenumber"), tags.get("addr:street"),
        tags.get("addr:suburb"), tags.get("addr:city"),
    ]))
    return {
        "name": tags.get("name", ""),
        "category": category,
        "address": addr,
        "locality": tags.get("addr:suburb", ""),
        "pincode": tags.get("addr:postcode", ""),
        "lat": lat, "lng": lng,
        "phone": tags.get("phone", tags.get("contact:phone", "")),
        "website": tags.get("website", tags.get("contact:website", "")),
        "google_rating": "", "review_count": "", "first_review_year": "",
        "size_proxy": (f"beds={tags['beds']}" if tags.get("beds") else
                       f"floors={tags['building:levels']}" if tags.get("building:levels") else ""),
        "owner_or_chain": "national_chain" if tags.get("brand") in
                          ("Croma", "Reliance Digital", "DMart") else "",
        "standalone_building": "", "amenity_power_backup": "", "maintenance_rate": "",
        "outage_keyword_hits": "0", "outage_quotes": "", "solar_visible": "",
        "fm_company": "", "rera_id": "",
        "source_urls": [f"https://www.openstreetmap.org/{el.get('type')}/{el.get('id')}"],
        "corridor": corridor,
        "icp": "society" if category == "housing_society" else "commercial",
    }


def run() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    session = requests.Session()
    for ckey, c in geo_config()["corridors"].items():
        rows = []
        for category, selector in QUERIES.items():
            try:
                for el in fetch(session, selector, c["bbox"]):
                    if (el.get("tags") or {}).get("name"):
                        rows.append(to_row(el, category, ckey))
            except requests.RequestException as exc:
                print(f"  ! {ckey}/{category}: {exc}")
            time.sleep(3)  # fair-use throttle
        path = os.path.join(RAW_DIR, f"osm_{ckey}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"{ckey}: {len(rows)} rows -> {path}")


if __name__ == "__main__":
    run()
