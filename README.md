# ✅ Day 1 — Project Setup & Data Ingestion

**Status:** Completed

The first phase of the Mutual Fund Analytics capstone focused on setting up the project environment, ingesting datasets, extracting mutual fund NAV data, and validating data quality.

## Tasks Completed

* Created the project folder structure.
* Installed the required Python dependencies and created `requirements.txt`.
* Loaded and inspected all 10 provided CSV datasets using Pandas.
* Examined dataset shapes, column data types, sample records, missing values, and duplicate rows.
* Retrieved NAV data from MFAPI for six mutual fund schemes.
* Explored the fund master dataset, including fund houses, categories, subcategories, and risk classifications.
* Validated AMFI scheme codes between the fund master and NAV history datasets.
* Created supporting Python scripts for data ingestion, NAV extraction, fund exploration, and scheme-code validation.
* Committed and pushed the project to GitHub.

### Data Quality Summary

| Metric                                     | Result |
| ------------------------------------------ | -----: |
| Original datasets inspected                |     10 |
| Total records across original datasets     | 87,533 |
| Unique fund master scheme codes            |     40 |
| Unique NAV history scheme codes            |     40 |
| Fund master codes missing from NAV history |      0 |
| Datasets containing missing values         |      1 |

**Observation:** The Monthly SIP Inflows dataset contains 12 missing values in `yoy_growth_pct`, corresponding to January–December 2022. These values were identified during data inspection and were not automatically replaced with zero.

**Validation result:** All 40 unique scheme codes in the fund master were found in the NAV history dataset.

### Project Structure

```text
Mutual-Fund-Analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── sql/
├── dashboard/
├── reports/
├── data_ingestion.py
├── explore_fund_master.py
├── live_nav_fetch.py
├── validate_amfi_codes.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* SQLAlchemy
* Requests
* SciPy
* Jupyter Notebook
* Git and GitHub

### Key Deliverables

* `data_ingestion.py` — Inspects the provided CSV datasets.
* `live_nav_fetch.py` — Retrieves and saves mutual fund NAV data.
* `explore_fund_master.py` — Explores fund master information.
* `validate_amfi_codes.py` — Validates scheme-code coverage between datasets.
* `requirements.txt` — Documents Python dependencies.
* `reports/` — Contains project data quality documentation.

### GitHub Version Control

**Day 1 commit:** `d6f5977`

**Commit message:** `Day 1: Data ingestion complete`

The Day 1 changes have been committed and pushed to the GitHub repository.

### Next Steps

The next phase will build on the validated datasets to develop deeper mutual fund analytics, including exploratory data analysis, performance comparisons, risk analysis, SQL-based analysis, and interactive dashboard development.
