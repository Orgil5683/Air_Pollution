**English** · [Монгол](README.md)

# Breathing Ulaanbaatar: 9 Years of PM2.5 Data

An analysis of Ulaanbaatar's air pollution using real sensor data from the [OpenAQ API](https://openaq.org). It looks at seasons, the May 2019 raw coal ban, differences between districts, and how many days are unhealthy to breathe.

> **Bottom line: better, not safe.** Winters were about 30% cleaner after the 2019 coal ban, but PM2.5 still sits far above the WHO guideline on most days.

## Key terms

| Term | Meaning |
|---|---|
| **PM2.5** | Fine smoke and dust particles 2.5 micrometers or smaller. They reach deep into the lungs. |
| **µg/m³** | Micrograms of particles per cubic meter of air |
| **WHO guideline** | 15 µg/m³ for a 24-hour average (WHO, 2021) |
| **Mongolian standard** | 50 µg/m³ for a 24-hour average (MNS 4585:2016) |

## Questions

1. **Seasons:** How much worse is winter than summer?
2. **Coal ban:** Were winters cleaner after the May 2019 raw coal ban?
3. **Districts:** Which parts of the city had the dirtiest air?
4. **Health:** How many days a year is the air unhealthy?

## Findings

### 1. Winter air is about 8x dirtier than summer

December and January average **154 µg/m³** (about 10x the WHO guideline). May to September averages **18.5**.

![Average PM2.5 by month](figures/monthly_pm25.png)

### 2. Winters were about 30% cleaner after the coal ban

| Period | Winters | Average winter PM2.5 (Dec to Feb) |
|---|---|---|
| Before the ban | 2016-17, 2018-19 | **176.4** |
| After the ban | 2019-20 to 2024-25 (5 winters) | **123.7** |

Every winter after the ban was lower than both winters before it. This points the same direction as a published study that found winter PM2.5 about 44% lower in 2019-20 at a central Ulaanbaatar station.

![Average winter PM2.5 before and after the coal ban](figures/winter_coal_ban.png)

**This shows a link, not proof of cause.** Other factors may explain part of the drop:
- Only 2 usable winters before the ban
- Weather (colder winters mean more burning and stronger temperature inversions)
- COVID-19 lockdowns in 2020-21
- One station only

### 3. Some districts had 3x dirtier winter air

On the 221 days when all 8 stations reported, winter PM2.5 ranged from **107** (Bukhiin urguu) to **320** (Bayankhoshuu). In summer, 7 of 8 stations sat between 17 and 23. The big winter spread points to local heating sources rather than city-wide traffic.

![PM2.5 by station, winter vs summer](figures/stations_winter_summer.png)

### 4. Most days are unhealthy, every year

| Year | Days above WHO (15) | Days above MNS (50) | Worst day |
|---|---|---|---|
| 2018 | 72% | 34% | 366 |
| 2019 | 76% | 38% | 472 |
| 2020 | 68% | 28% | 285 |
| 2024 | 61% | 29% | 270 |

Even in 2024, the cleanest year, **3 in 5 days** were above the WHO guideline.

![Share of unhealthy days per year](figures/unhealthy_days.png)

## Data

| Group | Stations | Years | Used for |
|---|---|---|---|
| A | US Embassy (one monitor, renamed on OpenAQ in Nov 2016) | 2016 to 2025 | Seasons, coal ban, health |
| B | 7 government stations: MNB, Amgalan, Bukhiin urguu, Baruun 4 zam, Nisekh, Tolgoit, Bayankhoshuu | 2016 to 2019 | District comparison |
| C | Bumbugur | Nov 2025 to now | Latest winter (preview only) |

Daily averages were downloaded from the OpenAQ v3 `/sensors/{id}/days` endpoint: **10,174 daily rows**.

## Data quality rules

1. **Complete days only:** keep days with at least 75% of hourly readings (10,174 to 7,597 rows).
2. **Complete winters only:** a winter counts only if Dec, Jan and Feb each have 15+ good days. Winters 2017-18 and 2022-23 were dropped.
3. **Suspect period removed:** US Embassy readings from March to October 2021 were 3 to 4 times higher than the same months in every other year, while the surrounding winter months looked normal. This suggests a sensor problem, so these 164 days were removed (7,433 rows left).

## Open questions

- Add daily temperature data to test how much of the post-ban drop is weather
- Use hourly data to find the worst hours of the day
- Bumbugur averaged 49 µg/m³ in Dec 2025 to Feb 2026, but it is a different sensor in a different place, so it is not directly comparable
- Bayankhoshuu was about 2x the other stations even in summer. Dust, roads, or industry?

## Project structure

```
Air_Pollution/
├── src/
│   ├── find_stations.py      # find PM2.5 sensors in Ulaanbaatar
│   └── download_daily.py     # download daily averages to data/
├── notebooks/
│   └── 01_clean_explore.ipynb  # cleaning, analysis, charts
├── data/                     # raw and cleaned CSVs
├── figures/                  # saved charts
└── requirements.txt
```

## How to run

1. Get a free API key at [explore.openaq.org](https://explore.openaq.org).
2. Create a `.env` file in the project folder (it is ignored by git):
   ```
   OPENAQ_API_KEY=your-key-here
   ```
3. Set up Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run the scripts, then open the notebook:
   ```bash
   python src/find_stations.py
   python src/download_daily.py
   ```
   Open `notebooks/01_clean_explore.ipynb` and click **Run All**.

## Sources

- [OpenAQ API v3 documentation](https://docs.openaq.org)
- WHO Global Air Quality Guidelines (2021)
- [Mongolia Standard MNS 4585:2016 (UNEP LEAP)](https://leap.unep.org/en/countries/mn/national-legislation/mongolia-standard-mns-45852016)
- [Particulate matter concentrations during winter seasons of 2016-2020 in Ulaanbaatar, Mongolia (Proceedings of the Mongolian Academy of Sciences)](https://www.mongoliajol.info/index.php/PMAS/article/view/1559)

---
Made by Orgil as a project for AI Academy.
