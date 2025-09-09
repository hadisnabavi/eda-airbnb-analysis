import re
import pandas as pd

def find_first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    existing_cols = [c for c in candidates if c in df.columns]
    return existing_cols[0] if existing_cols else None

def clean_price(series: pd.Series) -> pd.Series:
    # Remove currency symbols and commas, convert to float
    return (
        series.astype(str)
        .str.replace(r"[^\d\.\-]", "", regex=True)
        .replace({"": None})
        .astype(float)
    )

def iqr_filter(series: pd.Series, k: float = 1.5) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return (series >= lower) & (series <= upper)
