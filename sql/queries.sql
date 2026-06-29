-- 
-- BLUESTOCK MF - 10 ANALYTICAL SQL QUERIES

-- Q1: Top 5 Fund Houses by AUM
SELECT
    fund_house,
    ROUND(SUM(aum_crores), 2) AS total_aum_crores
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crores DESC
LIMIT 5;

-- Q2: Average NAV Per Month
SELECT
    STRFTIME('%Y-%m', date) AS month,
    amfi_code,
    ROUND(AVG(nav), 4)      AS avg_nav
FROM fact_nav
GROUP BY month, amfi_code
ORDER BY month DESC
LIMIT 10;

-- Q3: SIP Year-on-Year Growth
SELECT
    STRFTIME('%Y', transaction_date) AS year,
    COUNT(*)                          AS sip_count,
    ROUND(SUM(amount), 2)             AS total_sip_amount
FROM fact_transactions
WHERE UPPER(transaction_type) = 'SIP'
GROUP BY year
ORDER BY year;

-- Q4: Transactions by State
SELECT
    state,
    COUNT(*)              AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC
LIMIT 10;

-- Q5: Funds with Expense Ratio < 1%
SELECT
    scheme_name,
    fund_house,
    category,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC
LIMIT 10;

-- Q6: Top 10 NAV Growth Funds
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    ROUND(MIN(n.nav), 2)                AS start_nav,
    ROUND(MAX(n.nav), 2)                AS end_nav,
    ROUND((MAX(n.nav)-MIN(n.nav))
          /MIN(n.nav)*100, 2)           AS growth_pct
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY n.amfi_code
ORDER BY growth_pct DESC
LIMIT 10;

-- Q7: Monthly SIP Trend
SELECT
    STRFTIME('%Y-%m', transaction_date) AS month,
    COUNT(*)                             AS sip_count,
    ROUND(SUM(amount), 2)               AS total_sip
FROM fact_transactions
WHERE UPPER(transaction_type) = 'SIP'
GROUP BY month
ORDER BY month
LIMIT 12;

-- Q8: Category-wise Transaction Volume
SELECT
    f.category,
    COUNT(t.rowid)         AS txn_count,
    ROUND(SUM(t.amount),2) AS total_amount
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY f.category
ORDER BY total_amount DESC;

-- Q9: Risk Category vs Avg Expense Ratio
SELECT
    risk_category,
    COUNT(*)                          AS scheme_count,
    ROUND(AVG(expense_ratio_pct), 4)  AS avg_expense_ratio,
    ROUND(MIN(expense_ratio_pct), 4)  AS min_expense,
    ROUND(MAX(expense_ratio_pct), 4)  AS max_expense
FROM dim_fund
GROUP BY risk_category
ORDER BY avg_expense_ratio;

-- Q10: Top Fund Managers by Scheme Count
SELECT
    fund_manager,
    COUNT(*)                          AS scheme_count,
    ROUND(AVG(expense_ratio_pct), 4)  AS avg_expense,
    GROUP_CONCAT(DISTINCT category)   AS categories
FROM dim_fund
GROUP BY fund_manager
ORDER BY scheme_count DESC
LIMIT 10;
