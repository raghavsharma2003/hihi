# NCR Battery-Lead Scraper

Builds two ranked lead lists for a battery-as-a-service business in NCR, per the ICP scraping brief:

- **ICP-1 Commercial sites** — owner-operated, diesel-burning businesses (~10–50 kW) in high-outage corridors.
- **ICP-2 Housing societies** — handed-over, AOA-run, 200+ flat high-rises (possession ~2008–2019) with resident-billed diesel backup.

Public web data only. Every connector goes through a robots.txt gate (`ncr_leads/robots.py`) and skips any source whose robots.txt disallows the path. No login-walled scraping.

## Layout

```
config/geography.yml        corridor whitelist: localities + seed pincodes + bounding boxes
config/scoring.yml          score weights per the brief (0–100, tiers A/B/C)
ncr_leads/
  schema.py                 output CSV schema (one row shape for both ICPs)
  geography.py              corridor matching (locality / pincode / bbox)
  scoring.py                ICP-1 and ICP-2 scoring + tiering
  dedupe.py                 (name+pincode) and 50 m lat/lng dedup
  pipeline.py               merge raw JSONL → score → dedup → ranked CSVs
  robots.py                 robots.txt compliance gate (cached)
  connectors/
    google_places.py        Google Places API (Text Search + Details + reviews) — needs GOOGLE_MAPS_API_KEY
    overpass.py             OpenStreetMap Overpass — free, no key, ODbL
    justdial.py             Justdial category pages — robots-aware, best-effort
    portals.py              MagicBricks / 99acres / Housing.com / NoBroker society pages — robots-aware
    rera.py                 UP-RERA & Haryana-RERA public project search
data/raw/                   raw JSONL from connectors / collection agents
data/output/                final CSVs (full + Tier-A shortlists)
docs/RUNBOOK.md             how to run end-to-end, volume targets, field-visit handoff
```

## Quick start

```bash
pip install -r requirements.txt

# 1. Pull raw candidates (each writes data/raw/*.jsonl)
python -m ncr_leads.connectors.overpass                 # free seed layer
GOOGLE_MAPS_API_KEY=... python -m ncr_leads.connectors.google_places
python -m ncr_leads.connectors.portals                  # societies
python -m ncr_leads.connectors.rera

# 2. Merge, score, dedup, rank
python -m ncr_leads.pipeline
```

Outputs land in `data/output/`:

- `commercial_leads.csv` (all scored) + `commercial_top40.csv`
- `society_leads.csv` (all scored) + `society_top30.csv`
- `quality_report.md` — field-coverage stats and rows needing manual review

## What the scraper deliberately does NOT collect

Actual DG kVA & diesel spend, sanctioned load, decision-maker names, retrofit status — these are field-visit fields (see the brief). The scraper's only job is deciding **which doors are worth knocking**.

## Data provenance rules

- Every row carries `source_urls`. Rows without a source are dropped by the pipeline.
- Unknown fields are left blank, never guessed.
- Seed pincodes in `config/geography.yml` are approximate and marked for verification; corridor matching falls back to locality-name matching.
