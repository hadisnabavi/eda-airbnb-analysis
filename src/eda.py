import argparse
from pathlib import Path
import pandas as pd

from .config import COLS, REPORTS_FIG_DIR
from .data_loading import load_csv
from .cleaning import clean_listings
from .viz import save_hist, save_boxplot_by_cat, save_corr_heatmap, save_time_trend, save_map
from .utils import find_first_existing

def main(input_path: str, outdir: str | None = None):
    outdir = Path(outdir) if outdir else REPORTS_FIG_DIR
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_csv(input_path)
    df = clean_listings(df)

    price_col = find_first_existing(df, COLS["price"])
    room_col = find_first_existing(df, COLS["room_type"])
    neigh_col = find_first_existing(df, COLS["neighbourhood"])
    date_col = find_first_existing(df, COLS["last_review"])

    # Univariate
    if price_col:
        save_hist(df, price_col, outdir, "Price Distribution")

    # Bivariate
    if price_col and room_col:
        save_boxplot_by_cat(df, price_col, room_col, outdir, "Price by Room Type")
    if price_col and neigh_col:
        # Use top 15 neighborhoods by count to keep it readable
        top_neigh = df[neigh_col].value_counts().head(15).index
        save_boxplot_by_cat(
            df[df[neigh_col].isin(top_neigh)],
            price_col,
            neigh_col,
            outdir,
            "Price by Top Neighborhoods",
        )

    # Correlations
    save_corr_heatmap(df, outdir, "Numeric Feature Correlations")

    # Time trend (mean price by month if date available)
    if date_col and price_col:
        save_time_trend(df, date_col, price_col, outdir, "Monthly Average Price")

    # Map
    save_map(df, outdir, price_col)

    print(f"Saved figures to: {outdir}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to the listings CSV")
    ap.add_argument("--output", default=None, help="Output directory for figures")
    args = ap.parse_args()
    main(args.input, args.output)
