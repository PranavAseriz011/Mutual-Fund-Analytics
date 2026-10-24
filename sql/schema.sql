-- ============================================================
-- Mutual Fund Analytics
-- Day 2: SQLite Star Schema
-- ============================================================

PRAGMA foreign_keys = ON;

-- 1. FUND DIMENSION
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_key INTEGER PRIMARY KEY,
    amfi_code TEXT NOT NULL UNIQUE,
    fund_house TEXT,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- 2. DATE DIMENSION
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    quarter INTEGER NOT NULL
);

-- 3. NAV FACT TABLE
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_key INTEGER PRIMARY KEY,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    nav REAL NOT NULL CHECK (nav > 0),

    FOREIGN KEY (fund_key)
        REFERENCES dim_fund(fund_key),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    UNIQUE (fund_key, date_key)
);

-- 4. INVESTOR TRANSACTIONS FACT TABLE
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_key INTEGER PRIMARY KEY,
    investor_id TEXT NOT NULL,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount_inr REAL NOT NULL CHECK (amount_inr > 0),
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,

    FOREIGN KEY (fund_key)
        REFERENCES dim_fund(fund_key),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

-- 5. SCHEME PERFORMANCE FACT TABLE
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_key INTEGER PRIMARY KEY,
    fund_key INTEGER NOT NULL UNIQUE,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating REAL,
    risk_grade TEXT,

    FOREIGN KEY (fund_key)
        REFERENCES dim_fund(fund_key)
);

-- 6. AUM FACT TABLE
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_key INTEGER PRIMARY KEY,
    fund_house TEXT NOT NULL,
    date_key INTEGER NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    UNIQUE (fund_house, date_key)
);

-- Indexes for common analytical queries
CREATE INDEX IF NOT EXISTS idx_nav_fund_date
    ON fact_nav (fund_key, date_key);

CREATE INDEX IF NOT EXISTS idx_transactions_date
    ON fact_transactions (date_key);

CREATE INDEX IF NOT EXISTS idx_transactions_state
    ON fact_transactions (state);

CREATE INDEX IF NOT EXISTS idx_aum_date
    ON fact_aum (date_key);