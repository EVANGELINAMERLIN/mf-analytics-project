# Data Dictionary — Bluestock Mutual Fund Analytics

## Project Overview
**Project**: Mutual Fund Customer Behavior Analytics
**Database**: bluestock_mf.db (SQLite)
**Analyst**: MERLIN J
**Date**: June 2026

---

## 1. dim_fund (Fund Master)
**Source**: 01_fund_master.csv

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| amfi_code | INTEGER | Unique AMFI code (PK) | 119551 |
| fund_house | TEXT | AMC name | SBI Mutual Fund |
| scheme_name | TEXT | Full scheme name | SBI Bluechip Fund |
| category | TEXT | SEBI category | Equity |
| sub_category | TEXT | Sub-category | Large Cap |
| plan | TEXT | Regular or Direct | Direct |
| launch_date | DATE | Scheme launch date | 2006-02-14 |
| benchmark | TEXT | Benchmark index | NIFTY 100 TRI |
| expense_ratio_pct | REAL | Annual fee % | 0.66 |
| exit_load_pct | REAL | Exit load % | 1.0 |
| min_sip_amount | REAL | Min SIP amount | 500 |
| min_lumpsum_amount | REAL | Min lumpsum | 1000 |
| fund_manager | TEXT | Fund manager name | Sohini Andani |
| risk_category | TEXT | Risk level | Moderate |
| sebi_category_code | TEXT | SEBI code | EC01 |

---

## 2. fact_nav (NAV History)
**Source**: 02_nav_history.csv

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| amfi_code | INTEGER | AMFI code (FK) | 119551 |
| date | DATE | NAV date | 2022-01-03 |
| nav | REAL | Net Asset Value | 54.3856 |

---

## 3. fact_transactions
**Source**: 08_investor_transactions.csv

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| amfi_code | INTEGER | AMFI code (FK) | 119551 |
| transaction_date | DATE | Date of transaction | 2023-01-15 |
| transaction_type | TEXT | SIP/Lumpsum/Redemption | SIP |
| amount | REAL | Transaction amount Rs. | 5000 |
| units | REAL | Units purchased | 91.82 |
| nav_at_txn | REAL | NAV at transaction | 54.45 |
| investor_id | TEXT | Investor identifier | INV001 |
| state | TEXT | Investor state | Maharashtra |
| kyc_status | TEXT | KYC verification | VERIFIED |

---

## 4. fact_performance
**Source**: 07_scheme_performance.csv

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| amfi_code | INTEGER | AMFI code (FK) | 119551 |
| return_1m | REAL | 1 month return % | 2.5 |
| return_3m | REAL | 3 month return % | 7.8 |
| return_6m | REAL | 6 month return % | 12.3 |
| return_1y | REAL | 1 year return % | 24.5 |
| return_3y | REAL | 3 year CAGR % | 18.2 |
| return_5y | REAL | 5 year CAGR % | 15.6 |
| expense_ratio | REAL | Expense ratio | 0.66 |
| has_anomaly | INTEGER | Anomaly flag | 0 |

---

## 5. fact_aum
**Source**: 03_aum_by_fund_house.csv

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| amfi_code | INTEGER | AMFI code (FK) | 119551 |
| fund_house | TEXT | AMC name | SBI Mutual Fund |
| month | DATE | Month of AUM | 2024-01-01 |
| aum_crores | REAL | AUM in Crores | 45231.5 |

---

## Business Definitions

| Term | Definition |
|------|------------|
| NAV | Net Asset Value — price per unit |
| AUM | Assets Under Management |
| SIP | Systematic Investment Plan |
| AMFI | Association of Mutual Funds in India |
| SEBI | Securities & Exchange Board of India |
| CAGR | Compound Annual Growth Rate |
| Expense Ratio | Annual fee as % of AUM |
| Exit Load | Fee on early redemption |
| KYC | Know Your Customer |
| Direct Plan | No distributor commission |
| Regular Plan | With distributor commission |

---

## Data Quality Notes

| Dataset | Status |
|---------|--------|
| fund_master | Cleaned |
| nav_history | Cleaned + Forward-filled |
| investor_transactions | Cleaned + Standardized |
| scheme_performance | Cleaned + Anomalies flagged |
| aum_by_fund_house | Cleaned |

---
*Prepared by: MERLIN J | Teyzix Core Internship June 2026*
