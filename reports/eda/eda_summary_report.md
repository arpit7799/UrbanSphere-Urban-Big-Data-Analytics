# UrbanSphere — Comprehensive Exploratory Data Analysis Report
**Target System:** Gurugram Urban Big Data Analytics Platform  
**Datasets Analyzed:** Four Canonical Datasets (Weather/AQI, Traffic, Air Quality, Geography)  
**Temporal Coverage:** 2022-01-01 00:00 to 2024-12-31 23:00 (3 Full Years, 26,304 Hours)  
**Spatial Coverage:** 12 Canonical Localities across Gurugram  
**Generated Date:** 2026-10-28  

---

## 1. Dataset Dimensions and Quality Verification

| Dataset | Canonical Path | Row Count | Column Count | Missing Values | Duplicate Keys | Data Quality Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Weather & AQI** | `data/dataset_weather_gurugram_with_aqi.csv` | 315,648 | 15 | 0 (0.0%) | 0 | 100% Invariant Compliant |
| **Traffic** | `data/dataset_traffic_gurugram.csv` | 315,648 | 18 | 0 (0.0%) | 0 | 100% Invariant Compliant |
| **Air Quality** | `data/dataset_air_quality_gurugram.csv` | 315,648 | 14 | 0 (0.0%) | 0 | 100% Invariant Compliant |
| **Geography** | `data/dataset_geography_gurugram.csv` | 12 | 11 | 0 (0.0%) | 0 | 100% Invariant Compliant |

### Key Invariant Checks:
1. **Traffic Vehicle Sum Consistency:** `vehicle_count == two_wheeler + car + auto + bus + truck + other` confirmed across all 315,648 rows (0 mismatches).
2. **Physical Speeds and PCU:** All PCU and vehicle speed metrics are strictly non-negative.
3. **Temporal Coverage:** Exactly 26,304 contiguous hours $\times$ 12 localities = 315,648 observations for each hourly domain.
4. **Geography Identity:** All 12 locality names in the hourly tables map bit-for-bit to `dataset_geography_gurugram.csv`.

---

## 2. Key Analytical & Exploratory Findings

### A. Traffic & Congestion Patterns
- **Commuter Peaking:** Morning peak occurs sharply between 08:00 and 11:00; evening peak occurs between 17:00 and 21:00. Weekend volumes are flatter and peak later in the afternoon.
- **Modal Composition:** Two-wheelers and private cars constitute the overwhelming majority of urban vehicular trips (~75-80%), while commercial trucks and public buses account for under 10% of total trips.
- **Congestion Hotspots:** Commercial and mixed hubs (Cyber City, IFFCO Chowk, Rajiv Chowk, Sohna Road) experience the highest proportion of "Severe" and "High" congestion hours.

### B. Meteorology & Climate Dynamics
- **Extreme Seasonal Temperature Range:** Gurugram experiences temperatures ranging from ~4°C during January winter nights to ~46°C during June pre-monsoon heatwaves.
- **Monsoon Wet Deposition:** Peak precipitation is concentrated in July and August (~150-250 mm/month), driving high relative humidity (>75%) and rapid particulate wash-out.

### C. Air Quality & Atmospheric Regimes
- **Severe Winter Stagnation:** PM2.5 and PM10 peak dramatically in November, December, and January, driven by low temperatures, boundary layer trapping, calm surface winds, and post-monsoon biomass burning.
- **Monsoon Cleanliness:** Air quality is at its cleanest between July and September, with average PM2.5 dropping below the 60 µg/m³ 24-hr NAAQS standard.

### D. Critical AQI Discrepancy Analysis
- **Provenance Distinction:** The `aqi` column in `dataset_weather_gurugram_with_aqi.csv` and `dataset_air_quality_gurugram.csv` were generated via separate models/heuristics.
- In the weather dataset, AQI values are calculated with weather interaction terms; in the air-quality dataset, AQI is directly derived from criteria pollutant concentrations (PM2.5, PM10, NO2, SO2, CO, O3).
- **Integration Rule:** The integration pipeline explicitly preserves both fields as `weather_aqi` and `air_quality_aqi` to avoid confounding or false ground truth claims.

---

## 3. Generated Visual Artifacts

The following figures have been exported to `reports/eda/`:
1. `01_geographic_localities_layout.png`: Spatial distribution of 12 study localities across Gurugram.
2. `02_traffic_diurnal_peaks.png`: Weekday vs Weekend hourly volume profiles and peak commute intervals.
3. `03_vehicle_modal_split.png`: Fleet composition breakdown across vehicle classes.
4. `04_congestion_by_locality.png`: Proportion of congestion severity tiers across 12 localities.
5. `05_monthly_climate_patterns.png`: Annual climatological cycle (temperature & relative humidity).
6. `06_particulate_seasonal_dynamics.png`: Monthly PM2.5 and PM10 trajectories compared against 24-hr NAAQS thresholds.
7. `07_aqi_source_comparison.png`: Distributional alignment and divergence between weather and air quality AQI fields.
8. `08_multivariate_correlation_matrix.png`: Cross-domain Pearson correlation matrix aligned by timestamp and locality.

---

## 4. Methodological Limitations
1. **Synthetic Benchmark Nature:** As documented in the dataset specifications, these records represent high-fidelity synthetic urban benchmarks calibrated to Gurugram's topography and traffic norms, rather than direct certified continuous sensor streams.
2. **Correlation vs Causation:** Statistical associations between surface wind speed or temperature and air pollutants represent atmospheric correlations, not unilateral causal proofs.
