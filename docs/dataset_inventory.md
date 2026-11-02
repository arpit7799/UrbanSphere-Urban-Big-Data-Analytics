# UrbanSphere — Canonical Dataset Inventory

This document defines the authoritative canonical datasets established directly under `data/` and the derived analytical datasets under `data/processed/integrated/`.

## 1. Canonical Source Datasets (`data/`)

| File | Format | Rows | Columns | Temporal Coverage | Localities | Provenance / Role |
|:---|:---:|---:|---:|:---:|:---:|:---|
| `dataset_weather_gurugram_with_aqi.csv` | CSV | 315,648 | 15 | 2022-01-01 00:00 to 2024-12-31 23:00 | 12 | Hourly meteorological benchmark with embedded weather-derived AQI |
| `dataset_traffic_gurugram.csv` | CSV | 315,648 | 18 | 2022-01-01 00:00 to 2024-12-31 23:00 | 12 | Hourly vehicular traffic, PCU, speed, and congestion classification |
| `dataset_air_quality_gurugram.csv` | CSV | 315,648 | 14 | 2022-01-01 00:00 to 2024-12-31 23:00 | 12 | Hourly criteria air pollutants (PM2.5, PM10, NO2, SO2, CO, O3) & pollutant AQI |
| `dataset_geography_gurugram.csv` | CSV | 12 | 11 | Static Reference | 12 | Representative coordinate centroids, urban function, and corridor attributes |

## 2. Integrated Analytical Parquet Datasets (`data/processed/integrated/`)

| File | Format | Size | Rows | Columns | Purpose |
|:---|:---:|---:|---:|---:|:---|
| `urban_integrated_hourly.parquet` | Parquet (Snappy) | ~10.9 MB | 315,648 | 51 | Master unified hourly dataset. 1:1 join on `(timestamp, location_name)` with full geography attributes and dual AQI provenance (`weather_aqi` and `air_quality_aqi`). |
| `urban_integrated_daily.parquet` | Parquet (Snappy) | ~1.1 MB | 13,152 | 44 | Daily aggregated analytics and ML feature dataset (1,096 days × 12 localities). |
| `integration_metadata.json` | JSON | ~2.3 KB | - | - | Pipeline audit trail: checksums, join cardinalities, null checks, and physical invariant proofs. |

## 3. The 12 Canonical Localities

All hourly datasets and geography records cover the following 12 key urban nodes across Gurugram:
1. **Badshahpur** (Residential / Mixed Corridor)
2. **Cyber City** (Commercial / IT Special Economic Zone)
3. **Golf Course Extension** (High-Density Residential / Arterial)
4. **Golf Course Road** (Commercial & Premium Residential Corridor)
5. **Hero Honda Chowk** (Industrial / Major Highway Junction)
6. **IFFCO Chowk** (Major Transit Node & Arterial Junction)
7. **Manesar** (Industrial / Automobile Manufacturing Hub)
8. **MG Road** (Retail / Metro Transit Transit Corridor)
9. **Old Gurugram** (Traditional High-Density Core / Commercial)
10. **Rajiv Chowk** (Central Highway Junction & Multi-modal Interchange)
11. **Sohna Road** (Arterial Connector / Mixed Urban Corridor)
12. **Udyog Vihar** (Industrial / Commercial Node)

## 4. Provenance & Scientific Defensibility

- **Synthetic Benchmark Characteristics**: The hourly weather, traffic, and pollutant series are rigorous synthetic benchmarks mathematically calibrated to Gurugram's diurnal, seasonal, and geometric profiles across 2022–2024.
- **Dual AQI Provenance**: `dataset_weather_gurugram_with_aqi.csv` and `dataset_air_quality_gurugram.csv` provide independently derived AQI fields. To maintain scientific integrity, both are preserved distinctly as `weather_aqi` and `air_quality_aqi`.
