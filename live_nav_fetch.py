"""
<<<<<<< HEAD
live_nav_fetch.py — Day 1: Fetch live NAV data from mfapi.in

NOTE: The AMFI codes referenced in the original assignment brief
(125497, 119551, 120503, 118632, 119092, 120841) match fund_master.csv
internally, but only 118632 currently resolves to the expected fund
on the live mfapi.in registry. See reports/live_nav_code_validation_findings.txt
for full details. This script fetches whatever scheme_name the API
actually returns for each code, rather than assuming it matches.
=======
live_nav_fetch.py - Day 1: Fetch live NAV data from mfapi.in
>>>>>>> 0fe473c9a31a89642ef5800269374a54a61aef6a
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
<<<<<<< HEAD

=======
>>>>>>> 0fe473c9a31a89642ef5800269374a54a61aef6a
    meta = payload.get("meta", {})
    df = pd.DataFrame(payload.get("data", []))
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"] = pd.to_numeric(df["nav"])
    df["amfi_code"] = scheme_code
    df["scheme_name"] = meta.get("scheme_name")
    df["fund_house"] = meta.get("fund_house")
<<<<<<< HEAD

=======
>>>>>>> 0fe473c9a31a89642ef5800269374a54a61aef6a
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
