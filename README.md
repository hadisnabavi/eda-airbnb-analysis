# EDA: Airbnb Listings — Pricing, Location & Seasonality

This repository explores Airbnb listings to understand **pricing drivers**, **neighborhood popularity**, and **seasonal patterns**.

> Core outputs: a documented EDA notebook, clean plotting utilities, a small validation test-suite, and reproducible scripts.

---

## 1) Objectives
- Identify features most strongly associated with nightly price (e.g., room type, location, reviews).
- Map spatial patterns of listings and average prices by neighborhood or lat/lon.
- Examine temporal patterns (e.g., monthly review activity as a proxy for demand).
- Produce clear visuals and a concise write-up of findings.

---

## 2) Project Structure
```
eda-airbnb-analysis
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── .gitignore
├── .pre-commit-config.yaml
├── data
│   ├── external/        # third-party data (geojson/shapefiles, optional)
│   ├── interim/         # cleaned-but-not-final
│   ├── processed/       # analysis-ready datasets
│   ├── raw/             # original listings (DO NOT COMMIT)
│   └── raw/
│       └── listings.csv
├── notebooks
│   └── 01_exploratory_analysis.ipynb
├── reports
│   └── figures/         # charts saved here
├── src
│   ├── __init__.py
│   ├── config.py
│   ├── cleaning.py
│   ├── data_loading.py
│   ├── eda.py
│   ├── utils.py
│   └── viz.py
└── tests
    └── test_data_quality.py
```

---

## 3) Getting Started

### Environment
```bash
make install
source .venv/bin/activate
make precommit
```

### Run tests
```bash
make test
```

### Open the notebook
```bash
make notebook
```
Open `notebooks/01_exploratory_analysis.ipynb` and run cells top-to-bottom.

### Quick EDA run (uses the small synthetic sample)
```bash
make run-eda
```
This produces charts under `reports/figures`.

---

## 4) Data
Place the original listings CSV under `data/raw/`, e.g. `data/raw/listings.csv`.
The EDA expects these common columns when available (case-insensitive, flexible):
- `price` (nightly price, numeric after cleaning)
- `latitude`, `longitude`
- `room_type`
- `neighbourhood` or `neighbourhood_cleansed`
- `last_review` (for temporal trends, optional)
- `number_of_reviews` (optional)
- `availability_365` (optional)

If some fields are missing, the notebook and scripts skip those sections gracefully.

---

## 5) Workflow (Step-by-Step)

1. **Load & Inspect**
   - Load CSV, standardize column names, and parse types.
   - Basic sanity checks (non-negative price, lat/lon ranges).

2. **Clean**
   - Remove currency symbols and commas from `price` and cast to float.
   - Filter out extreme outliers via IQR or domain rules.
   - Handle missing values (drop or impute depending on column).

3. **Explore (Univariate → Bivariate → Multivariate)**
   - Distributions: price, reviews, availability.
   - Grouped summaries: price by room type, neighborhood.
   - Correlations between numeric features.
   - Time trends: monthly averages where `last_review` exists.

4. **Map**
   - Plot listing locations and price quantiles with Folium.
   - Optional: Choropleth by neighborhood (if a GeoJSON is available).

5. **Summarize Findings**
   - Capture key drivers of price (e.g., location, room type).
   - Note caveats and data quality issues.
   - Save charts to `reports/figures` and add a short narrative below.

---

## 6) Reproducible Scripts

You can run `src/eda.py` from CLI to execute the basic analysis:
```bash
python -m src.eda --input data/raw/listings.csv --output reports/figures
```
Flags:
- `--input`: path to the listings CSV
- `--output`: directory to save figures

---

## 7) Interpreting Results (Fill-in After Running on Real Data)

- **Top price drivers:** _e.g., neighborhood explains X% variance; room type premium ~Y%._  
- **Spatial pattern:** _hotspots appear near ..._  
- **Seasonality:** _average review activity peaks in ... months._  
- **Actionable insights:** _consider ..._

---

## 8) Notes
- The repo includes a tiny synthetic sample for smoke tests. Replace with the real dataset for meaningful results.
- Large raw data is ignored by git; commit only notebooks, scripts, and small artifacts.
