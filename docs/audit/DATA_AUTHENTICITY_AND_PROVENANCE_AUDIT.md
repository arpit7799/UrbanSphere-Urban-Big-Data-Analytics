# UrbanSphere — Data Authenticity & Provenance Audit

> **Audit Date:** October 2026  
> **Auditor:** Research Data Validator & Academic Project Reviewer  
> **Evaluation Framework:** Six-Tier Academic Confidence Hierarchy (Levels A–F)

---

## 1. Provenance Hierarchy & Confidence Classification

Every dataset in UrbanSphere has been evaluated against six rigorous evidence tiers:

- **Level A — Verified against the original source document:** Full provenance chain established; original report tables, page numbers, and authoring authority physically verified.
- **Level B — Verified against an authoritative API or official data portal:** Traceable to verified endpoints, documented query parameters, and authentic agency servers.
- **Level C — Internally consistent but not independently verified:** Valid distributions, reasonable physical ranges, and valid schemas, but original raw API payloads or sensor logs are not present in the repository.
- **Level D — Mathematically derived from documented metadata:** Calculations reproducibly derived from verified Level A/B totals, explicitly documented as derived rather than raw observations.
- **Level E — Unverified because supporting evidence is missing:** Records where origin, instrumentation, or geographic coordinates cannot be corroborated.
- **Level F — Contradicted by available evidence:** Records containing factual contradictions, fabricated observation tags, time-zone offsets, or falsified metadata.

---

## 2. Dataset-by-Dataset Provenance & Authenticity Assessment

### A. Mobility Domain: RITES 2018 Gurugram Metro DPR Survey Tables

| Dataset File | Rows | Level | Issuing Authority & Source Document | Verification Evidence |
|:---|:---:|:---:|:---|:---|
| `data/raw/midblock_traffic.csv` | 8 | **A** | RITES Ltd. / HMRTC (2019 DPR) | Tables 3.3, 2.6, 2.7 (Pages 3-4, 2-5, 2-6) |
| `data/raw/intersection_traffic.csv` | 4 | **A** | RITES Ltd. / HMRTC (2019 DPR) | Tables 3.5, 3.6 (Page 3-5) |
| `data/raw/outer_cordon_traffic.csv` | 3 | **A** | RITES Ltd. / HMRTC (2019 DPR) | Table 3.4 (Page 3-4) |
| `data/raw/road_speed_distribution.csv` | 8 | **A** | RITES Ltd. / HMRTC (2019 DPR) | Tables 3.8, 3.9 (Page 3-7) |
| `data/raw/intersection_vehicle_composition.csv` | 48 | **A** | RITES Ltd. / HMRTC (2019 DPR) | Tables 3.5, 3.6 (Page 3-5) |
| `data/raw/midblock_vehicle_composition_derived.csv` | 64 | **D** | Mathematically reconstructed | Total vehicles * composition %; largest-remainder method |
| `data/raw/air_quality_context.csv` | 9 | **A** | HSPCB / RITES DPR (2019) | Table 2.13 (Page 2-14) |
| `data/raw/citypulse_gurugram_master_long.csv` | 139 | **D** | Long-format normalization | Normalized combination of above tables |

#### Detailed Verification Findings:
1. **Source Document:** *Revised Final Detailed Project Report (DPR) – Metro Rail Connection from HUDA City Centre to Cyber City, Gurugram* (October 2019), prepared by RITES Ltd. for Haryana Mass Rapid Transport Corporation (HMRTC).
2. **Survey Methodology:** Primary traffic surveys conducted by RITES in **2018**:
   - Mid-block screen-line classified volume counts: 16-hour / 24-hour typical weekday surveys.
   - Intersection turning-movement surveys: 16-hour continuous counts (06:00 to 22:00) at 15-minute intervals.
   - Outer-cordon volume counts: Continuous 24-hour counts on arterial borders.
   - Speed & delay surveys: Moving-observer method over 567.3 km of network during peak hours.
3. **Vehicle Categories & PCU Standards:** Follow IRC:106-1990 standards:
   - Car/Jeep/Van = 1.0 PCU, Two-Wheeler = 0.5 PCU, Auto-Rickshaw = 1.0 PCU, Bus = 3.0 PCU, Light Commercial Vehicle = 1.5 PCU, Truck = 3.0 PCU, Cycle/Rickshaw = 0.5 PCU.
4. **Mathematical Consistency:**
   - In `intersection_vehicle_composition.csv`, category percentages sum to 100.01% (INT1), 99.99% (INT2), 100.00% (INT3), 99.99% (INT4) — exact source rounding behavior.
   - In `road_speed_distribution.csv`, road lengths across speed bands sum to 567.30 km for journey speed and 564.60 km for running speed, matching the network length of 567.3 km.
5. **Academic Limitations:**
   - These are **aggregated static survey snapshots from 2018**, NOT a continuous real-time streaming time series.
   - The reconstructed vehicle counts (`*_est_vehicles`) are mathematical estimations from reported percentages and must be explicitly defended as derived representations, not sensor observations.

---

### B. Mobility Domain: Synthetic Consolidated Master Dataset

| Dataset File | Rows | Level | Purported Origin | Actual Finding |
|:---|:---:|:---:|:---|:---|
| `data/raw/gurugram_traffic_master_consolidated.csv` | 40,320 | **F** | "Consolidated Traffic Master" | **Generated via seeded stochastic expansion (`seed=42`). Contains 2,880 rows falsely marked `is_source_observation: True`** |

#### Detailed Verification Findings:
1. **Contradiction with Metadata:**
   - 2,880 records (survey date 2018-01-15) have `is_source_observation: True` and `data_quality_flag: VALID`.
   - However, the `generation_note` column of these exact rows explicitly states:
     *"15-min directional slot derived from DPR daily totals using seeded stochastic expansion (seed=42). Seasonal factor=0.90; Day factor=1.00; Variation=1.0418."*
2. **Fabrication of Temporal Granularity:**
   - The DPR contains 16-hour daily aggregates for intersections and daily totals for midblock locations. It does NOT report direction-wise 15-minute counts for all 96 intervals of the day across 14 dates.
   - The intervals (00:00 to 23:45) and dates (2018-01-15 to 2018-12-10) were generated artificially using mathematical modulation curves and random seeds.
3. **Initial Audit Verdict:** **Level F (Contradicted by Evidence).** Storing this file in `data/raw/` with `is_source_observation: True` posed an unacceptable academic integrity risk.

#### Remediation Status (Step 1 Completed — October 2026):
- **Remediation Action:**
  1. Converted all 2,880 false `is_source_observation = True` rows to `False`. Now 100% of the 40,320 rows (40,320 / 40,320) have `is_source_observation = False`.
  2. Updated `data_quality_flag` to `SYNTHETIC_BENCHMARK` for all 40,320 records.
  3. Created quarantined benchmark copy under `data/benchmark/synthetic/gurugram_traffic_master_consolidated_synthetic.csv` with dedicated `README.md`.
  4. Retained in `data/raw/` with corrected flags and updated documentation in `README_DATASET.md` for pipeline backwards compatibility.
  5. Verified all 6 original RITES 2018 survey files remain 100% intact and bit-for-bit unchanged.
- **Post-Remediation Status:** **Level C (Synthetic Benchmark — Defensible for Scalability / Load Testing Only).** Falsely labelled records remaining: **0**.

---

### C. Weather Domain: 2024 Observational vs. 2022–2024 Reanalysis

| Dataset File | Rows | Level | Source Authority | Provenance Evidence |
|:---|:---:|:---:|:---|:---|
| `data/raw/Gurgaon_Weather_Dataset_2024_Hourly_8784_Rows.csv` | 8,784 | **C** | IMD / Gurugram Local Station (2024) | Continuous 8,784 hourly sequence, realistic physical bounds |
| `data/processed/weather/weather_cleaned.csv` (2024 portion) | 8,784 | **C** | Cleaned version of raw 2024 | Exact 1:1 match with raw 2024 |
| `data/processed/weather/weather_cleaned.csv` (2022–2023 portion) | 17,520 | **F** | Open-Meteo Historical Weather API | **UTC timestamps merged into IST without conversion; MSLP vs Surface pressure jump** |

#### Detailed Verification Findings:
1. **Raw 2024 Weather:**
   - 8,784 hours covering all 366 days of 2024 (leap year).
   - Zero duplicate timestamps; zero missing hours.
   - Realistic Gurugram meteorological behavior: Winter lows 2.0°C (January), summer highs 47.8°C (June heatwaves), monsoon precipitation peaks (July/August).
   - **Limitation:** The raw source download script and API query parameters are missing from the repository.
2. **2022–2023 Open-Meteo Reanalysis Data:**
   - **Missing Raw Files:** There is NO raw CSV or JSON in `data/raw/` for 2022 or 2023 weather. It appeared in `data/processed/` via an uncommitted or deleted script (`real_expansion.py`).
   - **Timezone Mismatch (UTC vs. IST):**
     - Diurnal temperature cycle analysis reveals that in 2022 and 2023, the peak daily temperature occurs at **09:00:00**. In Gurugram (IST = UTC+5:30), maximum solar heating occurs around 14:00–15:00. 09:00 UTC corresponds to 14:30 IST.
     - In 2024, the peak temperature occurs at **15:00:00 IST**.
     - **Conclusion:** 2022 and 2023 are in UTC, while 2024 is in IST. They are phase-shifted by 5.5 hours.
   - **Pressure Discontinuity:**
     - 2022 mean pressure = 981.7 hPa; 2023 mean pressure = 983.4 hPa (true surface pressure at ~230m altitude).
     - 2024 mean pressure = 1015.0 hPa (mean sea level pressure, MSLP).
     - Concatenating them into a single column `pressure_hpa` creates a spurious 33 hPa jump on January 1, 2024.

---

### D. Air Quality Domain: 2024 CAAQMS Stations vs. CAMS Reanalysis

| Dataset File | Rows | Level | Source Authority | Provenance Evidence |
|:---|:---:|:---:|:---|:---|
| `data/raw/Gurgaon_Air_Quality_Dataset_2024_1464_Records.csv` | 1,464 | **C** | CPCB / HSPCB CAAQMS Network | 4 verified official stations, CPCB NAQI math |
| `data/processed/air_quality/air_quality_cleaned.csv` (2024) | 1,464 | **C** | Cleaned version of 2024 | Exact match with raw |
| `data/processed/air_quality/air_quality_cleaned.csv` (2022–2023) | 515 | **E** | Open-Meteo CAMS Air Quality API | 215 days missing in 2022; AQI is 100% NULL |

#### Detailed Verification Findings:
1. **Station Verification (2024):**
   - `IND_HR_GGN_01`: Vikas Sadan, Sector 11 (Lat 28.4554, Lon 77.0329) — Official CPCB station.
   - `IND_HR_GGN_02`: Sector 51 IMD (Lat 28.4283, Lon 77.0722) — Official CPCB station.
   - `IND_HR_GGN_03`: Teri Gram, Gwal Pahari (Lat 28.4288, Lon 77.1511) — Official CPCB station.
   - `IND_HR_GGN_04`: NISE Gwal Pahari (Lat 28.4215, Lon 77.1582) — Official CPCB station.
   - All 4 stations are physically real, operational CAAQMS installations in Gurugram.
2. **AQI Calculation Verification:**
   - `aqi_calculated` matches CPCB National Air Quality Index (NAQI) breakpoints and formulas. PM2.5 of 12.0 µg/m³ correctly yields an AQI of 20 (Good category).
3. **Data Quality Nuance:**
   - Exactly 366 records per station (100% complete) with 0 nulls across all 6 pollutants. Real-world CPCB stations experience 5–15% sensor downtime. This data was likely pre-interpolated before archiving.
4. **2022–2023 Reanalysis Limitations:**
   - Only 150 days exist for 2022 (Aug 4 to Dec 31). The first 215 days of 2022 were omitted due to null values in CAMS model outputs.
   - Lacks AQI calculation (`aqi: NaN` for all 515 rows).

---

### E. Geography Domain: Municipal Sectors & Reference Entities

| Dataset File | Rows | Level | Purported Origin | Actual Finding |
|:---|:---:|:---:|:---|:---|
| `data/raw/Gurgaon_Geographical_GIS_Dataset_123_Sectors.csv` | 123 | **E** | "Gurgaon GIS Dataset" | Approximate sector centroids; unverified municipal source |
| `data/processed/geography/geography_cleaned.csv` | 138 | **F** | Processed GIS Reference | **100% of spatial coordinates (lat/lon) are NULL** |
| `transit_corridors_reference_derived.csv` | 7 | **D** | Derived spatial aggregation | Aggregated from raw GIS before coordinate nullification |
| `zones_reference_derived.csv` | 10 | **D** | Derived spatial aggregation | Aggregated from raw GIS before coordinate nullification |

#### Detailed Verification Findings:
1. **Raw Sector Centroids (123 Sectors):**
   - Covers Sector 1 to Sector 123. Bounding box (Lat 28.3420–28.5076, Lon 76.9241–77.1511) falls within Gurugram municipal boundaries.
   - However, no official GMDA (Gurugram Metropolitan Development Authority) GIS shapefile, OpenStreetMap relation ID, or Survey of India reference is cited.
2. **Cleaned Geography Catastrophe:**
   - In `data/processed/geography/geography_cleaned.csv`, **all 138 rows have `latitude: NaN`, `longitude: NaN`, `administrative_zone: NaN`, `elevation_meters: NaN`, `pincode: NaN`**.
   - The file was stripped of all geospatial values, rendering it completely incapable of supporting spatial joins, distance calculations, or GIS mapping.

---

### F. Events Domain: Complete Nonexistence

| Dataset File | Records | Level | Finding |
|:---|:---:|:---:|:---|
| (Any event file) | **0** | **N/A** | **NO EVENT DATASET EXISTS IN THE ENTIRE REPOSITORY.** |

#### Verification Evidence:
- Comprehensive repository search across all directories reveals **zero CSV, JSON, Parquet, or Excel files** containing event observations, event names, dates, or festival records.
- Event features described in `README.md` (e.g., `event_indicator`, `event_type`) are purely aspirational architecture stubs.

---

## 3. What Could NOT Be Independently Verified

1. **Original Raw API Response Payloads:**
   - Raw Open-Meteo JSON responses for 2022–2023 weather and 2022–2023 air quality are absent.
2. **Original CPCB Raw Station Downloads:**
   - Raw hourly station readings from CPCB (which are aggregated to 24-hr averages) are absent.
3. **Official GMDA GIS Polygon Boundaries:**
   - No shapefiles, GeoJSON boundaries, or official surveyor records exist to verify sector centroid coordinates.
