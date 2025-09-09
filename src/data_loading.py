from pathlib import Path
import pandas as pd

def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    df = pd.read_csv(path, low_memory=False)
    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    return df
