"""
data_ingestion.py - Day 1: Load and validate all static CSV datasets.
"""
import pandas as pd
import os

RAW_DIR = "data/raw"
FILE_MAP = {
    "fund_master": "01_fund_master.csv",
    "nav_history": "02_nav_history.csv",
    "aum_by_fund_house": "03_aum_by_fund_house.csv",
    "monthly_sip_inflows": "04_monthly_sip_inflows.csv",
    "category_inflows": "05_category_inflows.csv",
    "industry_folio_count": "06_industry_folio_count.csv",
    "scheme_performance": "07_scheme_performance.csv",
    "investor_transactions": "08_investor_transactions.csv",
    "portfolio_holdings": "09_portfolio_holdings.csv",
    "benchmark_indices": "10_benchmark_indices.csv",
}

def load_all_datasets(raw_dir=RAW_DIR):
    dfs = {}
    for name, fname in FILE_MAP.items():
        dfs[name] = pd.read_csv(os.path.join(raw_dir, fname))
    return dfs

def validate_amfi_codes(dfs):
    fm_codes = set(dfs["fund_master"]["amfi_code"].unique())
    nav_codes = set(dfs["nav_history"]["amfi_code"].unique())
    return {
        "fund_master_count": len(fm_codes),
        "nav_history_count": len(nav_codes),
        "missing_in_nav": sorted(fm_codes - nav_codes),
        "missing_in_master": sorted(nav_codes - fm_codes),
    }

if __name__ == "__main__":
    dfs = load_all_datasets()
    for name, df in dfs.items():
        print(f"{name}: {df.shape}")
    print(validate_amfi_codes(dfs))
