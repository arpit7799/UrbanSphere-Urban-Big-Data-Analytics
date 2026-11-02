# UrbanSphere — Integration Provenance & Scientific Methodology

## 1. Weather <-> Air Quality Integration
- **Canonical Daily Output**: `integrated/weather_air_quality_daily.csv` (and `.parquet`)
  - **Temporal Resolution**: Daily (YYYY-MM-DD).
  - **Methodology**: Hourly weather observations were aggregated to daily meteorological indicators (min, max, mean temperature, diurnal range, total precipitation, humidity, MSLP and surface pressure). Air quality was averaged across active CAAQMS monitoring stations to produce official daily city-wide averages.
  - **Scientific Validity**: Defensible because both datasets are joined at the exact physical temporal resolution of the air-quality observations (daily). Zero artificial row expansion.
- **Contextual Hourly Output**: `integrated/weather_air_quality.csv` (and `.parquet`)
  - **Temporal Resolution**: Hourly weather with daily AQ context.
  - **Explicit Caution**: Columns are explicitly prefixed `daily_city_avg_*` and metadata flag `aq_temporal_type = daily_aggregate_repeated` is embedded in every record to prevent machine learning models from mistaking daily averages for hourly sensor observations.

## 2. Traffic <-> Geography Integration
- **Output File**: `integrated/traffic_geographic_reference.csv` (and `.parquet`)
  - **Methodology**: Deterministic spatial mapping based on manual arterial corridor alignment.
  - **Integrity Fix**: Completely purged `np.random.choice` and `np.random.seed(42)`. Every survey location is assigned to a plausible Gurugram municipal sector. These mappings are deterministic but have not been independently verified against official GIS reference data.
  - **Limitation**: Sector assignments reflect best-effort road-to-sector matching, not GPS-confirmed ground truth.
