# Data Dictionary — Bluestock MF Analytics

Auto-generated on Day 2 of the project. Documents every table in `bluestock_mf.db`.

## `dim_fund`
**Source:** 01_fund_master.csv

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER, PK | Unique AMFI scheme code identifying a fund |
| fund_house | TEXT | Asset Management Company (AMC) name |
| scheme_name | TEXT | Full scheme name including plan/option |
| category | TEXT | Broad fund category, e.g. Equity, Debt, Hybrid |
| sub_category | TEXT | Fund sub-category, e.g. Large Cap, Mid Cap |
| plan | TEXT | Regular or Direct plan |
| launch_date | DATE | Date the scheme was launched |
| benchmark | TEXT | Benchmark index tracked by the scheme |
| expense_ratio_pct | REAL | Annual expense ratio charged, in percent |
| exit_load_pct | REAL | Exit load percentage applicable on redemption |
| min_sip_amount | REAL | Minimum SIP investment amount in INR |
| min_lumpsum_amount | REAL | Minimum lumpsum investment amount in INR |
| fund_manager | TEXT | Name of the fund manager |
| risk_category | TEXT | SEBI risk-o-meter category |
| sebi_category_code | TEXT | SEBI-defined scheme category code |

## `dim_date`
**Source:** Derived (generated calendar dimension)

| Column | Type | Description |
|---|---|---|
| date_key | TEXT, PK | Date in YYYY-MM-DD format, used as join key |
| full_date | DATE | Full calendar date |
| year | INTEGER | Calendar year |
| quarter | INTEGER | Calendar quarter (1-4) |
| month | INTEGER | Calendar month (1-12) |
| month_name | TEXT | Full month name |
| day | INTEGER | Day of month |
| day_of_week | TEXT | Name of weekday |
| is_weekend | INTEGER | 1 if Saturday/Sunday, else 0 |

## `fact_nav`
**Source:** 02_nav_history.csv

| Column | Type | Description |
|---|---|---|
| nav_id | INTEGER, PK | Surrogate key, auto-incrementing |
| amfi_code | INTEGER, FK -> dim_fund | Scheme identifier |
| date_key | TEXT, FK -> dim_date | NAV date |
| nav | REAL | Net Asset Value per unit on given date, in INR |

## `fact_transactions`
**Source:** 08_investor_transactions.csv

| Column | Type | Description |
|---|---|---|
| transaction_id | INTEGER, PK | Surrogate key, auto-incrementing |
| investor_id | TEXT | Unique investor identifier |
| amfi_code | INTEGER, FK -> dim_fund | Scheme invested in |
| date_key | TEXT, FK -> dim_date | Transaction date |
| transaction_type | TEXT | One of SIP, Lumpsum, Redemption |
| amount_inr | REAL | Transaction amount in INR |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | City classification, e.g. T30 (Top 30) / B30 (Beyond 30) |
| age_group | TEXT | Investor age bracket |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Investor's annual income in INR lakh |
| payment_mode | TEXT | Mode of payment, e.g. UPI, Cheque |
| kyc_status | TEXT | Verified or Pending |

## `fact_performance`
**Source:** 07_scheme_performance.csv

| Column | Type | Description |
|---|---|---|
| performance_id | INTEGER, PK | Surrogate key, auto-incrementing |
| amfi_code | INTEGER, FK -> dim_fund | Scheme identifier |
| return_1yr_pct | REAL | Trailing 1-year return, percent |
| return_3yr_pct | REAL | Trailing 3-year annualised return, percent |
| return_5yr_pct | REAL | Trailing 5-year annualised return, percent |
| benchmark_3yr_pct | REAL | Benchmark's 3-year return, percent |
| alpha | REAL | Excess return vs benchmark, risk-adjusted |
| beta | REAL | Volatility relative to benchmark |
| sharpe_ratio | REAL | Risk-adjusted return metric (excess return / std dev) |
| sortino_ratio | REAL | Downside-risk-adjusted return metric |
| std_dev_ann_pct | REAL | Annualised standard deviation, percent |
| max_drawdown_pct | REAL | Maximum peak-to-trough decline, percent |
| aum_crore | REAL | Assets Under Management, INR crore |
| expense_ratio_pct | REAL | Annual expense ratio, percent (valid range 0.1-2.5) |
| morningstar_rating | INTEGER | Morningstar star rating, 1-5 |
| risk_grade | TEXT | Qualitative risk grade, e.g. Moderate |
| is_return_anomaly | INTEGER | 1 if return values fall outside -90% to 200% (flag) |
| is_expense_ratio_valid | INTEGER | 1 if expense_ratio_pct within 0.1%-2.5% |

## `fact_aum`
**Source:** 03_aum_by_fund_house.csv

| Column | Type | Description |
|---|---|---|
| aum_id | INTEGER, PK | Surrogate key, auto-incrementing |
| fund_house | TEXT | Asset Management Company name |
| date_key | TEXT, FK -> dim_date | Reporting date |
| aum_lakh_crore | REAL | Total AUM in INR lakh crore |
| aum_crore | REAL | Total AUM in INR crore |
| num_schemes | INTEGER | Number of schemes offered by the fund house |
