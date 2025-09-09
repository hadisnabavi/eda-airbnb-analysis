from pathlib import Path
import pandas as pd
from src.data_loading import load_csv
from src.cleaning import clean_listings
from src.config import COLS
from src.utils import find_first_existing

def test_cleaning_sample():
    path = Path("data/samples/listings_sample.csv")
    df = load_csv(path)
    dfc = clean_listings(df)
    # price exists and is positive
    price_col = find_first_existing(dfc, COLS["price"])
    assert price_col is not None
    assert (dfc[price_col] > 0).all()
    # lat/lon ranges if present
    lat_col = find_first_existing(dfc, COLS["lat"])
    lon_col = find_first_existing(dfc, COLS["lon"])
    if lat_col and lon_col:
        assert dfc[lat_col].between(-90, 90).all()
        assert dfc[lon_col].between(-180, 180).all()
