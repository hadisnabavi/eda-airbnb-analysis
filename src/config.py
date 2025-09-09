from pathlib import Path

# Default paths (can be overridden by CLI args or env vars)
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_FIG_DIR = Path("reports") / "figures"

# Columns expected (flexible; handled gracefully if missing)
COLS = {
    "price": ["price"],
    "lat": ["latitude", "lat"],
    "lon": ["longitude", "lng", "lon"],
    "room_type": ["room_type"],
    "neighbourhood": ["neighbourhood", "neighbourhood_cleansed", "neighborhood"],
    "last_review": ["last_review", "last_scraped"],
    "num_reviews": ["number_of_reviews", "reviews"],
    "availability": ["availability_365"],
}
