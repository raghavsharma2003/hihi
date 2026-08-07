"""UP-RERA & Haryana-RERA public project search.

Both authorities expose public project registries (no login). Endpoints move
around; the JSON endpoints below are the ones in use as of mid-2026 — if they
404, check the portal's network tab and update ENDPOINTS.

Purpose per the brief: RERA status "completed" == handed over (AOA-run signal),
plus the rera_id column for the output schema.

Run: python -m ncr_leads.connectors.rera
"""
import json
import os
import time

import requests

from ..robots import USER_AGENT, allowed

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

ENDPOINTS = {
    # districts we care about -> search URL (public project list pages)
    "up": {
        "url": "https://www.up-rera.in/projects",
        "districts": ["Gautam Buddha Nagar", "Ghaziabad"],
    },
    "haryana": {
        "url": "https://haryanarera.gov.in/admincontrol/public_search_project",
        "districts": ["Gurugram", "Faridabad"],
    },
}


def run() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    session = requests.Session()
    rows = []
    for authority, cfg in ENDPOINTS.items():
        if not allowed(cfg["url"]):
            print(f"  robots.txt disallows {cfg['url']}, skipping")
            continue
        for district in cfg["districts"]:
            try:
                resp = session.get(cfg["url"], params={"district": district},
                                   timeout=45, headers={"User-Agent": USER_AGENT})
                if resp.status_code != 200:
                    print(f"  ! {authority}/{district}: HTTP {resp.status_code} "
                          f"(endpoint moved? update ENDPOINTS)")
                    continue
                # Both portals return HTML by default; JSON when the public API
                # endpoint is hit. Handle JSON; HTML needs the per-portal parser
                # a maintainer should update alongside ENDPOINTS.
                try:
                    data = resp.json()
                except ValueError:
                    print(f"  {authority}/{district}: HTML response — parser "
                          f"update needed, skipping")
                    continue
                for p in data if isinstance(data, list) else data.get("projects", []):
                    rows.append({
                        "name": p.get("projectName") or p.get("project_name", ""),
                        "category": "housing_society",
                        "address": p.get("projectAddress") or p.get("address", ""),
                        "locality": p.get("tehsil", ""), "pincode": p.get("pincode", ""),
                        "lat": "", "lng": "", "phone": "", "website": "",
                        "google_rating": "", "review_count": "", "first_review_year": "",
                        "size_proxy": (f"possession={str(p.get('completionDate', ''))[:4]}"
                                       if p.get("completionDate") else ""),
                        "owner_or_chain": "", "standalone_building": "",
                        "amenity_power_backup": "", "maintenance_rate": "",
                        "outage_keyword_hits": "0", "outage_quotes": "",
                        "solar_visible": "", "fm_company": "",
                        "rera_id": p.get("reraRegistrationNo") or p.get("rera_no", ""),
                        "source_urls": [cfg["url"]],
                        "corridor": "", "icp": "society",
                        "rera_status": p.get("status", ""),
                    })
            except requests.RequestException as exc:
                print(f"  ! {authority}/{district}: {exc}")
            time.sleep(2)
    path = os.path.join(RAW_DIR, "rera_projects.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{len(rows)} RERA rows -> {path}")


if __name__ == "__main__":
    run()
