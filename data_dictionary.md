# Mutual Fund Analytics — Data Dictionary

## 1. Project Overview

**Project:** Capstone Project I — Mutual Fund Analytics
**Purpose:** Clean, organize, and analyze mutual fund data using Python, Pandas, SQLite, and SQL.

### Data Sources

The project contains 10 cleaned CSV datasets stored in `data/processed/`.

## 2. Cleaned Datasets

| Dataset               | Records | Description                                   |
| --------------------- | ------: | --------------------------------------------- |
| Fund Master           |      40 | Fund and scheme details                       |
| NAV History           |  46,000 | Historical net asset values                   |
| AUM by Fund House     |      90 | Assets under management by fund house         |
| Monthly SIP Inflows   |      48 | Monthly systematic investment plan statistics |
| Category Inflows      |     144 | Monthly inflows by mutual fund category       |
| Industry Folio Count  |      21 | Industry and category folio statistics        |
| Scheme Performance    |      40 | Fund returns, risk metrics, and ratings       |
| Investor Transactions |  32,778 | Investor transaction records                  |
| Portfolio Holdings    |     322 | Stock holdings within mutual fund portfolios  |
| Benchmark Indices     |   8,050 | Historical benchmark index closing values     |

## 3. Star Schema

### `dim_fund`

**Purpose:** Stores fund master information.

| Column             | Type    | Definition                           |
| ------------------ | ------- | ------------------------------------ |
| fund_key           | INTEGER | Primary key generated for each fund  |
| amfi_code          | TEXT    | Unique AMFI scheme identifier        |
| fund_house         | TEXT    | Fund management company              |
| scheme_name        | TEXT    | Mutual fund scheme name              |
| category           | TEXT    | Fund category                        |
| sub_category       | TEXT    | Fund subcategory                     |
| plan               | TEXT    | Scheme plan                          |
| launch_date        | TEXT    | Scheme launch date                   |
| benchmark          | TEXT    | Benchmark associated with the scheme |
| expense_ratio_pct  | REAL    | Expense ratio percentage             |
| exit_load_pct      | REAL    | Exit load percentage                 |
| min_sip_amount     | REAL    | Minimum SIP investment               |
| min_lumpsum_amount | REAL    | Minimum lump-sum investment          |
| fund_manager       | TEXT    | Fund manager                         |
| risk_category      | TEXT    | Risk classification                  |
| sebi_category_code | TEXT    | SEBI category code                   |

**Primary key:** `fund_key`
**Unique key:** `amfi_code`

### `dim_date`

**Purpose:** Supports date-based analysis.

| Column    | Type    | Definition                  |
| --------- | ------- | --------------------------- |
| date_key  | INTEGER | Date key in YYYYMMDD format |
| full_date | TEXT    | Calendar date               |
| year      | INTEGER | Calendar year               |
| month     | INTEGER | Calendar month              |
| quarter   | INTEGER | Calendar quarter            |

**Primary key:** `date_key`
**Unique key:** `full_date`

### `fact_nav`

**Purpose:** Stores daily NAV observations.

| Column   | Type    | Definition                        |
| -------- | ------- | --------------------------------- |
| nav_key  | INTEGER | Primary key                       |
| fund_key | INTEGER | Reference to `dim_fund`           |
| date_key | INTEGER | Reference to `dim_date`           |
| nav      | REAL    | Net asset value; must be positive |

### `fact_transactions`

**Purpose:** Stores investor transactions.

| Column             | Type    | Definition                             |
| ------------------ | ------- | -------------------------------------- |
| transaction_key    | INTEGER | Primary key                            |
| investor_id        | TEXT    | Investor identifier                    |
| fund_key           | INTEGER | Reference to `dim_fund`                |
| date_key           | INTEGER | Reference to `dim_date`                |
| transaction_type   | TEXT    | SIP, Lumpsum, or Redemption            |
| amount_inr         | REAL    | Transaction amount in INR              |
| state              | TEXT    | Investor's state                       |
| city               | TEXT    | Investor's city                        |
| city_tier          | TEXT    | City classification                    |
| age_group          | TEXT    | Investor age group                     |
| gender             | TEXT    | Recorded gender category               |
| annual_income_lakh | REAL    | Annual income in lakh rupees           |
| payment_mode       | TEXT    | Payment method                         |
| kyc_status         | TEXT    | Know Your Customer verification status |

### `fact_performance`

**Purpose:** Stores scheme return and risk measurements.

| Column             | Type    | Definition                               |
| ------------------ | ------- | ---------------------------------------- |
| performance_key    | INTEGER | Primary key                              |
| fund_key           | INTEGER | Unique reference to `dim_fund`           |
| return_1yr_pct     | REAL    | One-year return percentage               |
| return_3yr_pct     | REAL    | Three-year return percentage             |
| return_5yr_pct     | REAL    | Five-year return percentage              |
| benchmark_3yr_pct  | REAL    | Three-year benchmark return              |
| alpha              | REAL    | Reported alpha metric                    |
| beta               | REAL    | Reported beta metric                     |
| sharpe_ratio       | REAL    | Sharpe ratio                             |
| sortino_ratio      | REAL    | Sortino ratio                            |
| std_dev_ann_pct    | REAL    | Annualized standard deviation percentage |
| max_drawdown_pct   | REAL    | Maximum drawdown percentage              |
| aum_crore          | REAL    | Assets under management in crore rupees  |
| expense_ratio_pct  | REAL    | Expense ratio percentage                 |
| morningstar_rating | REAL    | Reported Morningstar rating              |
| risk_grade         | TEXT    | Reported risk grade                      |

### `fact_aum`

**Purpose:** Stores AUM observations by fund house and date.

| Column         | Type    | Definition               |
| -------------- | ------- | ------------------------ |
| aum_key        | INTEGER | Primary key              |
| fund_house     | TEXT    | Fund house name          |
| date_key       | INTEGER | Reference to `dim_date`  |
| aum_lakh_crore | REAL    | AUM in lakh crore rupees |
| aum_crore      | REAL    | AUM in crore rupees      |
| num_schemes    | INTEGER | Number of schemes        |

## 4. Source Tables

The database also preserves the 10 original cleaned datasets in individual tables:

* `fund_master`
* `nav_history`
* `aum_by_fund_house`
* `monthly_sip_inflows`
* `category_inflows`
* `industry_folio_count`
* `scheme_performance`
* `investor_transactions`
* `portfolio_holdings`
* `benchmark_indices`

These tables preserve the cleaned CSV columns for further analysis.

## 5. Data Quality and Validation

* Cleaned CSV files were exported to `data/processed/`.
* The six star-schema tables were populated.
* Foreign-key integrity checks passed.
* Ten analytical SQL queries were executed successfully.
* Original source tables were preserved.

## 6. Important Notes

* Data types in this document describe the SQLite schema.
* Source datasets retain their own original columns and may have different data types.
* Date dimensions currently cover dates collected from NAV history, investor transactions, and AUM observations.
* No missing NAV values should be fabricated without a documented business rule.
* Financial metrics should be interpreted using their source definitions and units.

## 7. Project Deliverables

* 10 cleaned CSV datasets
* `bluestock_mf.db`
* `sql/schema.sql`
* `sql/queries.sql`
* `data_dictionary.md`
* `load_to_sqlite.py`
* `load_star_schema.py`
* `run_queries.py`
