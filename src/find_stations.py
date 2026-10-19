import os
import requests
from dotenv import load_dotenv

load_dotenv()
HEADERS = {"X-API-Key": os.getenv("OPENAQ_API_KEY")}
BASE = "https://api.openaq.org/v3"

r = requests.get(f"{BASE}/locations", headers=HEADERS,
                 params={"iso": "MN", "limit": 1000})
r.raise_for_status()

for loc in r.json()["results"]:
    lat = loc["coordinates"]["latitude"]
    lon = loc["coordinates"]["longitude"]
    if 47.75 < lat < 48.05 and 106.6 < lon < 107.2:
        for s in loc["sensors"]:
            if s["parameter"]["name"] == "pm25":
                print(loc["id"], loc["name"], "| sensor", s["id"],
                      "|", loc["datetimeFirst"], "->", loc["datetimeLast"])