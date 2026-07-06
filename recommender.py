
"""
recommender.py — Simple Fund Recommender
Bluestock MF Analytics

Usage:
    python recommender.py --risk Moderate
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path

TRADING_DAYS = 252
RF = 0.065
RF_DAILY = RF / TRADING_DAYS

PROC_DIR = Path("data/processed")

RISK_APPETITE_MAP = {
    "Low": ["Low", "Low to Moderate"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"],
}


def load_data():
    fund_master = pd.read_csv(PROC_DIR / "01_fund_master_clean.csv")
    nav = pd.read_csv(PROC_DIR / "02_nav_history_clean.csv", parse_dates=["date"])
    return fund_master, nav


def compute_sharpe_ratios(nav: pd.DataFrame) -> pd.DataFrame:
    nav_sorted = nav.sort_values(["amfi_code", "date"]).copy()
    nav_sorted["daily_return"] = nav_sorted.groupby("amfi_code")["nav"].pct_change()
    returns_df = nav_sorted.dropna(subset=["daily_return"])

    records = []
    for code, grp in returns_df.groupby("amfi_code"):
        mean_daily = grp["daily_return"].mean()
        std_daily = grp["daily_return"].std()
        sharpe = ((mean_daily - RF_DAILY) / std_daily) * np.sqrt(TRADING_DAYS) if std_daily > 0 else np.nan
        records.append({"amfi_code": code, "sharpe_ratio": sharpe})
    return pd.DataFrame(records)


def recommend_funds(risk_appetite: str, fund_risk_sharpe: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    if risk_appetite not in RISK_APPETITE_MAP:
        raise ValueError(f"risk_appetite must be one of {list(RISK_APPETITE_MAP.keys())}")

    matching_categories = RISK_APPETITE_MAP[risk_appetite]
    candidates = fund_risk_sharpe[fund_risk_sharpe["risk_category"].isin(matching_categories)]
    top = candidates.sort_values("sharpe_ratio", ascending=False).head(top_n)
    return top[["scheme_name", "fund_house", "risk_category", "sharpe_ratio"]].reset_index(drop=True)


def main():
    parser = argparse.ArgumentParser(description="Simple Fund Recommender — Bluestock MF Analytics")
    parser.add_argument("--risk", type=str, choices=["Low", "Moderate", "High"], required=True,
                         help="Risk appetite: Low / Moderate / High")
    parser.add_argument("--top_n", type=int, default=3, help="Number of funds to recommend (default 3)")
    args = parser.parse_args()

    fund_master, nav = load_data()
    sharpe_lookup = compute_sharpe_ratios(nav)
    fund_risk_sharpe = fund_master[["amfi_code", "scheme_name", "fund_house", "risk_category"]].merge(
        sharpe_lookup, on="amfi_code"
    )

    recommendations = recommend_funds(args.risk, fund_risk_sharpe, top_n=args.top_n)

    print(f"\n=== Top {args.top_n} Recommended Funds — Risk Appetite: {args.risk} ===")
    print(recommendations.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
