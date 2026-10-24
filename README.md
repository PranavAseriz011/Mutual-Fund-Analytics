# 📊 Mutual Fund Analytics

An end-to-end data analytics project focused on mutual fund data ingestion, data cleaning, database design, and SQL-based financial analysis.

The project transforms raw mutual fund datasets into structured, analysis-ready data and stores them in a SQLite database for analytical queries and future dashboard development.

## 🎯 Project Objectives

* Ingest and explore mutual fund datasets.
* Retrieve mutual fund Net Asset Value (NAV) data.
* Validate scheme codes and identify data quality issues.
* Clean and standardize datasets for reliable analysis.
* Design a relational database using a star schema.
* Perform SQL-based analysis of mutual fund performance, assets under management, investor transactions, and SIP inflows.
* Prepare the foundation for interactive financial analytics dashboards.

## 🛠️ Technologies Used

* **Programming:** Python
* **Data Analysis:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn, Plotly
* **Database:** SQLite
* **SQL Integration:** SQLAlchemy and Pandas
* **Data Collection:** Requests, MFAPI
* **Development:** Jupyter Notebook
* **Version Control:** Git and GitHub

## 📁 Project Structure

```text
Mutual-Fund-Analytics/
│
├── data/
│   ├── raw/                  # Original datasets
│   └── processed/            # Cleaned datasets
│
├── notebooks/                # Data exploration and cleaning notebooks
│
├── sql/
│   ├── schema.sql            # Database schema definitions
│   └── queries.sql           # Analytical SQL queries
│
├── dashboard/                # Dashboard development
├── reports/                  # Project reports and documentation
│
├── data_ingestion.py         # Dataset ingestion and inspection
├── explore_fund_master.py    # Fund master exploration
├── live_nav_fetch.py         # NAV data retrieval
├── validate_amfi_codes.py    # AMFI scheme-code validation
├── load_to_sqlite.py         # Load datasets into SQLite
├── load_star_schema.py       # Populate star-schema tables
├── verify_database.py        # Database verification
├── run_queries.py            # Execute analytical SQL queries
│
├── data_dictionary.md        # Dataset and schema documentation
├── bluestock_mf.db           # SQLite database
├── requirements.txt          # Python dependencies
├── README.md
└── .gitignore
```

## 📅 Day 1 — Project Setup and Data Ingestion

### Status: Completed ✅

The first phase focused on setting up the project environment, inspecting the provided datasets, retrieving NAV data, and validating scheme-code coverage.

### Day 1 Tasks Completed

* Created the project directory structure.
* Installed the required Python dependencies and created `requirements.txt`.
* Loaded and inspected all 10 original CSV datasets using Pandas.
* Examined dataset dimensions, data types, sample records, missing values, and duplicate rows.
* Retrieved NAV data from MFAPI for six mutual fund schemes.
* Explored fund houses, categories, subcategories, and risk classifications in the fund master.
* Validated AMFI scheme codes between the fund master and NAV history datasets.
* Created supporting scripts for data ingestion, NAV extraction, fund exploration, and scheme-code validation.
* Committed and pushed the project to GitHub.

### Day 1 Data Quality Summary

| Metric                                     | Result |
| ------------------------------------------ | -----: |
| Original datasets inspected                |     10 |
| Total records across original datasets     | 87,533 |
| Unique fund master scheme codes            |     40 |
| Unique NAV history scheme codes            |     40 |
| Fund master codes missing from NAV history |      0 |
| Datasets containing missing values         |      1 |

**Observation:** The Monthly SIP Inflows dataset contained 12 missing values in `yoy_growth_pct`, corresponding to January–December 2022. These were identified during data inspection and were not automatically replaced with zero.

**Validation result:** All 40 unique scheme codes in the fund master were found in the NAV history dataset.

## 📅 Day 2 — Data Cleaning and SQL Database Design

Status: Completed ✅

The second phase focused on preparing cleaned datasets, building the SQLite database, implementing a star schema, and executing analytical SQL queries.

### Day 2 Tasks Completed

* Created 10 cleaned CSV datasets in `data/processed/`.
* Developed a data dictionary documenting datasets, columns, and database tables.
* Created and populated the SQLite database `bluestock_mf.db`.
* Designed six star-schema tables with primary-key and foreign-key relationships.
* Loaded data into the database and verified table record counts.
* Checked foreign-key integrity.
* Created 10 analytical SQL queries.
* Executed the analytical queries and verified their successful execution.
* Corrected the query for identifying the top five individual mutual funds by AUM.
* Committed and pushed the Day 2 changes to GitHub.

### Database Design

The database contains six core analytical tables:

| Table               | Purpose                                                            |
| ------------------- | ------------------------------------------------------------------ |
| `dim_fund`          | Stores mutual fund identification and descriptive information.     |
| `dim_date`          | Stores calendar attributes for date-based analysis.                |
| `fact_nav`          | Stores mutual fund NAV observations.                               |
| `fact_transactions` | Stores investor transaction records.                               |
| `fact_performance`  | Stores fund performance, risk, expense ratio, and related metrics. |
| `fact_aum`          | Stores assets-under-management information.                        |

The star schema provides a structured foundation for joining fund, date, NAV, transaction, performance, and AUM information.

### Database Record Counts

| Table               | Records |
| ------------------- | ------: |
| `dim_fund`          |      40 |
| `dim_date`          |   1,297 |
| `fact_nav`          |  46,000 |
| `fact_transactions` |  32,778 |
| `fact_performance`  |      40 |
| `fact_aum`          |      90 |

These counts reflect the database verification results recorded during Day 2.

### Analytical SQL

The project includes 10 analytical SQL queries covering questions such as:

1. Which five mutual funds have the highest AUM?
2. What is the average NAV for each month?
3. How has SIP inflow growth changed year over year?
4. How are investor transactions distributed across states?
5. Which funds have an expense ratio below 1%?
6. How do mutual fund performance metrics compare?
7. How is AUM distributed across fund houses?
8. What trends can be identified in NAV history?
9. How do transaction types compare?
10. What additional insights can be extracted from the available datasets?

The exact SQL implementations are available in `sql/queries.sql`.

## 📦 Key Deliverables

| Deliverable           | Description                                                           |
| --------------------- | --------------------------------------------------------------------- |
| `data/processed/`     | Contains the cleaned CSV datasets.                                    |
| `bluestock_mf.db`     | SQLite database containing the loaded datasets and analytical tables. |
| `sql/schema.sql`      | SQL definitions for the star-schema tables.                           |
| `sql/queries.sql`     | Ten analytical SQL queries.                                           |
| `data_dictionary.md`  | Dataset, column, and schema documentation.                            |
| `load_to_sqlite.py`   | Script for loading cleaned datasets into SQLite.                      |
| `load_star_schema.py` | Script for populating the star-schema tables.                         |
| `verify_database.py`  | Script for checking database tables and record counts.                |
| `run_queries.py`      | Script for executing analytical SQL queries.                          |

## 🚀 Setup and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/PranavAseriz011/Mutual-Fund-Analytics.git
cd Mutual-Fund-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify the Database

```bash
python verify_database.py
```

### 5. Execute the Analytical Queries

```bash
python run_queries.py
```

**Note:** Database loading scripts are provided for rebuilding the database when required. Follow the schema and loading order defined by the project scripts.

## 🔗 GitHub Version Control

**Repository:** [PranavAseriz011/Mutual-Fund-Analytics](https://github.com/PranavAseriz011/Mutual-Fund-Analytics)

| Milestone        | Commit Message                           |
| ---------------- | ---------------------------------------- |
| Day 1            | `Day 1: Data ingestion complete`         |
| Day 2            | `Day 2: Cleaned data + SQLite DB loaded` |
| Query correction | `Fix top 5 funds by AUM query`           |

The Day 1 and Day 2 work, including the subsequent query correction, has been committed and pushed to GitHub.

## 🔮 Next Steps

* Complete a final audit of data-cleaning and validation rules.
* Perform exploratory data analysis on fund performance and investor transactions.
* Develop additional insights into risk, returns, AUM, and SIP trends.
* Build an interactive dashboard using Power BI.
* Document analytical findings and business recommendations.

## 👨‍💻 Project Focus

This project demonstrates practical experience in Python-based data processing, SQL, relational database design, data quality validation, and financial analytics.

The goal is to build a reproducible analytics workflow that transforms raw financial data into meaningful insights.
