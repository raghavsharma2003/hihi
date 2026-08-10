"""Google Places API connector (official API — not page scraping).

Needs GOOGLE_MAPS_API_KEY. Text Search per (corridor locality x category query),
then Place Details for phone/website/reviews. Review text is scanned for the
outage keywords from config/scoring.yml.

Run: GOOGLE_MAPS_API_KEY=... python -m ncr_leads.connectors.google_places
"""
import json
import os
import re
import time

import requests

from ..geography import config as geo_config
from ..scoring import config as score_config

API = "https://places.googleapis.com/v1/places:searchText"
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

CATEGORY_QUERIES = {
    "hospital": ["private hospital", "nursing home", "maternity centre",
                 "eye hospital", "diagnostic lab"],
    "dealership": ["car dealership", "car service centre",
                   "two wheeler showroom", "bike service centre"],
    "banquet": ["banquet hall", "marriage garden"],
    "hotel": ["hotel"],
    "school": ["private school", "coaching centre"],
    "retail": ["electronics showroom", "supermarket", "furniture store",
               "family restaurant"],
    "housing_society": ["apartment society", "residential society"],
}

FIELD_MASK = ",".join([
    "places.displayName", "places.formattedAddress", "places.location",
    "places.rating", "places.userRatingCount", "places.websiteUri",
    "places.nationalPhoneNumber", "places.reviews", "places.types", "places.id",
])


def search(session: requests.Session, key: str, query: str, bbox) -> list[dict]:
    s, w, n, e = bbox
    body = {
        "textQuery": query,
        "locationRestriction": {"rectangle": {
            "low": {"latitude": s, "longitude": w},
            "high": {"latitude": n, "longitude": e},
        }},
        "pageSize": 20,
    }
    places, token = [], None
    for _ in range(3):  # up to 60 results per query
        if token:
            body["pageToken"] = token
        resp = session.post(API, json=body, timeout=30, headers={
            "X-Goog-Api-Key": key, "X-Goog-FieldMask": FIELD_MASK + ",nextPageToken",
        })
        resp.raise_for_status()
        data = resp.json()
        places += data.get("places", [])
        token = data.get("nextPageToken")
        if not token:
            break
        time.sleep(2)
    return places


def to_row(place: dict, category: str, corridor: str) -> dict:
    kws = score_config()["outage_keywords"]
    reviews = place.get("reviews", [])
    hits, quotes, first_year = 0, [], ""
    for rv in reviews:
        text = (rv.get("text", {}) or {}).get("text", "") or ""
        low = text.lower()
        matched = [k for k in kws if k in low]
        if matched:
            hits += len(matched)
            if len(quotes) < 3:
                quotes.append(re.sub(r"\s+", " ", text)[:160])
        year = (rv.get("publishTime") or "")[:4]
        if year and (not first_year or year < first_year):
            first_year = year
    loc = place.get("location", {})
    address = place.get("formattedAddress", "")
    pin = re.search(r"\b(1[23]\d{4}|20\d{4})\b", address)
    return {
        "name": (place.get("displayName", {}) or {}).get("text", ""),
        "category": category,
        "address": address,
        "locality": "",
        "pincode": pin.group(1) if pin else "",
        "lat": loc.get("latitude", ""),
        "lng": loc.get("longitude", ""),
        "phone": place.get("nationalPhoneNumber", ""),
        "website": place.get("websiteUri", ""),
        "google_rating": place.get("rating", ""),
        "review_count": place.get("userRatingCount", ""),
        "first_review_year": first_year,
        "size_proxy": "",
        "owner_or_chain": "",
        "standalone_building": "",
        "amenity_power_backup": "",
        "maintenance_rate": "",
        "outage_keyword_hits": str(hits),
        "outage_quotes": " | ".join(quotes),
        "solar_visible": "",
        "fm_company": "",
        "rera_id": "",
        "source_urls": [f"https://www.google.com/maps/place/?q=place_id:{place.get('id', '')}"],
        "corridor": corridor,
        "icp": "society" if category == "housing_society" else "commercial",
    }


def run() -> None:
    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key:
        raise SystemExit("Set GOOGLE_MAPS_API_KEY (Places API [New] enabled).")
    os.makedirs(RAW_DIR, exist_ok=True)
    session = requests.Session()
    corridors = geo_config()["corridors"]
    for ckey, c in corridors.items():
        rows = []
        for cat, queries in CATEGORY_QUERIES.items():
            for q in queries:
                for loc in c["localities"][::2]:  # every other locality keeps quota sane
                    full_q = f"{q} in {loc} {c['city_hint'].split('|')[0]}"
                    try:
                        for place in search(session, key, full_q, c["bbox"]):
                            rows.append(to_row(place, cat, ckey))
                    except requests.RequestException as exc:
                        print(f"  ! {full_q}: {exc}")
                    time.sleep(0.2)
        path = os.path.join(RAW_DIR, f"places_{ckey}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"{ckey}: {len(rows)} rows -> {path}")


if __name__ == "__main__":
    run()
