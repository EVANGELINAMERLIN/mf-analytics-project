

-- Mutual Fund Analytics — Star Schema


-- DIMENSION: Fund
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT,
    scheme_name          TEXT,
    category             TEXT,
    sub_category         TEXT,
    plan                 TEXT,
    launch_date          DATE,
    benchmark            TEXT,
    expense_ratio_pct    REAL,
    exit_load_pct        REAL,
    min_sip_amount       REAL,
    min_lumpsum_amount   REAL,
    fund_manager         TEXT,
    risk_category        TEXT,
    sebi_category_code   TEXT
);

-- DIMENSION: Date (generated calendar table)
CREATE TABLE IF NOT EXISTS dim_date (
    date_id       TEXT PRIMARY KEY,   -- format YYYY-MM-DD
    full_date     DATE,
    year          INTEGER,
    quarter       INTEGER,
    month         INTEGER,
    month_name    TEXT,
    day           INTEGER,
    day_of_week   TEXT,
    is_weekend    INTEGER
);

-- FACT: NAV history
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code    INTEGER,
    date_id      TEXT,
    nav          REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- FACT: Investor transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT,
    date_id              TEXT,
    amfi_code            INTEGER,
    transaction_type     TEXT,
    amount_inr           REAL,
    state                TEXT,
    city                 TEXT,
    city_tier             TEXT,
    age_group             TEXT,
    gender                TEXT,
    annual_income_lakh    REAL,
    payment_mode          TEXT,
    kyc_status             TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- FACT: Scheme performance
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code            INTEGER,
    return_1yr_pct       REAL,
    return_3yr_pct       REAL,
    return_5yr_pct       REAL,
    benchmark_3yr_pct    REAL,
    alpha                REAL,
    beta                 REAL,
    sharpe_ratio         REAL,
    sortino_ratio        REAL,
    std_dev_ann_pct      REAL,
    max_drawdown_pct     REAL,
    aum_crore            REAL,
    expense_ratio_pct    REAL,
    morningstar_rating   INTEGER,
    risk_grade           TEXT,
    is_anomalous         INTEGER,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- FACT: AUM by fund house
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id           TEXT,
    fund_house        TEXT,
    aum_lakh_crore    REAL,
    aum_crore         REAL,
    num_schemes       INTEGER,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
