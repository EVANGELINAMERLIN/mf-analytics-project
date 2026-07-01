-- Query: top_5_funds_by_aum
SELECT scheme_name, fund_house, aum_crore
        FROM fact_performance fp
        JOIN dim_fund df ON fp.amfi_code = df.amfi_code
        ORDER BY aum_crore DESC
        LIMIT 5;

-- Query: avg_nav_per_month
SELECT dd.year, dd.month, df.scheme_name, ROUND(AVG(fn.nav), 2) AS avg_nav
        FROM fact_nav fn
        JOIN dim_date dd ON fn.date_id = dd.date_id
        JOIN dim_fund df ON fn.amfi_code = df.amfi_code
        GROUP BY dd.year, dd.month, df.scheme_name
        ORDER BY dd.year, dd.month;

-- Query: sip_yoy_growth
SELECT dd.year, dd.month, SUM(ft.amount_inr) AS total_sip_amount
        FROM fact_transactions ft
        JOIN dim_date dd ON ft.date_id = dd.date_id
        WHERE ft.transaction_type = 'SIP'
        GROUP BY dd.year, dd.month
        ORDER BY dd.year, dd.month;

-- Query: transactions_by_state
SELECT state, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
        FROM fact_transactions
        GROUP BY state
        ORDER BY total_amount DESC;

-- Query: funds_with_low_expense_ratio
SELECT scheme_name, fund_house, expense_ratio_pct
        FROM dim_fund
        WHERE expense_ratio_pct < 1.0
        ORDER BY expense_ratio_pct ASC;

-- Query: top_5_funds_by_1yr_return
SELECT df.scheme_name, fp.return_1yr_pct
        FROM fact_performance fp
        JOIN dim_fund df ON fp.amfi_code = df.amfi_code
        ORDER BY fp.return_1yr_pct DESC
        LIMIT 5;

-- Query: kyc_status_breakdown
SELECT kyc_status, COUNT(*) AS num_investors, SUM(amount_inr) AS total_amount
        FROM fact_transactions
        GROUP BY kyc_status;

-- Query: transaction_type_distribution
SELECT transaction_type, COUNT(*) AS num_transactions,
               ROUND(SUM(amount_inr), 2) AS total_amount,
               ROUND(AVG(amount_inr), 2) AS avg_amount
        FROM fact_transactions
        GROUP BY transaction_type;

-- Query: high_risk_high_sharpe_funds
SELECT df.scheme_name, df.risk_category, fp.sharpe_ratio, fp.return_3yr_pct
    FROM fact_performance fp
    JOIN dim_fund df ON fp.amfi_code = df.amfi_code
    WHERE df.risk_category IN ('High', 'Very High') AND fp.sharpe_ratio > 0.8
    ORDER BY fp.sharpe_ratio DESC;

-- Query: city_tier_investment_pattern
SELECT city_tier, COUNT(*) AS num_transactions,
               ROUND(SUM(amount_inr), 2) AS total_amount,
               ROUND(AVG(amount_inr), 2) AS avg_ticket_size
        FROM fact_transactions
        GROUP BY city_tier
        ORDER BY total_amount DESC;

