from pathlib import Path
import pandas as pd

# Locate datasets
PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

# Load datasets
fund_master = pd.read_csv(RAW_DIR / "01_fund_master.csv")
nav_history = pd.read_csv(RAW_DIR / "02_nav_history.csv")

print("=" * 55)
print("AMFI SCHEME CODE VALIDATION")
print("=" * 55)

# Get unique scheme codes from each dataset
fund_codes = set(fund_master["amfi_code"].dropna())
nav_codes = set(nav_history["amfi_code"].dropna())

# Find codes missing from NAV history
missing_codes = fund_codes - nav_codes

# Display results
print(f"\nUnique codes in fund master: {len(fund_codes)}")
print(f"Unique codes in NAV history: {len(nav_codes)}")

print(f"\nCodes missing from NAV history: {len(missing_codes)}")

if missing_codes:
    print("\nMissing AMFI codes:")
    print(sorted(missing_codes))
else:
    print("\nAll fund master codes exist in NAV history!")

print("\nValidation completed.")