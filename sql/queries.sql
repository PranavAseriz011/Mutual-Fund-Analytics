-- ============================================================
-- Mutual Fund Analytics: 10 Analytical SQL Queries
-- Database: bluestock_mf.db
-- ============================================================

-- 1. Top 5 fund houses by latest available AUM
SELECT
fund_house,
aum_crore,
num_schemes,
date_key
FROM fact_aum
WHERE date_key = (
SELECT MAX(date_key)
FROM fact_aum
)
ORDER BY aum_crore DESC
LIMIT 5;



-- 2. Average NAV per month for each fund
SELECT
    f.scheme_name,
    d.year,
    d.month,
    ROUND(AVG(n.nav), 4) AS average_nav
FROM fact_nav n
JOIN dim_fund f ON n.fund_key = f.fund_key
JOIN dim_date d ON n.date_key = d.date_key
GROUP BY f.scheme_name, d.year, d.month
ORDER BY d.year, d.month, f.scheme_name;


-- 3. SIP inflow year-over-year growth
SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;


-- 4. Transaction amount by state
SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM investor_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;


-- 5. Funds with expense ratio below 1%
SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;


-- 6. Top 10 funds by 3-year return
SELECT
    f.scheme_name,
    f.fund_house,
    p.return_3yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.fund_key = f.fund_key
WHERE p.return_3yr_pct IS NOT NULL
ORDER BY p.return_3yr_pct DESC
LIMIT 10;


-- 7. Transaction breakdown by transaction type
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS average_amount_inr
FROM investor_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;


-- 8. Benchmark index closing values by index
SELECT
    index_name,
    ROUND(AVG(close_value), 2) AS average_close_value,
    MIN(close_value) AS minimum_close_value,
    MAX(close_value) AS maximum_close_value
FROM benchmark_indices
GROUP BY index_name
ORDER BY average_close_value DESC;


-- 9. Portfolio holdings by sector
SELECT
    sector,
    COUNT(*) AS holding_count,
    ROUND(SUM(market_value_cr), 2) AS total_market_value_cr
FROM portfolio_holdings
GROUP BY sector
ORDER BY total_market_value_cr DESC;


-- 10. Monthly category inflows
SELECT
    category,
    ROUND(AVG(net_inflow_crore), 2) AS average_monthly_inflow_crore,
    ROUND(SUM(net_inflow_crore), 2) AS total_inflow_crore
FROM category_inflows
GROUP BY category
ORDER BY total_inflow_crore DESC;