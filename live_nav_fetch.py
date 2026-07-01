"""
live_nav_fetch.py - Day 1: Fetch live NAV data from mfapi.in
"""
import pandas as pd
import requests
import os

KEY_SCHEME_CODES = [125497, 119551, 120503, 118632, 119092, 120841]

def fetch_mfapi_nav(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    meta = payload.get("meta", {})
    df = pd.DataFrame(payload.get("data", []))
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"] = pd.to_numeric(df["nav"])
    df["amfi_code"] = scheme_code
    df["scheme_name"] = meta.get("scheme_name")
    df["fund_house"] = meta.get("fund_house")
    return df.sort_values("date").reset_index(drop=True), meta

def fetch_all(out_dir="data/raw"):
    os.makedirs(out_dir, exist_ok=True)
    frames = []
    for code in KEY_SCHEME_CODES:
        df, meta = fetch_mfapi_nav(code)
        df.to_csv(os.path.join(out_dir, f"live_nav_{code}.csv"), index=False)
        frames.append(df)
        print(f"Fetched {code}: {meta.get('scheme_name')} ({len(df)} rows)")
    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(os.path.join(out_dir, "live_nav_key_schemes_combined.csv"), index=False)
    return combined

if __name__ == "__main__":
    fetch_all()
