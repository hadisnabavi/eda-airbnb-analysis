from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

from .config import COLS

sns.set(style="whitegrid")

def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def save_hist(df: pd.DataFrame, col: str, outdir: Path, title: str):
    _ensure_dir(outdir)
    plt.figure(figsize=(8, 5))
    sns.histplot(df[col], bins=40, kde=True)
    plt.title(title)
    plt.xlabel(col)
    plt.tight_layout()
    out = outdir / f"hist_{col}.png"
    plt.savefig(out, dpi=150)
    plt.close()

def save_boxplot_by_cat(df: pd.DataFrame, num_col: str, cat_col: str, outdir: Path, title: str):
    _ensure_dir(outdir)
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x=cat_col, y=num_col)
    plt.title(title)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    out = outdir / f"box_{num_col}_by_{cat_col}.png"
    plt.savefig(out, dpi=150)
    plt.close()

def save_corr_heatmap(df: pd.DataFrame, outdir: Path, title: str):
    _ensure_dir(outdir)
    num = df.select_dtypes(include=["number"]).corr()
    plt.figure(figsize=(9, 7))
    sns.heatmap(num, annot=False, cmap="viridis", vmin=-1, vmax=1)
    plt.title(title)
    plt.tight_layout()
    out = outdir / "correlations.png"
    plt.savefig(out, dpi=150)
    plt.close()

def save_time_trend(df: pd.DataFrame, date_col: str, value_col: str, outdir: Path, title: str):
    _ensure_dir(outdir)
    ts = (
        df[[date_col, value_col]]
        .dropna()
        .assign(month=lambda d: d[date_col].dt.to_period("M").dt.to_timestamp())
        .groupby("month")[value_col]
        .mean()
    )
    if ts.empty:
        return
    plt.figure(figsize=(9, 4))
    ts.plot(marker="o")
    plt.title(title)
    plt.xlabel("month")
    plt.ylabel(value_col)
    plt.tight_layout()
    out = outdir / f"time_{value_col}.png"
    plt.savefig(out, dpi=150)
    plt.close()

def save_map(df: pd.DataFrame, outdir: Path, price_col: str | None = None):
    lat_col = next((c for c in COLS["lat"] if c in df.columns), None)
    lon_col = next((c for c in COLS["lon"] if c in df.columns), None)
    if not lat_col or not lon_col or df.empty:
        return
    _ensure_dir(outdir)

    center = [df[lat_col].median(), df[lon_col].median()]
    m = folium.Map(location=center, zoom_start=11)

    # Cap points to avoid huge files
    sample = df.sample(min(len(df), 500), random_state=42)

    for _, r in sample.iterrows():
        popup = None
        if price_col and price_col in df.columns:
            popup = f"${r[price_col]:.0f}" if pd.notna(r[price_col]) else None
        folium.CircleMarker(
            location=[r[lat_col], r[lon_col]],
            radius=3,
            fill=True,
            popup=popup,
        ).add_to(m)

    out_html = outdir / "map_listings.html"
    m.save(str(out_html))
    return out_html
