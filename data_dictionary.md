# Data Dictionary — Mutual Fund Analytics Project

This file explains what each column in bluestock_mf.db means.

## dim_fund — one row per mutual fund scheme
- amfi_code: unique ID for the fund
- fund_house: which company manages it (e.g. SBI, HDFC)
- scheme_name: full name of the fund
- category / sub_category: type of fund (e.g. Equity, Large Cap)
- expense_ratio_pct: yearly fee charged (%)
- risk_category: how risky the fund is (Low/Moderate/High)

## dim_date — one row per calendar day
- date_id: the date, used to link other tables to a specific day

## fact_nav — daily price (NAV) of each fund
- amfi_code: which fund
- date_id: which day
- nav: the fund's price per unit that day

## fact_transactions — every investor transaction
- transaction_type: SIP, Lumpsum, or Redemption
- amount_inr: how much money, in rupees
- state / city: where the investor is located
- kyc_status: whether their identity is verified

## fact_performance — how each fund has performed
- return_1yr_pct / return_3yr_pct / return_5yr_pct: returns over time
- sharpe_ratio: risk-adjusted performance score
- is_anomalous: flagged as an unusual/outlier value during cleaning

## fact_aum — total money managed by each fund house, over time
- fund_house: the company
- aum_crore: total assets managed, in crores of rupees
- num_schemes: how many funds they run

## Data quality notes
- Missing NAV values on weekends/holidays were filled using the previous day's price.
- All transaction amounts were checked to be greater than zero.
- Expense ratios were checked to fall between 0.1% and 2.5%.
- AMFI fund codes matched perfectly between our two main datasets (40/40),
  but did NOT match the live mfapi.in website for 5 out of 6 test codes —
  this is expected since our data is practice data, not live data.
