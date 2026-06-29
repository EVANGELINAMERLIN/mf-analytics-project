import requests
import pandas as pd
import time

schemes = {
    "SBI Bluechip"     : 119551,
    "ICICI Bluechip"   : 120503,
    "Nippon Large Cap" : 118632,
    "Axis Bluechip"    : 119092,
    "Kotak Bluechip"   : 120841,
}

all_nav = []
for name, code in schemes.items():
    url      = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for record in data["data"]:
            all_nav.append({
                "scheme_code" : code,
                "scheme_name" : name,
                "date"        : record["date"],
                "nav"         : record["nav"]
            })
        print(f"Fetched {name}: {len(data['data'])} records")
    time.sleep(0.5)

df = pd.DataFrame(all_nav)
df.to_csv("data/raw/all_5_schemes_nav.csv", index=False)
print(f"Saved: {len(df)} total records")
