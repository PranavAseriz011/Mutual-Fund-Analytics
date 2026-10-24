from pathlib import Path
import sqlite3

import pandas as pd

# Project paths
PROJECT_PATH = Path(__file__).resolve().parent
PROCESSED_PATH = PROJECT_PATH / "data" / "processed"
SCHEMA_PATH = PROJECT_PATH / "sql" / "schema.sql"
DB_PATH = PROJECT_PATH / "bluestock_mf.db"

# All ten cleaned datasets
CSV_FILES = sorted(PROCESSED_PATH.glob("cleaned_*.csv"))

if not SCHEMA_PATH.exists():
    raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

if len(CSV_FILES) != 10:
    raise ValueError(
        f"Expected 10 cleaned CSV files, found {len(CSV_FILES)}"
    )

# Read datasets
dataframes = {
    file.stem.removeprefix("cleaned_"): pd.read_csv(file)
    for file in CSV_FILES
}

# Create database and schema
with sqlite3.connect(DB_PATH) as conn:
    conn.execute("PRAGMA foreign_keys = ON")

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema_sql)

    # Preserve every cleaned dataset in its own table.
    # These tables retain the original cleaned columns.
    for name, df in dataframes.items():
        df.to_sql(
            name,
            conn,
            if_exists="replace",
            index=False
        )
        print(f"Loaded {name}: {len(df):,} rows")

print(f"\nDatabase created at: {DB_PATH}")
print("All ten cleaned datasets loaded into SQLite.")