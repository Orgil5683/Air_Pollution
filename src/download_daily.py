import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
HEADERS = {"X-API-Key": os.getenv("OPENAQ_API_KEY")}
BASE = "https://api.openaq.org/v3"

# sensor_id: (station name, group)
SENSORS = {
    4686: ("US Embassy", "A"),
    23753: ("US Embassy", "A"),
    5139: ("MNB", "B"),
    42: ("Amgalan", "B"),
    1446: ("Bukhiin urguu", "B"),
    69: ("Baruun 4 zam", "B"),
    1507: ("Nisekh", "B"),
    5118: ("Tolgoit", "B"),
    4727: ("Bayankhoshuu", "B"),
    14549786: ("Bumbugur", "C"),
}

def get_days(sensor_id):
    rows, page = [], 1
    while True:
        r = requests.get(f"{BASE}/sensors/{sensor_id}/days", headers=HEADERS,
                         params={"date_from": "2016-01-01", "date_to": "2026-10-19",
                                 "limit": 1000, "page": page})
        if r.status_code == 429:          # rate limited: wait, then retry
            print("  Rate limited, waiting 60s...")
            time.sleep(60)
            continue
        r.raise_for_status()
        results = r.json()["results"]
        if not results:
            break
        for d in results:
            rows.append({
                "date": d["period"]["datetimeFrom"]["local"][:10],  # YYYY-MM-DD
                "pm25": d["value"],
                "coverage": (d.get("coverage") or {}).get("percentCoverage"),
            })
        page += 1
        time.sleep(1)
    return rows

all_rows = []
for sensor_id, (station, group) in SENSORS.items():
    print(f"Downloading {station} (sensor {sensor_id})...")
    for row in get_days(sensor_id):
        row.update({"station": station, "group": group, "sensor_id": sensor_id})
        all_rows.append(row)

df = pd.DataFrame(all_rows)
df.to_csv("data/ub_pm25_daily.csv", index=False)

print("\nSaved", len(df), "rows to data/ub_pm25_daily.csv")
print(df.groupby("station")["date"].agg(["min", "max", "count"]))