

-- Bluestock MF Analytics — SQLite Star Schema


DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS dim_fund;
DROP TABLE IF EXISTS dim_date;

-- ------------------------------------------------------------
-- DIM: dim_fund  (one row per AMFI scheme code)
-- ------------------------------------------------------------
CREATE TABLE dim_fund (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT NOT NULL,
    scheme_name          TEXT NOT NULL,
    category             TEXT,
    sub_category          TEXT,
    plan                 TEXT,
    launch_date          DATE,
    benchmark             TEXT,
    expense_ratio_pct     REAL,
    exit_load_pct         REAL,
    min_sip_amount        REAL,
    min_lumpsum_amount    REAL,
    fund_manager           TEXT,
    risk_category          TEXT,
    sebi_category_code      TEXT
);

-- ------------------------------------------------------------
-- DIM: dim_date  (calendar dimension, generated from data range)
-- ------------------------------------------------------------
CREATE TABLE dim_date (
    date_key      TEXT PRIMARY KEY,     -- format YYYY-MM-DD
    full_date     DATE NOT NULL,
    year          INTEGER,
    quarter       INTEGER,
    month         INTEGER,
    month_name    TEXT,
    day           INTEGER,
    day_of_week   TEXT,
    is_weekend    INTEGER
);

-- ------------------------------------------------------------
-- FACT: fact_nav  (daily NAV per scheme)
-- ------------------------------------------------------------
CREATE TABLE fact_nav (
    nav_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code    INTEGER NOT NULL,
    date_key     TEXT NOT NULL,
    nav          REAL NOT NULL CHECK (nav > 0),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_key)  REFERENCES dim_date(date_key)
);

-- ------------------------------------------------------------
-- FACT: fact_transactions  (investor-level transactions)
-- ------------------------------------------------------------
CREATE TABLE fact_transactions (
    transaction_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id        TEXT NOT NULL,
    amfi_code          INTEGER NOT NULL,
    date_key           TEXT NOT NULL,
    transaction_type    TEXT NOT NULL CHECK (transaction_type IN ('SIP','Lumpsum','Redemption')),
    amount_inr          REAL NOT NULL CHECK (amount_inr > 0),
    state                TEXT,
    city                 TEXT,
    city_tier             TEXT,
    age_group             TEXT,
    gender                TEXT,
    annual_income_lakh     REAL,
    payment_mode           TEXT,
    kyc_status              TEXT CHECK (kyc_status IN ('Verified','Pending')),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_key)  REFERENCES dim_date(date_key)
);

-- ------------------------------------------------------------
-- FACT: fact_performance  (scheme-level return/risk metrics)
-- ------------------------------------------------------------
CREATE TABLE fact_performance (
    performance_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code           INTEGER NOT NULL,
    return_1yr_pct       REAL,
    return_3yr_pct       REAL,
    return_5yr_pct       REAL,
    benchmark_3yr_pct     REAL,
    alpha                 REAL,
    beta                  REAL,
    sharpe_ratio            REAL,
    sortino_ratio            REAL,
    std_dev_ann_pct           REAL,
    max_drawdown_pct           REAL,
    aum_crore                   REAL,
    expense_ratio_pct             REAL CHECK (expense_ratio_pct BETWEEN 0.1 AND 2.5),
    morningstar_rating              INTEGER CHECK (morningstar_rating BETWEEN 1 AND 5),
    risk_grade                        TEXT,
    is_return_anomaly                   INTEGER,
    is_expense_ratio_valid                INTEGER,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- ------------------------------------------------------------
-- FACT: fact_aum  (fund-house level AUM over time)
-- ------------------------------------------------------------
CREATE TABLE fact_aum (
    aum_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house         TEXT NOT NULL,
    date_key             TEXT NOT NULL,
    aum_lakh_crore         REAL,
    aum_crore                REAL,
    num_schemes                INTEGER,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);
