# UrbanSphere — Data Quality & Statistical Validation Results

> **Audit Date:** October 2026  
> **Auditor:** Senior Data Quality Auditor  
> **Testing Environment:** Python 3.14 / PySpark 4.2.0 / Pandas 3.0.6 / macOS ARM64  
> **Execution Rule:** All metrics calculated from physical files on disk; no estimated numbers.

---

## 1. Executive Summary of Validation Tests

A suite of automated statistical, schema, temporal, and spatial validation tests was executed against all 32 datasets in the UrbanSphere repository.



---

## 2. Parquet vs. CSV Parity Validation

| Dataset | CSV Shape | Parquet Shape | Shape Match | Column Order Match | Discrepancies |
|:---|:---:|:---:|:---:|:---:|:---:|
| `air_quality_cleaned` | (1,979, 21) | (1,979, 21) | **TRUE** | **TRUE** | 0 |
| `weather_cleaned` | (26,304, 22) | (26,304, 22) | **TRUE** | **TRUE** | 0 |
| `weather_air_quality` | (26,304, 34) | (26,304, 34) | **TRUE** | **TRUE** | 0 |
| `traffic_cleaned` | (15, 18) | (15, 18) | **TRUE** | **TRUE** | 0 |
| `vehicle_composition_cleaned` | (112, 9) | (112, 9) | **TRUE** | **TRUE** | 0 |
| `speed_distribution_cleaned` | (8, 12) | (8, 12) | **TRUE** | **TRUE** | 0 |
| `geography_cleaned` | (138, 15) | (138, 15) | **TRUE** | **TRUE** | 0 |

**Finding:** All Parquet files exactly match their CSV counterparts in row count, column count, and schema definitions. Parquet conversion pipeline integrity is validated.

---

## 3. Detailed Data Quality Failure Reports

### TEST DQ-01: Weather Timezone Phase-Shift (Critical Failure — P0)
- **Target File:** `data/processed/weather/weather_cleaned.csv`
- **Why It Matters:** Diurnal environmental analysis requires accurate local time. A 5.5-hour error causes midday heat to appear in the morning, corrupting all solar radiation and human mobility correlations.
- **Test Method:** Evaluated diurnal temperature cycles by calculating average temperature by hour of day for each year.
- **Empirical Evidence:**
  - **Year 2022 (Reanalysis):** Peak temperature occurs at **09:00:00** (Mean: 30.42°C); Minimum at **00:00:00** (Mean: 19.46°C).
  - **Year 2023 (Reanalysis):** Peak temperature occurs at **09:00:00** (Mean: 29.63°C); Minimum at **23:00:00** (Mean: 19.06°C).
  - **Year 2024 (Observed):** Peak temperature occurs at **15:00:00** (Mean: 31.66°C); Minimum at **03:00:00** (Mean: 18.71°C).
- **Physical Ground Truth:** In Gurugram (UTC+5:30), maximum solar heating occurs around 14:00–15:00 local time. 09:00 UTC = 14:30 IST.
- **Root Cause:** 2022–2023 Open-Meteo data was downloaded in UTC and concatenated with 2024 IST without converting timezones.
- **Severity:** **P0 (Critical).**
- **Action Required:** Convert 2022–2023 timestamps from UTC to IST (+5 hours 30 minutes) and realign date/hour indices.

---

### TEST DQ-02: Atmospheric Pressure Incompatibility (Critical Failure — P0)
- **Target File:** `data/processed/weather/weather_cleaned.csv`
- **Why It Matters:** Machine learning and statistical models cannot train on columns where different physical units/variables are merged under a single column name.
- **Test Method:** Grouped `pressure_hpa` by `source_year` and computed summary statistics.
- **Empirical Evidence:**
  - **2022 (Reanalysis):** Mean = 981.74 hPa (Min: 967.6, Max: 997.5 hPa)
  - **2023 (Reanalysis):** Mean = 983.36 hPa (Min: 969.5, Max: 1000.0 hPa)
  - **2024 (Observed):** Mean = 1015.02 hPa (Min: 997.8, Max: 1032.6 hPa)
- **Physical Analysis:** Gurugram sits at an elevation of ~220–240 meters above sea level. Barometric formula dictates surface pressure at 230m is ~985 hPa. The 2022–2023 values are **Surface Pressure**. The 2024 values (~1015 hPa) are **Mean Sea Level Pressure (MSLP)**.
- **Severity:** **P0 (Critical).**
- **Action Required:** Convert 2022–2023 surface pressure to MSLP using the hypsometric equation, or label them as distinct columns (`surface_pressure_hpa` vs. `mslp_hpa`).

---

### TEST DQ-03: Fabricated Observation Flags in Synthetic Traffic (Critical Failure — P0)
- **Target File:** `data/raw/gurugram_traffic_master_consolidated.csv`
- **Why It Matters:** Academic research integrity prohibits labeling synthetic data as authentic observations.
- **Test Method:** Audited unique values of `is_source_observation` and cross-referenced with `generation_note`.
- **Empirical Evidence:**
  - Out of 40,320 rows, **2,880 rows (7.14%) have `is_source_observation: True`**.
  - All 2,880 rows correspond to `survey_date: 2018-01-15`.
  - The `generation_note` on those exact rows reads:
    *"15-min directional slot derived from DPR daily totals using seeded stochastic expansion (seed=42). Seasonal factor=0.90; Day factor=1.00; Variation=1.0418."*
- **Severity:** **P0 (Critical).**
- **Action Required:** Set `is_source_observation: False` across all 40,320 rows and relocate the file from `data/raw/` to `data/benchmark/synthetic/`.

---

### TEST DQ-04: Complete Nullification of Geography Coordinates (Critical Failure — P0)
- **Target File:** `data/processed/geography/geography_cleaned.csv`
- **Why It Matters:** Urban spatial intelligence cannot function without coordinates.
- **Test Method:** Calculated null percentage across all attributes for 138 entities.
- **Empirical Evidence:**
  - `latitude`: **138 nulls (100.0%)**
  - `longitude`: **138 nulls (100.0%)**
  - `administrative_zone`: **138 nulls (100.0%)**
  - `primary_land_use`: **138 nulls (100.0%)**
  - `elevation_meters`: **138 nulls (100.0%)**
  - `pincode`: **138 nulls (100.0%)**
  - `nearest_transit_corridor`: **138 nulls (100.0%)**
- **Severity:** **P0 (Critical).**
- **Action Required:** Restore official coordinates and sector centroids from verified municipal GIS sources.

---

### TEST DQ-05: Schema Fragmentation in Processed Weather (High Failure — P1)
- **Target File:** `data/processed/weather/weather_cleaned.csv`
- **Empirical Evidence:**
  - `humidity_pct`: 17,520 nulls (66.61%) — populated ONLY in 2024.
  - `humidity_percent`: 8,784 nulls (33.39%) — populated ONLY in 2022–2023.
  - `wind_direction`: 17,520 nulls (66.61%) — populated ONLY in 2024.
  - `weather_condition`: 8,784 nulls (33.39%) — populated ONLY in 2022–2023.
  - `station_name`: 8,784 nulls (33.39%) — populated ONLY in 2022–2023.
- **Severity:** **P1 (High).**
- **Action Required:** Coalesce `humidity_pct` and `humidity_percent` into a single `relative_humidity_pct` column.

---

### TEST DQ-06: Missing Time Series in Air Quality Reanalysis (High Failure — P1)
- **Target File:** `data/processed/air_quality/air_quality_cleaned.csv`
- **Empirical Evidence:**
  - For 2022, only 150 days are present (2022-08-04 to 2022-12-31).
  - The first 215 days of 2022 (2022-01-01 to 2022-08-03) were omitted due to null values in CAMS models.
  - In `weather_air_quality.csv`, this causes **5,160 hours (215 days * 24 hrs) to have 100% null air quality values**.
  - All 515 reanalysis records have `aqi: NaN`.
- **Severity:** **P1 (High).**
- **Action Required:** Explicitly document the 215-day gap, calculate synthetic sub-index AQI for reanalysis rows, or restrict integrated analysis to 2024.

---

## 4. Comprehensive Missing Value Audit Table

| Dataset | Total Records | Columns With Null Values | Null Count | Null % | Impact |
|:---|---:|:---|---:|---:|:---|
| `midblock_traffic.csv` | 8 | None | 0 | 0.0% | None |
| `intersection_traffic.csv` | 4 | None | 0 | 0.0% | None |
| `outer_cordon_traffic.csv` | 3 | None | 0 | 0.0% | None |
| `road_speed_distribution.csv` | 8 | `average_journey_speed_peak_kmh` (4), `average_running_speed_peak_kmh` (4) | 8 | 10.0% | Expected (metric split) |
| `Gurgaon_Weather_Dataset_2024` | 8,784 | None | 0 | 0.0% | None |
| `Gurgaon_Air_Quality_Dataset_2024` | 1,464 | None | 0 | 0.0% | None |
| `Gurgaon_Geographical_GIS` | 123 | None | 0 | 0.0% | None |
| `gurugram_traffic_master_consolidated` | 40,320 | None | 0 | 0.0% | None |
| `traffic_cleaned.csv` | 15 | Peak metrics for intersections (`morning_peak_*`, `evening_peak_*`) | 50 | 18.5% | Expected (survey difference) |
| `vehicle_composition_cleaned.csv` | 112 | Derivation columns for intersections | 224 | 22.2% | Expected (derived vs observed) |
| `weather_cleaned.csv` | 26,304 | `humidity_pct` (17,520), `humidity_percent` (8,784), `wind_direction` (17,520), `weather_condition` (8,784) | 122,784 | 21.2% | **Severe Schema Fragmentation** |
| `air_quality_cleaned.csv` | 1,979 | `sector` (515), `aqi` (515), `aqi_category` (515), metadata (2,964) | 5,503 | 13.2% | **Reanalysis AQI Missing** |
| `geography_cleaned.csv` | 138 | 9 spatial/attribute columns * 138 rows | 1,242 | 60.0% | **Total Spatial Loss** |
| `weather_air_quality.csv` | 26,304 | Weather nulls (122,784) + AQ nulls (5,160 * 10) + `aqi` (17,520) + `month_aq` (17,520) | 209,424 | 23.4% | **Severe Cross-Domain Nulls** |
