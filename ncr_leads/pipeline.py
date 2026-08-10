"""Merge data/raw/*.jsonl -> corridor-filter -> score -> dedup -> ranked CSVs.

Run: python -m ncr_leads.pipeline
"""
import csv
import glob
import json
import os

from .dedupe import dedupe
from .geography import match_corridor
from .schema import FIELDS, blank_row
from .scoring import score_commercial, score_society

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "output")


def load_raw() -> list[dict]:
    rows = []
    for path in sorted(glob.glob(os.path.join(RAW_DIR, "*.jsonl"))):
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip().rstrip(",")
                if not line or line in ("[", "]"):
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    print(f"  ! bad JSON skipped: {os.path.basename(path)}:{i + 1}")
                    continue
                if isinstance(obj, dict):
                    obj["_src_file"] = os.path.basename(path)
                    rows.append(obj)
    return rows


def normalize(raw: dict) -> dict:
    row = blank_row()
    for k in FIELDS:
        v = raw.get(k, "")
        row[k] = v if v is not None else ""
    if isinstance(row["source_urls"], str) and row["source_urls"]:
        row["source_urls"] = [u.strip() for u in row["source_urls"].split("|") if u.strip()]
    if not isinstance(row["source_urls"], list):
        row["source_urls"] = []
    return row


def run() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    raw = load_raw()
    print(f"raw rows: {len(raw)}")

    dropped_no_source, dropped_no_corridor = 0, 0
    commercial, society = [], []
    for r in raw:
        row = normalize(r)
        if not row["name"] or not row["source_urls"]:
            dropped_no_source += 1
            continue
        corridor = match_corridor(row["locality"], row["address"], row["pincode"],
                                  row["lat"], row["lng"], row.get("corridor", ""))
        row["corridor"] = corridor
        if not corridor:
            dropped_no_corridor += 1
            continue
        icp = (row.get("icp") or "").lower()
        if "society" in icp or "housing" in (row.get("category") or "").lower():
            row["icp"] = "society"
            society.append(row)
        else:
            row["icp"] = "commercial"
            commercial.append(row)

    commercial = dedupe(commercial)
    society = dedupe(society)

    for row in commercial:
        row["score"], row["tier"] = score_commercial(row)
    for row in society:
        row["score"], row["tier"] = score_society(row)

    key = lambda r: ({"A": 0, "B": 1, "C": 2}[r["tier"]], -int(r["score"]), r["name"])
    commercial.sort(key=key)
    society.sort(key=key)

    _write("commercial_leads.csv", commercial)
    _write("commercial_top40.csv", commercial[:40])
    _write("society_leads.csv", society)
    _write("society_top30.csv", society[:30])
    _quality_report(commercial, society, dropped_no_source, dropped_no_corridor)

    print(f"commercial: {len(commercial)} (dropped: {dropped_no_source} no-source, "
          f"{dropped_no_corridor} out-of-corridor across both ICPs)")
    print(f"society:    {len(society)}")
    print(f"outputs in {os.path.abspath(OUT_DIR)}")


def _write(fname: str, rows: list[dict]) -> None:
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["source_urls"] = " | ".join(out.get("source_urls") or [])
            writer.writerow(out)


def _coverage(rows: list[dict], field: str) -> str:
    n = sum(1 for r in rows if str(r.get(field, "")).strip())
    return f"{n}/{len(rows)} ({(100 * n // len(rows)) if rows else 0}%)"


def _quality_report(commercial, society, no_source, no_corridor) -> None:
    lines = ["# Data quality report", ""]
    lines.append(f"- rows dropped (missing name/source): {no_source}")
    lines.append(f"- rows dropped (outside corridor whitelist): {no_corridor}")
    for label, rows in (("Commercial", commercial), ("Society", society)):
        lines += ["", f"## {label} ({len(rows)} rows)", ""]
        tiers = {t: sum(1 for r in rows if r["tier"] == t) for t in "ABC"}
        lines.append(f"- tiers: A={tiers['A']} B={tiers['B']} C={tiers['C']}")
        for f in ("phone", "email", "pincode", "google_rating", "size_proxy",
                  "outage_quotes", "owner_or_chain", "amenity_power_backup", "rera_id"):
            lines.append(f"- {f} coverage: {_coverage(rows, f)}")
    lines += ["", "Fields left for field visits (per brief): DG kVA, diesel spend, "
              "sanctioned load, decision-maker, retrofit status.", ""]
    with open(os.path.join(OUT_DIR, "quality_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    run()
