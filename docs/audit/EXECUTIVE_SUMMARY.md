# UrbanSphere Data Platform — Comprehensive Audit: Executive Summary

**Project:** UrbanSphere — Urban Big Data Analytics Platform for Gurugram  
**Author / Investigator:** Academic Review & Data Quality Audit Team  
**Evaluation Role:** Senior Data Engineer, Big Data Architect, Data Quality Auditor, Research Data Validator  
**Date of Audit:** October 2026  
**Audit Scope:** Entire repository (`data/`, `hadoop/`, `spark/`, `docs/`, `analytics/`, `backend/`, `frontend/`)  
**Audit Mode:** Read-Only Forensic Inspection & Quantitative Validation  

---

## 1. Overall Project Data-Readiness Verdict

### **VERDICT: PARTIALLY SUITABLE; MATERIAL GAPS AND CRITICAL PROVENANCE CONCERNS REMAIN**

The UrbanSphere repository contains a mixture of **highly authentic municipal engineering survey data**, **real but severely misaligned meteorological and environmental time-series**, **synthetic data falsely tagged as authentic observations**, and **completely missing domains**.

While the project has a well-conceived architecture and strong academic alignment on paper (CSE 3712), **it cannot currently be defended in its present state before an independent technical evaluator or viva committee** without immediate remediation of five critical integrity flaws.

| Data Domain | Records | Integrity Status | Academic Suitability |
|:---|:---:|:---:|:---|
| 🚗 **Mobility (DPR 2018)** | 15 locations / 112 comp / 8 speed | **VERIFIED (Levels A & D)** | Excellent for corridor/intersection static profiling |
| 🚗 **Mobility (Consolidated Master)** | 40,320 records | **COMPROMISED (Level F)** | Unusable as real observations (fabricated observation tags) |
| 🌦️ **Weather (2024 Raw)** | 8,784 hourly rows | **VERIFIED (Level C)** | High quality for 2024 environmental analysis |
| 🌦️ **Weather (2022–2024 Processed)** | 26,304 hourly rows | **FLAWED (Level F)** | 5.5-hr UTC/IST timezone shift; MSLP vs Surface pressure jump |
| 🌫️ **Air Quality (2024 Observed)** | 1,464 station-day rows | **VERIFIED (Level C)** | Authentic 4 CPCB CAAQMS stations, complete 2024 coverage |
| 🌫️ **Air Quality (2022–2023 Reanalysis)** | 515 day rows | **INCOMPLETE (Level C/E)** | Lacks AQI; missing 215 days of 2022; single virtual point |
| 🗺️ **Geography (123 Sectors Raw)** | 123 sectors | **UNVERIFIED (Level E)** | Approximate centroids; unverified municipal sources |
| 🗺️ **Geography (138 Entities Cleaned)** | 138 entities | **UNUSABLE (Level F)** | **100% of coordinates, zones, elevations are NULL** |
| 🎫 **Events** | 0 records | **MISSING (N/A)** | Completely absent from repository |
| 🔗 **Integrated Weather–Air Quality** | 26,304 hourly rows | **METHODOLOGICAL RISK** | Daily AQ broadcast to hours; stations averaged to single point |

---

## 2. Most Trustworthy Datasets (And Why)

1. **RITES 2018 Gurugram Metro DPR Survey Tables** (`data/raw/midblock_traffic.csv`, `intersection_traffic.csv`, `outer_cordon_traffic.csv`, `road_speed_distribution.csv`):
   - **Provenance Level A**: Directly traceable to printed tables in the official *Revised Final DPR – Metro Rail Connection from HUDA City Centre to Cyber City, Gurugram* (October 2019), authored by RITES Ltd. for HMRTC.
   - **Internal Consistency**: 100% mathematically consistent. Composition percentages sum to ~100.0% across all locations; speed band road lengths sum exactly to 567.3 km; PCU factors adhere to IRC standards.
   - **Limitation**: Represents a cross-sectional 2018 snapshot (16-hour and peak counts), **not a continuous time series**.

2. **2024 Observational Air Quality Dataset** (`data/raw/Gurgaon_Air_Quality_Dataset_2024_1464_Records.csv`):
   - **Provenance Level C**: Exactly represents the 4 official CPCB / HSPCB Continuous Ambient Air Quality Monitoring Stations (CAAQMS) in Gurugram: Vikas Sadan (Sec 11), Sector 51 IMD, Teri Gram, and NISE Gwal Pahari.
   - **Internal Consistency**: Sub-index calculations for PM2.5 and PM10 follow CPCB NAQI regulatory standards with zero negative or physically impossible values.

3. **2024 Hourly Weather Dataset** (`data/raw/Gurgaon_Weather_Dataset_2024_Hourly_8784_Rows.csv`):
   - **Provenance Level C**: Full 366-day leap-year coverage (8,784 consecutive hours) with zero timestamp duplicates, zero missing hours, and physically realistic ranges for Gurugram (temperature 2.0°C to 47.8°C; relative humidity 12% to 98%).

---

## 3. Datasets That Are Internally Consistent But Not Independently Verified

1. **2024 Air Quality Station Observations** (1,464 records):
   - While station names, coordinates, and seasonal trends (monsoon drop to 12.0 µg/m³, winter spikes >500 µg/m³) are plausible, the raw dataset exhibits an unusual property: **zero missing values across 366 days for all 6 pollutants**. Real CAAQMS sensors experience periodic maintenance downtime and transmission dropouts. The data has likely undergone prior imputation or cleaning before landing in the repository.
2. **Derived Vehicle Composition Counts** (`data/raw/midblock_vehicle_composition_derived.csv`):
   - Mathematically reconstructed from total vehicles and percentage compositions using the largest-remainder method. Correctly documented as derived, but not direct sensor counts.

---

## 4. Datasets with Material Accuracy or Provenance Concerns

### 🚨 Critical Concern 1: Fabricated Source Flags in Synthetic Traffic Master
- **File:** `data/raw/gurugram_traffic_master_consolidated.csv` (40,320 rows, 19.5 MB)
- **Finding:** Generated via seeded stochastic expansion (`seed=42`) from 15 DPR daily totals across 14 dates. However, **2,880 records (survey date 2018-01-15) have `is_source_observation: True`** and `data_quality_flag: VALID`.
- **Academic Risk:** Severe. A reviewer examining raw data will conclude the project fabricated 15-minute directional traffic records and disguised them as authentic field observations.

### 🚨 Critical Concern 2: 5.5-Hour UTC vs. IST Timezone Shift in Weather
- **File:** `data/processed/weather/weather_cleaned.csv` (26,304 rows)
- **Finding:** When 2022–2023 Open-Meteo reanalysis data (17,520 hours) was merged with 2024 observed weather (8,784 hours), the UTC timestamps from Open-Meteo were concatenated directly without shifting +5:30 to Indian Standard Time (IST).
- **Hard Evidence:**
  - In 2022 and 2023, the daily peak temperature occurs at **09:00:00** (9:00 AM UTC = 14:30 IST).
  - In 2024, the daily peak temperature occurs at **15:00:00** (3:00 PM IST).
- **Academic Risk:** Any diurnal correlation with traffic, air quality, or human activity in 2022–2023 is off by 5.5 hours.

### 🚨 Critical Concern 3: Incompatible Pressure Variables
- **File:** `data/processed/weather/weather_cleaned.csv`
- **Finding:** 2022–2023 pressure averages **982.5 hPa** (Surface Atmospheric Pressure at ~230m elevation), whereas 2024 pressure averages **1015.0 hPa** (Mean Sea Level Pressure, MSLP). Both are placed in `pressure_hpa`, creating an artificial 32.5 hPa step jump on 2024-01-01.

### 🚨 Critical Concern 4: Total Coordinate Nullification in Geography
- **File:** `data/processed/geography/geography_cleaned.csv` (138 entities)
- **Finding:** **100% of latitude, longitude, administrative zone, land use, elevation, and pincode fields are NULL.**
- **Academic Risk:** The project claims spatial intelligence, GIS mapping, and spatial clustering, but the cleaned spatial dataset contains zero spatial coordinates.

---

## 5. Missing Datasets

1. **Events Dataset:**
   - **Status:** **0 records exist anywhere in the repository.**
   - No CSV, no Parquet, no JSON, no ingestion script.
   - The roadmap and research questions claim multi-domain integration including events, but this is currently vaporware.
2. **Raw Open-Meteo Source Files:**
   - Raw downloads for 2022–2023 weather (17,520 rows) and 2022–2023 air quality reanalysis (515 rows) are completely missing from `data/raw/`. They exist only as processed artifacts.

---

## 6. Most Important Scientific-Validity Risks

1. **Spurious Cross-Domain Joining:**
   - Attempting to correlate 2018 DPR traffic observations with 2024 weather or air quality implies contemporaneous causality when a 6-year temporal gap exists.
2. **Synthetic Random Spatial Joins:**
   - `spark/preprocessing/data_integration.py` assigns traffic survey locations to geographic sectors using `np.random.choice(sectors)` with `seed=42`. Inventing random spatial mappings invalidates any spatial traffic analysis.
3. **Temporal Granularity Mismatch in Integrated Weather-AQ:**
   - Daily air quality (averaged across 4 stations) is broadcast identically across all 24 hours of that day's weather. This obscures diurnal pollution spikes (rush hour, temperature inversions) and creates repeated collinear values.

---

## 7. Demonstration and Academic Evaluation Readiness

- **Ready for Demonstration?** **NO.** The frontend, backend, analytics scripts, and MapReduce jobs are empty stubs.
- **Ready for Academic Evaluation?** **NO.** If audited today, an external examiner will uncover the fabricated `is_source_observation: True` flags, the 5.5-hour timezone discrepancy, the 100% null geography coordinates, and the complete absence of event data.

---

## 8. The Five Most Important Actions to Take Next (Priority Remediation)

| Priority | Action | Target Component | Rationale |
|:---:|---|---|---|
| **1** | **Relabel & Quarantine Synthetic Traffic** | `data/raw/gurugram_traffic_master_consolidated.csv` | Move to `data/benchmark/synthetic/` and set `is_source_observation: False` on all generated rows to eliminate academic misconduct risk. |
| **2** | **Correct Weather Timezone & Pressure Discontinuities** | `data/processed/weather/` | Shift 2022–2023 UTC timestamps by +5:30 to IST, harmonize pressure to MSLP, and unify `humidity_pct` / `humidity_percent`. |
| **3** | **Restore Verified Spatial Coordinates** | `data/processed/geography/` | Repopulate official sector centroids and station coordinates from verified municipal GIS sources to enable spatial queries. |
| **4** | **Re-scope Research Objectives & Scope Out Events** | `README.md`, `docs/architecture.md` | Explicitly state that events are future scope; remove false claims of event correlation; formally separate 2018 traffic profiling from 2022–2024 environmental time series. |
| **5** | **Fix Broken Pipelines & Implement Actual PySpark/MapReduce Jobs** | `spark/preprocessing/`, `hadoop/mapreduce/` | Fix `data_cleaning.py` path bugs (`DATA_DIR / "raw"`), convert scripts to true PySpark DataFrames, and write working MapReduce jobs. |
