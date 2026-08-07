"""Output schema — one row shape shared by both ICP CSVs (per the brief)."""

FIELDS = [
    "name",
    "category",
    "address",
    "locality",
    "pincode",
    "lat",
    "lng",
    "phone",
    "website",
    "google_rating",
    "review_count",
    "first_review_year",
    "size_proxy",
    "owner_or_chain",
    "standalone_building",
    "amenity_power_backup",
    "maintenance_rate",
    "outage_keyword_hits",
    "outage_quotes",
    "solar_visible",
    "fm_company",
    "rera_id",
    "source_urls",
    "corridor",
    "icp",
    "score",
    "tier",
]

# Category name -> brief priority rank (1 = highest).
CATEGORY_RANKS = {
    "hospital": 1, "nursing home": 1, "maternity": 1, "eye centre": 1,
    "eye center": 1, "diagnostic": 1, "pathology": 1, "clinic": 1, "lab": 1,
    "dealer": 2, "dealership": 2, "showroom": 2, "service centre": 2,
    "service center": 2, "workshop": 2,
    "banquet": 3, "marriage garden": 3, "wedding": 3, "party lawn": 3,
    "hotel": 4, "guest house": 4,
    "school": 5, "coaching": 5, "institute": 5, "academy": 5,
    "electronics": 6, "supermarket": 6, "furniture": 6, "restaurant": 6,
    "qsr": 6, "retail": 6, "store": 6, "mart": 6,
}


def category_rank(category: str) -> int:
    """Map a free-text category to a brief priority rank; 6 (lowest) if unknown."""
    c = (category or "").lower()
    best = None
    for key, rank in CATEGORY_RANKS.items():
        if key in c and (best is None or rank < best):
            best = rank
    return best if best is not None else 6


def blank_row() -> dict:
    return {f: "" for f in FIELDS}
