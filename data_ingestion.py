from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# The 10 original datasets use the numeric filename prefixes 01–10.
EXPECTED_DATASETS = [
    f"{number:02d}_"
    for number in range(1, 11)
]


def inspect_dataset(file_path: Path) -> None:
    """Load and inspect one CSV dataset."""

    print("\n" + "=" * 80)
    print(f"DATASET: {file_path.name}")
    print("=" * 80)

    try:
        df = pd.read_csv(file_path)

        print(f"\nShape: {df.shape}")

        print("\nData types:")
        print(df.dtypes.to_string())

        print("\nFirst five rows:")
        print(df.head().to_string())

        print("\nMissing values:")
        missing = df.isnull().sum()
        print(missing[missing > 0].to_string()
              if missing.any()
              else "No missing values found.")

        print(f"\nDuplicate rows: {df.duplicated().sum()}")

    except Exception as error:
        print(f"ERROR reading {file_path.name}: {error}")


def main() -> None:
    """Inspect the 10 supplied CSV datasets."""

    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(
            f"Raw data directory not found: {RAW_DATA_DIR}"
        )

    all_csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    # Select only the original datasets, excluding downloaded NAV files.
    datasets = [
        file_path
        for file_path in all_csv_files
        if any(
            file_path.name.startswith(prefix)
            for prefix in EXPECTED_DATASETS
        )
    ]

    print(f"Raw data directory: {RAW_DATA_DIR}")
    print(f"Expected original datasets: 10")
    print(f"Found original datasets: {len(datasets)}")

    if len(datasets) != 10:
        print(
            "\nWARNING: Expected 10 original datasets. "
            "Check the filenames and missing files."
        )

    if not datasets:
        raise FileNotFoundError(
            "No numbered source CSV datasets were found."
        )

    for file_path in datasets:
        inspect_dataset(file_path)

    print("\n" + "=" * 80)
    print("DATA INGESTION INSPECTION COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()