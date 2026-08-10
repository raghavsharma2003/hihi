# Runbook

## End-to-end (from a machine with open internet)

```bash
pip install -r requirements.txt

# Seed layer — free, no key. ~10 min with fair-use throttling.
python -m ncr_leads.connectors.overpass

# Primary layer — Google Places API (New). Text Search + Details.
# Budget: ~1,500–3,000 Text Search calls for the full corridor x category grid.
export GOOGLE_MAPS_API_KEY=...
python -m ncr_leads.connectors.google_places

# Societies — portals (robots-aware; skips disallowed paths) + RERA registries.
python -m ncr_leads.connectors.portals
python -m ncr_leads.connectors.rera

# Merge -> corridor filter -> score -> dedup -> ranked CSVs + quality report.
python -m ncr_leads.pipeline
```

## Volume targets (per the brief)

- 300–500 raw commercial → `commercial_top40.csv`
- 150–250 societies → `society_top30.csv`
- The Places grid alone typically clears both raw targets; Overpass adds
  standalone-building lat/lng anchors and dedup keys.

## Adding review-text outage signals

Places Details returns up to 5 reviews per place — enough for the keyword
counter but thin. To deepen:

- Re-run `google_places.py` monthly; reviews rotate, hits accumulate if you
  merge (the pipeline's dedup merges blanks and unions `source_urls`).
- Justdial review pages are robots-gated; the connector skips what robots.txt
  disallows. Do not bypass.

## Compliance notes

- `ncr_leads/robots.py` gates every portal fetch; disallowed → skipped, never
  spoofed around. Google data comes via the paid Places API, not SERP scraping.
- Phone numbers collected are business listings (public), not personal data.
- OSM data is ODbL — keep the `openstreetmap.org` source URLs in the output.

## Field-visit handoff

The CSVs deliberately leave blank: DG kVA, diesel spend, sanctioned load,
decision-maker name, retrofit status, `solar_visible` (optional satellite CV
step). Sort by tier then score; knock Tier A first.

## Sandbox note (this repo's seed data)

`data/raw/*.jsonl` in this repo was collected by autonomous web-research
agents (search-engine snippets + fetchable public pages) because the CI
sandbox's egress policy blocks direct connections to the data sources. Every
row carries `source_urls`; unknown fields are blank, never guessed. Re-running
the connectors above from an open network will supersede and enrich this seed.
