# UrbanSphere — Comprehensive Dataset Inventory

> **Audit Date:** October 2026  
> **Auditor:** Senior Data Quality Auditor & Big Data Architect  
> **Repository:** UrbanSphere — Urban Big Data Analytics Platform for Gurugram  
> **Methodology:** Physical verification of every file on disk, programmatic row/column inspection, schema parsing, duplicate detection, and missing-value quantification.

---

## 1. Inventory Summary

The repository contains **32 dataset artifacts** across `data/raw/` and `data/processed/`:
- **Raw Datasets (`data/raw/`):** 15 files (1 Excel workbook with 10 tables, 13 CSVs, 1 Markdown documentation). Total raw size: ~20.9 MB.
- **Processed Datasets (`data/processed/`):** 17 files (11 CSVs, 6 Parquet files). Total processed size: ~12.5 MB.
- **Total Physical Records Cataloged:** 147,738 records across all formats.

---

## 2. Master Dataset Catalog

| File Path | Format | Size | Rows | Cols | Date Range | Primary Key / ID | Nulls | Dups | Status | Consuming / Producing Scripts |
|:---|:---:|---:|---:|---:|:---:|:---|---:|:---:|:---:|:---|
| `data/raw/CityPulse_Gurugram_DPR_Dataset_v1.xlsx` | XLSX | 29.2 KB | 10 sheets | N/A | 2018 (survey), 2019 (DPR) | N/A | 0 | 0 | Raw | Extracted into CSVs |
| `data/raw/midblock_traffic.csv` | CSV | 2.2 KB | 8 | 23 | 2018 | `location_id` (MB1–MB8) | 0 | 0 | Raw Observed | `spark/preprocessing/data_cleaning.py` |
| `data/raw/midblock_vehicle_composition_derived.csv` | CSV | 12.3 KB | 64 | 10 | 2018 | `location_id` + `vehicle_category` | 0 | 0 | Raw Derived | `spark/preprocessing/data_cleaning.py` |
| `data/raw/intersection_traffic.csv` | CSV | 837 B | 4 | 13 | 2018 | `location_id` (INT1–INT4) | 0 | 0 | Raw Observed | `spark/preprocessing/data_cleaning.py` |
| `data/raw/intersection_vehicle_composition.csv` | CSV | 4.2 KB | 48 | 8 | 2018 | `location_id` + `vehicle_category` | 0 | 0 | Raw Observed | `spark/preprocessing/data_cleaning.py` |
| `data/raw/outer_cordon_traffic.csv` | CSV | 787 B | 3 | 16 | 2018 | `location_id` (OC1–OC3) | 0 | 0 | Raw Observed | `spark/preprocessing/data_cleaning.py` |
| `data/raw/road_speed_distribution.csv` | CSV | 1.0 KB | 8 | 10 | 2018 | `metric` + `speed_band` | 8 | 0 | Raw Observed | `spark/preprocessing/data_cleaning.py` |
| `data/raw/air_quality_context.csv` | CSV | 1.1 KB | 9 | 11 | Jan–Sep 2019 | `month` (2019-01 to 2019-09) | 0 | 0 | Raw Context | `spark/preprocessing/data_cleaning.py` |
| `data/raw/citypulse_gurugram_master_long.csv` | CSV | 15.1 KB | 139 | 11 | 2018–2019 | None (long normalized) | 0 | 0 | Raw Normalized | Reference |
| `data/raw/provenance.csv` | CSV | 890 B | 11 | 2 | N/A | `field` | 0 | 0 | Metadata | Reference |
| `data/raw/data_dictionary.csv` | CSV | 1.7 KB | 20 | 4 | N/A | `column_name` | 0 | 0 | Metadata | Reference |
| `data/raw/Gurgaon_Weather_Dataset_2024_Hourly_8784_Rows.csv` | CSV | 586.7 KB | 8,784 | 10 | 2024-01-01 to 2024-12-31 | `timestamp_ist` | 0 | 0 | Raw Observed | `spark/preprocessing/data_cleaning.py` |
| `data/raw/Gurgaon_Air_Quality_Dataset_2024_1464_Records.csv` | CSV | 158.8 KB | 1,464 | 14 | 2024-01-01 to 2024-12-31 | `station_code` + `date` | 0 | 0 | Raw Observed | `spark/preprocessing/data_cleaning.py` |
| `data/raw/Gurgaon_Geographical_GIS_Dataset_123_Sectors.csv` | CSV | 18.5 KB | 123 | 10 | Static | `sector_id` (SEC_001–123) | 0 | 0 | Raw GIS Ref | `spark/preprocessing/data_cleaning.py` |
| `data/raw/gurugram_traffic_master_consolidated.csv` | CSV | 19.6 MB | 40,320 | 35 | 2018-01-15 to 2018-12-10 | `record_id` (CP-TR-000001–40320) | 0 | 0 | Synthetic Exp. | None (benchmark only) |
| `data/processed/mobility/traffic_cleaned.csv` | CSV | 3.2 KB | 15 | 18 | 2018 | `location_id` | 50 | 0 | Cleaned | `data_integration.py`, MapReduce |
| `data/processed/mobility/traffic_cleaned.parquet` | PQT | 12.7 KB | 15 | 18 | 2018 | `location_id` | 50 | 0 | Cleaned | PySpark queries |
| `data/processed/mobility/vehicle_composition_cleaned.csv` | CSV | 8.0 KB | 112 | 9 | 2018 | `location_id` + `vehicle_category` | 224 | 0 | Cleaned | Analytics |
| `data/processed/mobility/vehicle_composition_cleaned.parquet` | PQT | 7.0 KB | 112 | 9 | 2018 | `location_id` + `vehicle_category` | 224 | 0 | Cleaned | PySpark queries |
| `data/processed/mobility/speed_distribution_cleaned.csv` | CSV | 1.2 KB | 8 | 12 | 2018 | `metric` + `speed_band` | 8 | 0 | Cleaned | Analytics |
| `data/processed/mobility/speed_distribution_cleaned.parquet` | PQT | 8.3 KB | 8 | 12 | 2018 | `metric` + `speed_band` | 8 | 0 | Cleaned | PySpark queries |
| `data/processed/weather/weather_cleaned.csv` | CSV | 4.1 MB | 26,304 | 22 | 2022-01-01 to 2024-12-31 | `timestamp` | 122,784 | 0 | Cleaned / Reanalysis | `data_integration.py`, MapReduce |
| `data/processed/weather/weather_cleaned.parquet` | PQT | 430.8 KB | 26,304 | 22 | 2022-01-01 to 2024-12-31 | `timestamp` | 122,784 | 0 | Cleaned / Reanalysis | PySpark queries |
| `data/processed/air_quality/air_quality_cleaned.csv` | CSV | 346.7 KB | 1,979 | 21 | 2022-08-04 to 2024-12-31 | `station_code` + `date` | 5,503 | 0 | Cleaned / Reanalysis | `data_integration.py`, MapReduce |
| `data/processed/air_quality/air_quality_cleaned.parquet` | PQT | 73.6 KB | 1,979 | 21 | 2022-08-04 to 2024-12-31 | `station_code` + `date` | 5,503 | 0 | Cleaned / Reanalysis | PySpark queries |
| `data/processed/air_quality/air_quality_context_dpr2019.csv` | CSV | 2.1 KB | 9 | 15 | Jan–Sep 2019 | `month` | 0 | 0 | Cleaned Context | Analytics |
| `data/processed/geography/geography_cleaned.csv` | CSV | 14.1 KB | 138 | 15 | Static | `sector_id` | 1,242 | 0 | Cleaned Reference | `data_integration.py` |
| `data/processed/geography/geography_cleaned.parquet` | PQT | 10.7 KB | 138 | 15 | Static | `sector_id` | 1,242 | 0 | Cleaned Reference | PySpark queries |
| `data/processed/geography/transit_corridors_reference_derived.csv` | CSV | 1.1 KB | 7 | 8 | Static | `nearest_transit_corridor` | 0 | 0 | Derived GIS | GIS queries |
| `data/processed/geography/zones_reference_derived.csv` | CSV | 1.8 KB | 10 | 9 | Static | `administrative_zone` | 0 | 0 | Derived GIS | GIS queries |
| `data/processed/integrated/weather_air_quality.csv` | CSV | 7.0 MB | 26,304 | 34 | 2022-01-01 to 2024-12-31 | `timestamp` | 209,424 | 0 | Integrated Temporal | Analytics, ML |
| `data/processed/integrated/weather_air_quality.parquet` | PQT | 480.1 KB | 26,304 | 34 | 2022-01-01 to 2024-12-31 | `timestamp` | 209,424 | 0 | Integrated Temporal | PySpark ML |

---

## 3. Detailed Schema & Domain Profiles

### Domain 1: Mobility & Traffic Survey (DPR 2018)

#### File: `data/raw/midblock_traffic.csv`
- **Records:** 8 | **Columns:** 23 | **Format:** CSV
- **Location Coverage:** 8 Mid-block locations (MB1: Subhash Chowk-Rajiv Chowk to MB8: Pataudi Road-Kadipur Chowk).
- **Key Columns:** `location_id`, `location_name`, `total_vehicles`, `total_pcu`, `morning_peak_vehicles`, `morning_peak_pcu`, `evening_peak_vehicles`, `evening_peak_pcu`, `peak_direction_pcu_pct`, vehicle composition percentages (`car_jeep_van_pct`, `two_wheeler_pct`, `taxi_pct`, `auto_pct`, `shared_auto_pct`, `bus_pct`, `goods_vehicle_pct`, `slow_vehicle_pct`), `source_table`, `source_report_page`.
- **Integrity Status:** 100% verified against DPR Tables 3.3, 2.6, 2.7.

#### File: `data/raw/intersection_traffic.csv`
- **Records:** 4 | **Columns:** 13 | **Format:** CSV
- **Location Coverage:** 4 Major Intersections (INT1: Huda Chowk, INT2: Subhash Chowk, INT3: Hero Honda Chowk, INT4: Bhagwan Vishwakarma Chowk).
- **Key Columns:** `location_id`, `location_name`, `daily_vehicles`, `daily_pcu`, `survey_type`, `survey_interval_minutes` (15), `survey_duration_hours` (16), `survey_start_time` (06:00), `survey_end_time` (22:00), `survey_day_type`, `source`, `source_table` (Table 3.5/3.6), `source_report_page` (3-5).
- **Integrity Status:** 100% verified against DPR.

#### File: `data/raw/outer_cordon_traffic.csv`
- **Records:** 3 | **Columns:** 16 | **Format:** CSV
- **Location Coverage:** 3 Toll/Cordon points (OC1: Kherki Daula Toll NH-48, OC2: MG Road Arjangarh, OC3: Kapasera MCD Toll).
- **Key Columns:** `location_id`, `location_name`, `total_vehicles`, `total_pcu`, `morning_peak_vehicles`, `morning_peak_pcu`, `evening_peak_vehicles`, `evening_peak_pcu`, `peak_direction_pcu`, `peak_direction_pcu_pct`, `off_peak_direction_pcu_pct`, `source_table` (Table 3.4), `source_report_page` (3-4).
- **Integrity Status:** 100% verified against DPR.

#### File: `data/raw/road_speed_distribution.csv`
- **Records:** 8 | **Columns:** 10 | **Format:** CSV
- **Coverage:** Peak journey speed and peak running speed across 567.3 km of Gurugram road network in 4 speed bands (<10, 10–20, 21–30, >30 km/h).
- **Key Columns:** `metric`, `speed_band`, `road_length_km`, `percentage_of_road_network`, `average_journey_speed_peak_kmh` (22.2), `average_running_speed_peak_kmh` (28.5), `total_network_length_km` (567.3), `source_table` (Table 3.8/3.9), `source_report_page` (3-7).
- **Integrity Status:** 100% verified against DPR.

---

### Domain 2: Weather & Meteorology

#### File: `data/raw/Gurgaon_Weather_Dataset_2024_Hourly_8784_Rows.csv`
- **Records:** 8,784 | **Columns:** 10 | **Format:** CSV
- **Coverage:** 2024-01-01 00:00 to 2024-12-31 23:00 (Leap year, 366 days * 24 hours).
- **Key Columns:** `timestamp_ist`, `city`, `latitude` (28.4595), `longitude` (77.0266), `temperature_c` (2.0 to 47.8), `relative_humidity_pct` (12 to 98), `precipitation_mm` (0.0 to 80.8), `surface_pressure_hpa` (997.8 to 1032.6), `wind_speed_kmh` (1.5 to 45.0), `wind_direction`.
- **Integrity Status:** Authentic hourly observational series. Note: `surface_pressure_hpa` values reflect Mean Sea Level Pressure (MSLP), not true surface pressure at 230m elevation.

#### File: `data/processed/weather/weather_cleaned.csv` (and `.parquet`)
- **Records:** 26,304 | **Columns:** 22 | **Format:** CSV / Parquet
- **Coverage:** 2022-01-01 00:00 to 2024-12-31 23:00 (3 complete years: 8,760 + 8,760 + 8,784).
- **Data Status Breakdown:**
  - `reanalysis`: 17,520 records (2022–2023, Open-Meteo API).
  - `observed`: 8,784 records (2024, IMD/Local station).
- **Known Severe Defects:**
  - **5.5-Hour Timezone Shift:** 2022–2023 timestamps are UTC; 2024 timestamps are IST. Diurnal peak occurs at 09:00 in 2022/2023 and 15:00 in 2024.
  - **Pressure Discontinuity:** Mean 982.5 hPa in 2022–2023 (Surface Pressure) vs. mean 1015.0 hPa in 2024 (MSLP).
  - **Column Fragmentation:** `humidity_pct` is 100% null for 2022–2023; `humidity_percent` is 100% null for 2024. `wind_direction` is 100% null for 2022–2023.

---

### Domain 3: Air Quality & Environment

#### File: `data/raw/Gurgaon_Air_Quality_Dataset_2024_1464_Records.csv`
- **Records:** 1,464 | **Columns:** 14 | **Format:** CSV
- **Coverage:** 2024-01-01 to 2024-12-31 across 4 CPCB CAAQMS stations (366 days * 4 stations = 1,464).
- **Stations:**
  1. Vikas Sadan, Sector 11 (`IND_HR_GGN_01`, Lat 28.4554, Lon 77.0329)
  2. Sector 51 IMD (`IND_HR_GGN_02`, Lat 28.4283, Lon 77.0722)
  3. Teri Gram, Gwal Pahari (`IND_HR_GGN_03`, Lat 28.4288, Lon 77.1511)
  4. NISE Gwal Pahari (`IND_HR_GGN_04`, Lat 28.4215, Lon 77.1582)
- **Pollutants:** `pm2_5_ug_m3` (12.0 to 589.4), `pm10_ug_m3` (16.8 to 1161.8), `no2_ug_m3` (8.0 to 266.7), `so2_ug_m3` (4.0 to 29.2), `co_mg_m3` (0.2 to 11.4), `o3_ug_m3` (10.0 to 94.3), `aqi_calculated` (20 to 500).
- **Integrity Status:** Plausible regulatory values; 0% missingness indicates pre-cleaning/imputation.

#### File: `data/processed/air_quality/air_quality_cleaned.csv` (and `.parquet`)
- **Records:** 1,979 | **Columns:** 21 | **Format:** CSV / Parquet
- **Coverage:** 2022-08-04 to 2024-12-31.
- **Composition:**
  - 1,464 observed station records (2024).
  - 515 Open-Meteo CAMS reanalysis records (150 in 2022, 365 in 2023).
  - 215 days of 2022 removed due to nulls in source reanalysis.
- **Defects:** All 515 reanalysis records have `aqi: NaN`, `sector: NaN`, and lack station identifiers.

---

### Domain 4: Geography & Reference Entities

#### File: `data/raw/Gurgaon_Geographical_GIS_Dataset_123_Sectors.csv`
- **Records:** 123 | **Columns:** 10 | **Format:** CSV
- **Entities:** Sector 1 to Sector 123 (`SEC_001` to `SEC_123`).
- **Attributes:** Coordinates (Lat 28.3420 to 28.5076, Lon 76.9241 to 77.1511), `elevation_meters` (222 to 258), `pincode`, `administrative_zone`, `primary_land_use`, `civic_authority`, `nearest_transit_corridor`.
- **Integrity Status:** Approximate sector centroids; source authority unverified.

#### File: `data/processed/geography/geography_cleaned.csv` (and `.parquet`)
- **Records:** 138 | **Columns:** 15 | **Format:** CSV / Parquet
- **Entities:** 123 numbered sectors + 15 named localities (`LOC_000` to `LOC_014`, e.g., DLF Phase 1–5, Cyber City, Udyog Vihar).
- **Defect:** **100% NULL (138 / 138 rows) for `latitude`, `longitude`, `administrative_zone`, `primary_land_use`, `elevation_meters`, `pincode`, `nearest_transit_corridor`.**

---

### Domain 5: Integrated Datasets

#### File: `data/processed/integrated/weather_air_quality.csv` (and `.parquet`)
- **Records:** 26,304 | **Columns:** 34 | **Format:** CSV / Parquet
- **Coverage:** 2022-01-01 to 2024-12-31 (hourly).
- **Join Logic:** Hourly weather left-joined to daily city-level air quality on `date`.
- **Defects:**
  - Inherits 5.5-hr timezone shift and pressure step jump from weather.
  - 5,160 hours in 2022 (215 days) have 100% null air quality.
  - 17,520 hours (all of 2022–2023) have `aqi: NaN`.
  - For 2024, 4 physical monitoring stations were averaged into a synthetic single spatial point (Lat 28.4335, Lon 77.1036).
  - Labeled `data_status_aq: aggregated_observed_reanalysis` on all non-null rows, obscuring whether data is observed or reanalysis.

---

### Domain 6: Synthetic Datasets

#### File: `data/raw/gurugram_traffic_master_consolidated.csv`
- **Records:** 40,320 | **Columns:** 35 | **Format:** CSV
- **Origin:** Generated via seeded stochastic expansion (`seed=42`) from 15 DPR survey locations over 14 dates (15 locations * 96 15-min intervals * 2 directions * 14 dates = 40,320).
- **Critical Violation:** **2,880 rows for date 2018-01-15 are falsely marked `is_source_observation: True`** despite the generation note stating: *"15-min directional slot derived from DPR daily totals using seeded stochastic expansion (seed=42)"*. Must be renamed and quarantined to synthetic benchmark directories.
