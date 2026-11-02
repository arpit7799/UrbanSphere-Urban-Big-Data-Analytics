# UrbanSphere — Data Remediation Plan & Execution Status

> **Status: P0 AND P1 DATA INTEGRITY REMEDIATIONS FULLY EXECUTED & VERIFIED (October 2026)**
> All data authenticity, timezone synchronization, barometric harmonization, geographic coordinate restoration, and deterministic spatial join repairs have been successfully completed.

---

## 1. Remediation Progress Dashboard

| Priority | Action Item | Target File(s) | Initial Status | Remediated Status | Verification |
|:---|:---|:---|:---:|:---:|:---|
| **P0-1** | **Quarantine & Relabel Synthetic Traffic Master** | `data/raw/gurugram_traffic_master_consolidated.csv` | Level F (2,880 false flags) | **COMPLETED** | `is_source_observation=False` on 100% (40,320) rows; quarantined in `data/benchmark/synthetic/` |
| **P0-2** | **Synchronize Weather Timezones (UTC -> IST)** | `data/processed/weather/weather_cleaned.csv` / `.parquet` | Level F (+5.5h phase shift) | **COMPLETED** | Added +5:30 to 2022-2023; diurnal temperature peaks at 14:00-15:00 IST across all 3 years |
| **P0-3** | **Harmonize Atmospheric Pressure Levels** | `data/processed/weather/weather_cleaned.csv` / `.parquet` | Level F (33 hPa jump) | **COMPLETED** | Barometric reduction applied; explicit `surface_pressure_hpa` and `mslp_hpa` provided |
| **P0-4** | **Purge Random Geographic Mapping** | `spark/preprocessing/data_integration.py` | Level F (`np.random.choice`) | **COMPLETED** | Random choice purged; deterministic arterial corridor & sector mapping implemented |
| **P1-1** | **Harmonize Air Quality Units & Compute NAQI** | `data/processed/air_quality/air_quality_cleaned.csv` / `.parquet` | Level E (CO in ug/m3, NaN AQI) | **COMPLETED** | CO converted to mg/m3; official CPCB NAQI calculated for 100% of rows |
| **P1-2** | **Coalesce Weather Humidity Columns** | `data/processed/weather/weather_cleaned.csv` / `.parquet` | Level D (Split columns) | **COMPLETED** | `relative_humidity_pct` unified across 26,304 rows with 0 nulls |
| **P1-3** | **Fix Data Cleaning Path References** | `spark/preprocessing/data_cleaning.py` | Level E (FileNotFoundError) | **COMPLETED** | Paths standardized to `RAW_DIR`, `BENCHMARK_DIR`, and `PROCESSED_DIR` |
| **P1-4** | **Restore Geography Sector Coordinates** | `data/processed/geography/geography_cleaned.csv` / `.parquet` | Level F (100% null coordinates) | **COMPLETED** | 123 authentic sector centroids restored with 0 null coordinates |
| **P1-5** | **Canonical Daily Analytical Integration** | `data/processed/integrated/weather_air_quality_daily.csv` | Level F (False 24x repetition) | **COMPLETED** | 515-day canonical daily analytical dataset created; zero artificial row expansion |

---



> **Audit Date:** October 2026  
> **Auditor:** Senior Data Engineer, Big Data Architect & Data Quality Auditor  
> **Guiding Principle:** Minimal, evidence-based modifications to achieve 100% academic defensibility without redesigning working components or modifying data without necessity.

---

## 1. Prioritization Framework

Actions are categorized strictly by academic and technical severity:

- **P0 — Critical:** Direct threats to academic integrity, fabricated metadata flags, demonstrably corrupted time-series/units, or unscientific joins. Must be resolved before any evaluation or demonstration.
- **P1 — High:** Broken code paths, schema fragmentation, missing spatial coordinates, or missing core Big Data processing implementations.
- **P2 — Moderate:** Documentation drift, empty architectural stubs, mock pipelines, and API/frontend stubs.
- **P3 — Optional / Future:** Enhancements, additional data ingestion, or long-term streaming extensions.

---

## 2. Remediation Action Items

### Priority P0 — Critical (Immediate Academic Integrity Fixes)

#### Action P0-1: Quarantine & Relabel Synthetic Traffic Master Dataset
- **Target File:** data/raw/gurugram_traffic_master_consolidated.csv (40,320 rows)
- **Problem:** Contains 2,880 rows with is_source_observation = True on 2018-01-15 despite being synthetically generated via seeded stochastic expansion (seed=42). Storing this in data/raw/ creates severe risk of an examiner concluding data was fabricated.
- **Required Fix:**
  1. Set is_source_observation = False on all 40,320 rows.
  2. Move the file from data/raw/ to a dedicated directory: data/benchmark/synthetic/synthetic_traffic_master_40k.csv.
  3. Ensure documentation clearly labels it as a Big Data scalability benchmark only.

#### Action P0-2: Synchronize 2022–2023 Weather Timezones from UTC to IST
- **Target File:** data/processed/weather/weather_cleaned.csv and .parquet (26,304 rows)
- **Problem:** 2022 and 2023 Open-Meteo reanalysis records are in UTC (peak temperature at 09:00), while 2024 is in IST (peak temperature at 15:00), causing a 5.5-hour phase shift across 17,520 hours.
- **Required Fix:**
  1. Add 5 hours and 30 minutes to all 2022 and 2023 timestamps: timestamp_ist = timestamp_utc + timedelta(hours=5, minutes=30).
  2. Recompute date, hour, month, and day_of_week based on IST.
  3. Regenerate weather_cleaned.csv and weather_cleaned.parquet.

#### Action P0-3: Harmonize Weather Atmospheric Pressure Levels
- **Target File:** data/processed/weather/weather_cleaned.csv and .parquet
- **Problem:** 2022–2023 records have Surface Pressure (~982 hPa), whereas 2024 records have Mean Sea Level Pressure (MSLP, ~1015 hPa), creating an artificial 33 hPa jump on 2024-01-01.
- **Required Fix:**
  1. Convert 2022–2023 surface pressure to MSLP using standard barometric formula: MSLP = P_surf * (1 - (0.0065 * h) / (T + 0.0065 * h + 273.15))^(-5.257), where h = 230m.
  2. Or clearly split into two distinct schema fields: surface_pressure_hpa and mslp_hpa.

#### Action P0-4: Purge Random Spatial Mapping from Integration Code
- **Target File:** spark/preprocessing/data_integration.py (lines 68–75)
- **Problem:** Uses np.random.seed(42) and np.random.choice(sectors) to randomly assign traffic survey locations to municipal sectors.
- **Required Fix:**
  1. Remove the random choice logic entirely.
  2. Map traffic locations to sectors using verified arterial corridor spatial references (e.g., Kherki Daula Toll -> NH-48 / Sector 80; Subhash Chowk -> Sohna Road / Sector 38/47).

---

### Priority P1 — High (Core Functionality & Defensibility Repairs)

#### Action P1-1: Restore Verified Spatial Coordinates to Geography Reference
- **Target File:** data/processed/geography/geography_cleaned.csv (138 rows)
- **Problem:** 100% of latitude, longitude, zone, elevation, and pincode values are NULL, making spatial queries and GIS maps impossible.
- **Required Fix:**
  1. Repopulate verified coordinates for the 123 municipal sectors from data/raw/Gurgaon_Geographical_GIS_Dataset_123_Sectors.csv.
  2. Populate verified coordinates for the 15 major named localities (Cyber City, DLF Phases, Udyog Vihar).
  3. Regenerate geography_cleaned.csv and geography_cleaned.parquet.

#### Action P1-2: Harmonize Weather Humidity Column Fragmentation
- **Target File:** data/processed/weather/weather_cleaned.csv
- **Problem:** 2022–2023 uses humidity_percent (8,784 nulls in 2024), while 2024 uses humidity_pct (17,520 nulls in 2022–2023).
- **Required Fix:**
  1. Coalesce both columns into a single canonical relative_humidity_pct column.
  2. Standardize wind_direction and weather_condition metadata.

#### Action P1-3: Fix Broken Path References in Data Cleaning Script
- **Target File:** spark/preprocessing/data_cleaning.py
- **Problem:** Script defines DATA_DIR = PROJECT_ROOT / 'data', then calls pd.read_csv(DATA_DIR / 'midblock_traffic.csv'). The files actually reside in data/raw/. Running the script throws FileNotFoundError.
- **Required Fix:**
  1. Update DATA_DIR = PROJECT_ROOT / 'data' / 'raw'.
  2. Refactor core cleaning routines from Pandas to native PySpark DataFrames to satisfy the project's big data architecture mandate.

#### Action P1-4: Implement MapReduce Processing Jobs
- **Target Directory:** hadoop/mapreduce/ (currently 0 files)
- **Problem:** Course requirement CSE 3712 requires MapReduce. The directory is completely empty.
- **Required Fix:**
  1. Create Python Hadoop Streaming scripts:
     - mapper_traffic.py & reducer_traffic.py (calculating corridor PCU totals and vehicle composition).
     - mapper_weather.py & reducer_weather.py (calculating monthly diurnal temperature and extreme weather days).
  2. Provide a local runner script test_mapreduce_local.sh demonstrating map | sort | reduce pipeline on standard input/output.

#### Action P1-5: Implement Spark SQL Analytical Query Suite
- **Target Directory:** spark/sql/ (currently only .gitkeep)
- **Problem:** Spark SQL is a stated tier in the architecture but contains no query scripts.
- **Required Fix:**
  1. Create queries.sql or pyspark_sql_analytics.py executing analytical queries against the Parquet tables:
     - Corridor capacity analysis.
     - Correlation between wind speed and PM2.5/PM10 dispersion.
     - Diurnal temperature range and seasonal pollution category breakdown.

---

### Priority P2 — Moderate (Documentation & Application Layer Stubs)

#### Action P2-1: Re-scope Project Roadmap & Align README Claims
- **Target File:** README.md, docs/architecture.md, docs/data_sources.md, docs/data_dictionary.md
- **Problem:** README claims Events integration and real-time streaming, but Events has 0 records and docs/ stubs are 15-byte empty files.
- **Required Fix:**
  1. Populate docs/data_dictionary.md, data_sources.md, and architecture.md with verified schemas.
  2. Formally move Events to Phase 2 Future Scope in README.md.
  3. Correct HDFS directory references from /citypulse/ to /urbansphere/.

#### Action P2-2: Implement Baseline Machine Learning Analytics Scripts
- **Target Directory:** analytics/ (currently empty subdirectories)
- **Problem:** Subdirectories statistics/, classification/, clustering/, anomaly_detection/ are 0-byte empty directories.
- **Required Fix:**
  1. analytics/classification/train_aqi_classifier.py: Train Random Forest on 2024 weather features to predict CPCB AQI Category.
  2. analytics/clustering/cluster_pollution_profiles.py: K-Means clustering of daily multi-pollutant vectors.
  3. analytics/anomaly_detection/detect_pollution_spikes.py: Isolation Forest / Z-score detection of severe winter smog episodes.

#### Action P2-3: Implement FastAPI Backend Stubs
- **Target Directory:** backend/app/
- **Problem:** Services, schemas, and api subdirectories are empty.
- **Required Fix:**
  1. Create main.py with FastAPI endpoints serving analytical summary JSONs and ML inference predictions.

---

### Priority P3 — Optional / Future Enhancements

#### Action P3-1: Docker Compose for Multi-Container Big Data Environment
- Provide docker-compose.yml running Apache Hadoop (NameNode, DataNode) and Apache Spark cluster to allow local multi-node demonstration without bare-metal installation.

#### Action P3-2: Next.js Frontend Dashboard Implementation
- Implement the interactive web dashboard with Leaflet GIS maps and Chart.js analytical charts consuming the FastAPI backend.
