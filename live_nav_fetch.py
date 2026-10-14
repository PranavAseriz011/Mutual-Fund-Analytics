import requests
import pandas as pd
from pathlib import Path

# Project ka raw data folder
RAW_DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"

# Mutual fund scheme codes
SCHEMES = {
    "HDFC_Top_100_Direct": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841",
}

# Fetch NAV data from API
for scheme_name, scheme_code in SCHEMES.items():

    print(f"\nFetching {scheme_name}...")

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        result = response.json()

        # API se NAV records nikaalna
        nav_data = result.get("data", [])

        if not nav_data:
            print("No NAV data received.")
            continue

        df = pd.DataFrame(nav_data)

        # CSV file mein save karna
        output_file = RAW_DATA_DIR / f"{scheme_name}_nav.csv"
        df.to_csv(output_file, index=False)

        print(f"Records fetched: {len(df)}")
        print(f"Saved: {output_file.name}")

    except requests.RequestException as error:
        print(f"API request failed: {error}")

print("\nNAV fetching process finished!")