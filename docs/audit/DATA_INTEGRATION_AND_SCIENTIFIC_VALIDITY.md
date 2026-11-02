# UrbanSphere — Data Integration & Scientific Validity Audit

> **Audit Date:** October 2026  
> **Auditor:** Research Data Validator & Big Data Architect  
> **Evaluation Scope:** Multi-domain data merging, join keys, cardinalities, temporal alignment, and methodological validity

---

## 1. Executive Summary of Integration Pipelines

UrbanSphere attempts to integrate five heterogeneous urban domains: **Mobility, Weather, Air Quality, Geography, and Events**.

Our audit of the integration code (spark/preprocessing/data_integration.py), intermediate outputs, and the final integrated dataset (data/processed/integrated/weather_air_quality.csv and .parquet) revealed **three severe methodological and scientific validity flaws**:

1. **Temporal Disconnection (6-Year Temporal Gap):** Attempting to analyze relationships between 2018 traffic surveys and 2024 weather/air quality introduces severe ecological fallacies if joined on timestamps.
2. **Fabricated Spatial Join via Random Sector Assignment:** data_integration.py assigns traffic survey locations to municipal sectors using np.random.choice(sectors) with seed=42. Inventing random spatial linkages is scientifically unacceptable.
3. **Daily-to-Hourly Granularity Distortion & Spatial Blurring:** In weather_air_quality.csv, daily air quality averaged across 4 distant physical stations is broadcast identically to all 24 hours of that day, and the 4 physical stations are collapsed into a single synthetic coordinate point (Lat 28.4335, Lon 77.1036).

---

## 2. Forensic Audit of the Weather <-> Air Quality Integration

### Pipeline Details
- **Script:** spark/preprocessing/data_integration.py
- **Output Files:**
  - Active on disk: data/processed/integrated/weather_air_quality.csv (26,304 rows, 34 columns)
  - Parquet on disk: data/processed/integrated/weather_air_quality.parquet (26,304 rows, 34 columns)
- **Intended Output in Script:** Script attempts to write weather_air_quality_2024.csv, but disk contains weather_air_quality.csv (created by an earlier expansion pipeline).
- **Primary Join Key:** date (YYYY-MM-DD string).
- **Join Type:** Left Outer Join (Hourly Weather -> Daily Air Quality Summary).

### Cardinality & Row Multiplication Audit
- Hourly weather has 24 rows per date.
- Raw air quality has 4 stations per date (in 2024) or 1 virtual point per date (in 2022–2023).
- **Direct Join Risk:** If joined directly on date, 24 weather hours * 4 stations would cause a **4x row multiplication (96 rows per day)**, duplicating meteorological measurements.
- **Implemented Mitigation:** data_integration.py aggregates air quality by date before joining:
  - Takes city mean for PM2.5, PM10, NO2, SO2, CO, O3.
  - Takes city max for AQI.
- **Validation Result:** Row count exactly matches weather (26,304 rows). Zero row explosion occurred.

### Methodological & Scientific Validity Flaws

#### A. Temporal Broadcasting Flaw (Daily AQ to Hourly Weather)
- Each hourly weather record receives the exact same daily mean pollutant value for that calendar date.
- **Scientific Impact:**
  - Air pollution in North India exhibits strong diurnal cycles (morning rush hour spikes at 08:00–10:00, evening boundary layer compression spikes at 20:00–23:00, and afternoon photochemical ozone peaks).
  - Broadcasting a single daily average to all 24 hours destroys this diurnal variation. In statistical regressions or ML models, the model will see 24 identical PM2.5 values against 24 varying temperatures, generating artificial autocorrelation and invalid p-values.

#### B. Spatial Collapse of Monitoring Stations
- In 2024, the 4 CAAQMS stations are geographically distinct:
  - Vikas Sadan (Old Gurgaon dense urban core)
  - Sector 51 IMD (New residential / commercial fringe)
  - Teri Gram & NISE Gwal Pahari (Rural / forested Aravalli foothills)
- In weather_air_quality.csv, their coordinates were averaged into:
  - latitude_aq = 28.4335
  - longitude_aq = 77.1036
- **Scientific Impact:** This coordinate does not represent any physical sensor. Averaging rural background stations (NISE) with urban traffic stations (Vikas Sadan) dilutes localized pollution signals and creates an invented spatial entity.

#### C. Obscured Provenance Tagging
- In weather_air_quality.csv, every non-null air quality row is labeled:
  data_status_aq = 'aggregated_observed_reanalysis'
- **Scientific Impact:** For 2023, the data is 100% CAMS satellite/model reanalysis. For 2024, it is 100% observed ground CAAQMS measurements. Combining them under a single ambiguous label prevents researchers from filtering or differentiating real ground truth from numerical models.

#### D. Time-Zone Desynchronization in Hourly Analysis
- Because 2022–2023 weather timestamps are in UTC, the daily partition date = dt.date in 2022–2023 was computed from UTC timestamps!
- For example, 2022-01-01 19:00 UTC corresponds to 2022-01-02 00:30 IST. The hours from 18:30 to 23:59 IST were assigned to the wrong calendar date!

---

## 3. Forensic Audit of the Traffic <-> Geography Integration

### Pipeline Details
- **Code Inspected:** spark/preprocessing/data_integration.py (lines 60–95)
- **Intended Output:** traffic_geographic_reference.csv

### The Synthetic Random Mapping Vulnerability
In data_integration.py, the following logic was written to map traffic survey locations to municipal sectors:
- Uses np.random.seed(42) and np.random.choice(sectors) to assign a random sector_id to each traffic location.

### Scientific Evaluation:
1. **Invented Spatial Relationships:**
   - Real traffic survey locations (e.g., Kherki Daula Toll Plaza on NH-48 or Subhash Chowk on Sohna Road) have exact, physically verified locations on Gurugram arterial roads.
   - Using random choice assigns these major highway bottlenecks to completely random sectors (e.g., residential Sector 4, fringe Sector 103, or industrial Sector 37).
2. **Academic Repercussions:**
   - Any external reviewer examining this code will immediately reject the spatial traffic analysis as fraudulent or unscientific.
   - **Recommendation:** Permanently purge np.random.choice from the codebase. Map traffic locations to sectors using verified GIS coordinates or arterial corridor references.

---

## 4. Cross-Domain Temporal Compatibility Audit

| Cross-Domain Join | Observation Periods | Temporal Compatibility | Validity Assessment |
|:---|:---:|:---:|:---|
| **Weather <-> Air Quality** | 2024 (Observed) vs. 2024 (Observed) | **Synchronous (1:1 Date)** | **SCIENTIFICALLY VALID.** Real simultaneous measurements. |
| **Weather <-> Air Quality** | 2022–2023 (Reanalysis) vs. 2022–2023 (Reanalysis) | **Synchronous (Model)** | **VALID WITH DOCUMENTED MODEL LIMITATIONS.** |
| **Traffic <-> Weather** | 2018 (Traffic) vs. 2024 (Weather) | **6-Year Gap** | **SCIENTIFICALLY INVALID.** Spurious correlation. |
| **Traffic <-> Air Quality** | 2018 (Traffic) vs. 2024 (AQ) | **6-Year Gap** | **SCIENTIFICALLY INVALID.** Spurious correlation. |
| **Events <-> Any Domain** | Events absent (0 rows) | **N/A** | **IMPOSSIBLE.** Feature unimplemented. |

### Rule of Research Integrity:
> **Never perform a temporal join between 2018 traffic surveys and 2024 environmental time series.**
>
> Gurugram underwent massive infrastructure expansion between 2018 and 2024 (opening of Dwarka Expressway, Southern Peripheral Road expansion, Sohna Elevated Corridor, post-COVID traffic shifts). Implying that 2018 traffic counts explain 2024 air pollution is scientifically indefensible.

---

## 5. Architectural Recommendation: Separate Analytical Datasets

Rather than forcing heterogeneous data into an unscientific single table, UrbanSphere should establish **three separate, defensible analytical datasets**:

1. **DATASET 1: Environmental Time Series (Weather + Air Quality)**
   - Hourly 2024 observations
   - Daily pollutant aggregates
   - Valid cross-domain analytics (meteorology vs. pollution)
2. **DATASET 2: Mobility Corridor Profile (DPR 2018 Surveys)**
   - 15 corridors and intersections
   - Classified vehicle breakdown
   - Capacity, PCU, and speed profiles
3. **DATASET 3: Municipal GIS Reference (Sectors & Corridors)**
   - 123 verified sectors
   - 7 transit corridors
   - 10 administrative zones

This decoupled design is standard big data architecture practice and will satisfy all academic reviewers.
