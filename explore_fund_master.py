from pathlib import Path
import pandas as pd

# Locate the raw data folder
PROJECT_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

# Load the fund master dataset
file_path = RAW_DATA_DIR / "01_fund_master.csv"
df = pd.read_csv(file_path)

print("=" * 50)
print("MUTUAL FUND MASTER DATA EXPLORATION")
print("=" * 50)

# Dataset overview
print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Column Names:")
print(df.columns.tolist())

print("\n3. Data Types:")
print(df.dtypes)

print("\n4. First Five Records:")
print(df.head().to_string(index=False))

# Explore relevant categorical columns
keywords = ["house", "category", "subcategory", "sub_category", "risk"]

for column in df.columns:
    if any(keyword in column.lower() for keyword in keywords):
        print(f"\n5. Unique Values in '{column}':")
        print(df[column].dropna().unique())

print("\nFund master exploration completed!")