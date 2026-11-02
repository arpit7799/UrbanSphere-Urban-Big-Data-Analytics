# UrbanSphere — Data Sources & Provenance

| Domain | Source Authority | Instrument / Methodology | Temporal Coverage | Resolution | Status & Integrity |
|:---|:---|:---|:---|:---|:---|
| **Traffic (Survey)** | RITES Ltd. / HMRTC | 2018 Primary Traffic Surveys (Gurugram Metro DPR, 2019) | 2018 typical working days | Daily totals & peak hours | **Authoritative (Level A)**: 15 locations, 6 verified tables, 0 modifications. |
| **Traffic (Benchmark)** | UrbanSphere Simulation | Seeded stochastic expansion (`seed=42`) | 14 dates in 2018 | 15-minute directional slots | **Synthetic Benchmark (Level C)**: Quarantined under `data/benchmark/synthetic/`. All rows `is_source_observation=False`. |
| **Weather (Observed)** | India Meteorological Dept (IMD) | Automated Weather Station, Gurugram | 2024-01-01 to 2024-12-31 | Hourly (8,784 rows) | **Observed (Level C)**: IST timestamps, complete annual sequence. |
| **Weather (Reanalysis)** | Open-Meteo Historical API | ERA5 / ECMWF Reanalysis Model | 2022-01-01 to 2023-12-31 | Hourly (17,520 rows) | **Reanalysis (Level C)**: Converted from UTC to IST (+5:30). Harmonized pressure levels. |
| **Air Quality (Observed)** | CPCB / HSPCB CAAQMS Network | 4 Continuous Ambient Air Quality Stations (Vikas Sadan, Sec 51, Teri Gram, NISE) | 2024-01-01 to 2024-12-31 | Daily (1,464 records) | **Observed (Level C)**: 4 verified official stations, CPCB NAQI formula. Suspected pre-imputed. |
| **Air Quality (Reanalysis)**| Open-Meteo CAMS | Copernicus Atmospheric Monitoring Service | 2022-08-04 to 2023-12-31 | Daily (515 records) | **Reanalysis (Level D)**: Missing 215 days in 2022 preserved. CO harmonized to mg/m3. NAQI calculated. |
| **Geography** | GMDA / MCG Planning Reference | GIS Centroid Compilation | Static reference (2024) | Sector-level (123 sectors) | **Reference (Level B)**: Authentic coordinates, zones, land use, and corridors. |
| **Events** | None (Uncollected) | N/A | N/A | N/A | **Deferred**: Zero event records. No fabricated events. |
