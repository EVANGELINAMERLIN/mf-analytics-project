import os
import pandas as pd

# Create folders
folders = [
    "data/raw", "data/processed",
    "notebooks", "sql",
    "dashboard", "reports"
]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

RAW_DIR = "data/raw"

DATASETS = {
    "fund_master"        : f"{RAW_DIR}/01_fund_master.csv",
    "nav_history"        : f"{RAW_DIR}/02_nav_history.csv",
    "aum_by_fund_house"  : f"{RAW_DIR}/03_aum_by_fund_house.csv",
    "scheme_returns"     : f"{RAW_DIR}/04_scheme_returns.csv",
    "risk_metrics"       : f"{RAW_DIR}/05_risk_metrics.csv",
    "fund_manager"       : f"{RAW_DIR}/06_fund_manager.csv",
    "portfolio_holdings" : f"{RAW_DIR}/07_portfolio_holdings.csv",
    "investor_data"      : f"{RAW_DIR}/08_investor_data.csv",
    "benchmark_index"    : f"{RAW_DIR}/09_benchmark_index.csv",
    "expense_ratio"      : f"{RAW_DIR}/10_expense_ratio.csv",
}

dataframes = {}
for name, path in DATASETS.items():
    if os.path.exists(path):
        df = pd.read_csv(path)
        dataframes[name] = df
        print(f"Loaded {name}: {df.shape}")
    else:
        print(f"Not found: {path}")

