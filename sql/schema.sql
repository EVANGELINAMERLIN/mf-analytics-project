-- 
-- BLUESTOCK MUTUAL FUND STAR SCHEMA
-- 

-- Dimension: Fund
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code          INTEGER PRIMARY KEY,
    fund_house         TEXT    NOT NULL,
    scheme_name        TEXT    NOT NULL,
    category           TEXT,
    sub_category       TEXT,
    plan               TEXT,
    benchmark          TEXT,
    fund_manager       TEXT,
    risk_category      TEXT,
    sebi_category_code TEXT,
    expense_ratio_pct  REAL,
    exit_load_pct      REAL,
    min_sip_amount     REAL,
    min_lumpsum_amount REAL,
    launch_date        DATE
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id     INTEGER PRIMARY KEY,
    full_date   DATE    NOT NULL UNIQUE,
    day         INTEGER,
    month       INTEGER,
    month_name  TEXT,
    quarter     INTEGER,
    year        INTEGER,
    is_weekend  INTEGER,
    is_monthend INTEGER
);

-- Fact: NAV History
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL,
    date      DATE    NOT NULL,
    nav       REAL    NOT NULL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    txn_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code        INTEGER,
    transaction_date DATE,
    transaction_type TEXT,
    amount           REAL,
    units            REAL,
    nav_at_txn       REAL,
    investor_id      TEXT,
    state            TEXT,
    kyc_status       TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Performance
CREATE TABLE IF NOT EXISTS fact_performance (
    perf_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code     INTEGER,
    as_of_date    DATE,
    return_1m     REAL,
    return_3m     REAL,
    return_6m     REAL,
    return_1y     REAL,
    return_3y     REAL,
    return_5y     REAL,
    expense_ratio REAL,
    has_anomaly   INTEGER DEFAULT 0,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: AUM
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code  INTEGER,
    fund_house TEXT,
    month      DATE,
    aum_crores REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
