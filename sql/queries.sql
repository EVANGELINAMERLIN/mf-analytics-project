-- Query: 01_top5_funds_by_aum
SELECT df.scheme_name, df.fund_house, fp.aum_crore
FROM fact_performance fp
JOIN dim_fund df ON df.amfi_code = fp.amfi_code
ORDER BY fp.aum_crore DESC
LIMIT 5;

-- Query: 02_avg_nav_per_month
SELECT dd.year, dd.month, fn.amfi_code, ROUND(AVG(fn.nav), 2) AS avg_nav
FROM fact_nav fn
JOIN dim_date dd ON dd.date_key = fn.date_key
GROUP BY dd.year, dd.month, fn.amfi_code
ORDER BY fn.amfi_code, dd.year, dd.month;

-- Query: 03_sip_yoy_growth
SELECT dd.year, ROUND(SUM(ft.amount_inr), 2) AS total_sip_amount
FROM fact_transactions ft
JOIN dim_date dd ON dd.date_key = ft.date_key
WHERE ft.transaction_type = 'SIP'
GROUP BY dd.year
ORDER BY dd.year;

-- Query: 04_transactions_by_state
SELECT state, COUNT(*) AS num_transactions, ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- Query: 05_funds_expense_ratio_below_1pct
SELECT df.scheme_name, df.fund_house, fp.expense_ratio_pct
FROM fact_performance fp
JOIN dim_fund df ON df.amfi_code = fp.amfi_code
WHERE fp.expense_ratio_pct < 1.0
ORDER BY fp.expense_ratio_pct ASC;

-- Query: 06_top5_schemes_by_1yr_return
SELECT df.scheme_name, df.fund_house, fp.return_1yr_pct
FROM fact_performance fp
JOIN dim_fund df ON df.amfi_code = fp.amfi_code
ORDER BY fp.return_1yr_pct DESC
LIMIT 5;

-- Query: 07_avg_ticket_size_by_transaction_type
SELECT transaction_type, COUNT(*) AS num_txns, ROUND(AVG(amount_inr), 2) AS avg_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY avg_amount DESC;

-- Query: 08_kyc_status_distribution_by_city_tier
SELECT city_tier, kyc_status, COUNT(*) AS num_investors
FROM fact_transactions
GROUP BY city_tier, kyc_status
ORDER BY city_tier, kyc_status;

-- Query: 09_aum_growth_by_fund_house
SELECT fund_house, date_key, aum_crore
FROM fact_aum
WHERE fund_house IN (
    SELECT fund_house FROM fact_aum GROUP BY fund_house
    ORDER BY MAX(aum_crore) DESC LIMIT 5
)
ORDER BY fund_house, date_key;

-- Query: 10_risk_adjusted_return_ranking
SELECT df.scheme_name, df.fund_house, fp.sharpe_ratio, fp.sortino_ratio, fp.std_dev_ann_pct
FROM fact_performance fp
JOIN dim_fund df ON df.amfi_code = fp.amfi_code
ORDER BY fp.sharpe_ratio DESC
LIMIT 10;

