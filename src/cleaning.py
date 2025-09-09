import pandas as pd
from .config import COLS
from .utils import clean_price, find_first_existing, iqr_filter

def clean_listings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Price
    price_col = find_first_existing(df, COLS["price"])
    if price_col:
        df[price_col] = clean_price(df[price_col])
        # Drop non-positive or missing
        df = df[df[price_col].notna() & (df[price_col] > 0)]

        # Outlier filter
        mask = iqr_filter(df[price_col])
        df = df[mask]

    # Lat/Lon sanity
    lat_col = find_first_existing(df, COLS["lat"])
    lon_col = find_first_existing(df, COLS["lon"])
    if lat_col and lon_col:
        df = df[df[lat_col].between(-90, 90) & df[lon_col].between(-180, 180)]

    # Dates
    last_review_col = find_first_existing(df, COLS["last_review"])
    if last_review_col:
        df[last_review_col] = pd.to_datetime(df[last_review_col], errors="coerce")

    # Numeric conversions (optional columns)
    num_reviews_col = find_first_existing(df, COLS["num_reviews"])
    if num_reviews_col:
        df[num_reviews_col] = pd.to_numeric(df[num_reviews_col], errors="coerce")

    availability_col = find_first_existing(df, COLS["availability"])
    if availability_col:
        df[availability_col] = pd.to_numeric(df[availability_col], errors="coerce")

    return df.reset_index(drop=True)
