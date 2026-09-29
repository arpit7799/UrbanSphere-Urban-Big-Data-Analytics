"""
UrbanSphere — Stage 2: Data Cleaning & Profiling
================================================
Loads all datasets from data/, profiles them, cleans/standardizes,
and saves cleaned outputs to data/processed/{domain}/.

Data Integrity Rules:
- Never fabricate observations
- Preserve source provenance
- Label synthetic data explicitly
- Do not join 2018 traffic with 2024 weather/AQ
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ============================================================
# Configuration
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

# Create output directories
for subdir in ["mobility", "weather", "air_quality", "geography", "integrated"]:
    (PROCESSED_DIR / subdir).mkdir(parents=True, exist_ok=True)

# Tracking
profiling_results = {}
cleaning_log = []

def log(msg):
    """Print and store log messages."""
    print(msg)
    cleaning_log.append(msg)

def profile_dataset(name, df):
    """Profile a DataFrame and return summary dict."""
    result = {
        "name": name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "nulls": df.isnull().sum().to_dict(),
        "null_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "duplicates": df.duplicated().sum(),
    }
    profiling_results[name] = result
    return result

def print_profile(name, result):
    """Print a formatted profile summary."""
    log(f"\n{'='*60}")
    log(f"PROFILE: {name}")
    log(f"{'='*60}")
    log(f"  Rows: {result['rows']}")
    log(f"  Columns: {result['columns']}")
    log(f"  Duplicates: {result['duplicates']}")
    
    # Null summary
    nulls = {k: v for k, v in result['nulls'].items() if v > 0}
    if nulls:
        log(f"  Columns with nulls:")
        for col, count in nulls.items():
            log(f"    - {col}: {count} ({result['null_pct'][col]}%)")
    else:
        log(f"  Nulls: None")
    
    # Dtypes
    log(f"  Column types:")
    for col, dtype in result['dtypes'].items():
        log(f"    - {col}: {dtype}")

def save_cleaned(df, domain, name, parquet=True):
    """Save cleaned dataset as CSV and optionally Parquet."""
    csv_path = PROCESSED_DIR / domain / f"{name}.csv"
    df.to_csv(csv_path, index=False)
    log(f"  Saved: {csv_path} ({len(df)} rows)")
    
    if parquet:
        parquet_path = PROCESSED_DIR / domain / f"{name}.parquet"
        df.to_parquet(parquet_path, index=False, engine="pyarrow")
        log(f"  Saved: {parquet_path}")
    
    return csv_path


# ============================================================
# 1. MOBILITY — Source-Grounded Traffic Data
# ============================================================
log("\n" + "#"*60)
log("# DOMAIN: MOBILITY / TRAFFIC")
log("#"*60)

# --- 1a. Midblock Traffic ---
log("\n--- Loading midblock_traffic.csv ---")
mb = pd.read_csv(DATA_DIR / "midblock_traffic.csv")
p = profile_dataset("midblock_traffic", mb)
print_profile("midblock_traffic", p)

# Standardize: already has good column names
# Validate numeric fields
numeric_cols_mb = ['total_vehicles', 'total_pcu', 'morning_peak_vehicles', 
                   'morning_peak_pcu', 'evening_peak_vehicles', 'evening_peak_pcu']
for col in numeric_cols_mb:
    invalid = (mb[col] < 0).sum()
    if invalid > 0:
        log(f"  WARNING: {col} has {invalid} negative values")
    else:
        log(f"  ✓ {col}: all values non-negative")

# Validate percentages sum
pct_cols = [c for c in mb.columns if c.endswith('_pct') and c not in ['peak_direction_pcu_pct', 'off_peak_direction_pcu_pct']]
if pct_cols:
    pct_sums = mb[pct_cols].sum(axis=1)
    log(f"  Vehicle composition % sums: {pct_sums.values} (should be ~100)")

# Add provenance
mb_clean = mb.copy()
mb_clean['data_status'] = 'observed'
mb_clean['source_year'] = 2018
mb_clean['source_domain'] = 'mobility'


# --- 1b. Intersection Traffic ---
log("\n--- Loading intersection_traffic.csv ---")
it = pd.read_csv(DATA_DIR / "intersection_traffic.csv")
p = profile_dataset("intersection_traffic", it)
print_profile("intersection_traffic", p)

for col in ['daily_vehicles', 'daily_pcu']:
    invalid = (it[col] < 0).sum()
    log(f"  ✓ {col}: {'all non-negative' if invalid == 0 else f'{invalid} negative!'}")

it_clean = it.copy()
it_clean['data_status'] = 'observed'
it_clean['source_year'] = 2018
it_clean['source_domain'] = 'mobility'


# --- 1c. Outer Cordon Traffic ---
log("\n--- Loading outer_cordon_traffic.csv ---")
oc = pd.read_csv(DATA_DIR / "outer_cordon_traffic.csv")
p = profile_dataset("outer_cordon_traffic", oc)
print_profile("outer_cordon_traffic", p)

for col in ['total_vehicles', 'total_pcu']:
    invalid = (oc[col] < 0).sum()
    log(f"  ✓ {col}: {'all non-negative' if invalid == 0 else f'{invalid} negative!'}")

oc_clean = oc.copy()
oc_clean['data_status'] = 'observed'
oc_clean['source_year'] = 2018
oc_clean['source_domain'] = 'mobility'


# --- 1d. Vehicle Compositions ---
log("\n--- Loading intersection_vehicle_composition.csv ---")
ivc = pd.read_csv(DATA_DIR / "intersection_vehicle_composition.csv")
p = profile_dataset("intersection_vehicle_composition", ivc)
print_profile("intersection_vehicle_composition", p)

# Validate: compositions should sum to ~100% per location
for loc_id in ivc['location_id'].unique():
    loc_sum = ivc[ivc['location_id'] == loc_id]['composition_pct'].sum()
    log(f"  {loc_id} composition sum: {loc_sum:.2f}% (should be ~100%)")

ivc_clean = ivc.copy()
ivc_clean['data_status'] = 'observed'
ivc_clean['source_year'] = 2018

log("\n--- Loading midblock_vehicle_composition_derived.csv ---")
mvc = pd.read_csv(DATA_DIR / "midblock_vehicle_composition_derived.csv")
p = profile_dataset("midblock_vehicle_composition_derived", mvc)
print_profile("midblock_vehicle_composition_derived", p)

# Validate: compositions should sum to ~100% per location
for loc_id in mvc['location_id'].unique():
    loc_sum = mvc[mvc['location_id'] == loc_id]['source_percentage'].sum()
    log(f"  {loc_id} composition sum: {loc_sum:.2f}% (should be ~100%)")

mvc_clean = mvc.copy()
mvc_clean['data_status'] = 'derived'
mvc_clean['source_year'] = 2018


# --- 1e. Road Speed Distribution ---
log("\n--- Loading road_speed_distribution.csv ---")
rsd = pd.read_csv(DATA_DIR / "road_speed_distribution.csv")
p = profile_dataset("road_speed_distribution", rsd)
print_profile("road_speed_distribution", p)

# Validate: road lengths should sum to 567.3 km for each metric
for metric in rsd['metric'].unique():
    total_km = rsd[rsd['metric'] == metric]['road_length_km'].sum()
    log(f"  {metric} total road length: {total_km:.1f} km (should be ~567.3 km)")

rsd_clean = rsd.copy()
rsd_clean['data_status'] = 'observed'
rsd_clean['source_year'] = 2018


# --- 1f. Create unified traffic_cleaned.csv ---
log("\n--- Creating unified traffic_cleaned.csv ---")

# Combine the three traffic survey datasets into a single canonical format
# Each has different columns, so we normalize to a common schema

records = []

# Midblock
for _, row in mb_clean.iterrows():
    records.append({
        'location_id': row['location_id'],
        'location_name': row['location_name'],
        'location_type': 'mid_block',
        'daily_total_vehicles': row['total_vehicles'],
        'daily_total_pcu': row['total_pcu'],
        'morning_peak_vehicles': row['morning_peak_vehicles'],
        'morning_peak_pcu': row['morning_peak_pcu'],
        'evening_peak_vehicles': row['evening_peak_vehicles'],
        'evening_peak_pcu': row['evening_peak_pcu'],
        'peak_direction_pcu_pct': row['peak_direction_pcu_pct'],
        'survey_type': row['survey_type'],
        'survey_day_type': row['survey_day_type'],
        'data_status': 'observed',
        'source_year': 2018,
        'source': row['source'],
        'source_table': row['source_table'],
    })

# Intersection
for _, row in it_clean.iterrows():
    records.append({
        'location_id': row['location_id'],
        'location_name': row['location_name'],
        'location_type': 'intersection',
        'daily_total_vehicles': row['daily_vehicles'],
        'daily_total_pcu': row['daily_pcu'],
        'morning_peak_vehicles': np.nan,  # not available for intersections
        'morning_peak_pcu': np.nan,
        'evening_peak_vehicles': np.nan,
        'evening_peak_pcu': np.nan,
        'peak_direction_pcu_pct': np.nan,
        'survey_type': row['survey_type'],
        'survey_day_type': row['survey_day_type'],
        'data_status': 'observed',
        'source_year': 2018,
        'source': row['source'],
        'source_table': row['source_table'],
    })

# Outer cordon
for _, row in oc_clean.iterrows():
    records.append({
        'location_id': row['location_id'],
        'location_name': row['location_name'],
        'location_type': 'outer_cordon',
        'daily_total_vehicles': row['total_vehicles'],
        'daily_total_pcu': row['total_pcu'],
        'morning_peak_vehicles': row['morning_peak_vehicles'],
        'morning_peak_pcu': row['morning_peak_pcu'],
        'evening_peak_vehicles': row['evening_peak_vehicles'],
        'evening_peak_pcu': row['evening_peak_pcu'],
        'peak_direction_pcu_pct': row['peak_direction_pcu_pct'],
        'survey_type': row['survey_type'],
        'survey_day_type': row['survey_day_type'],
        'data_status': 'observed',
        'source_year': 2018,
        'source': row['source'],
        'source_table': row['source_table'],
    })

traffic_cleaned = pd.DataFrame(records)
log(f"  Unified traffic dataset: {len(traffic_cleaned)} locations")
log(f"  Location types: {traffic_cleaned['location_type'].value_counts().to_dict()}")
log(f"  Schema: {list(traffic_cleaned.columns)}")

save_cleaned(traffic_cleaned, "mobility", "traffic_cleaned")

# Also save the vehicle composition and speed data
# Merge midblock + intersection compositions into one file
all_compositions = []
for _, row in ivc_clean.iterrows():
    all_compositions.append({
        'location_id': row['location_id'],
        'location_name': row['location_name'],
        'location_type': 'intersection',
        'vehicle_category': row['vehicle_category'],
        'composition_pct': row['composition_pct'],
        'data_status': 'observed',
        'source_year': 2018,
    })
for _, row in mvc_clean.iterrows():
    all_compositions.append({
        'location_id': row['location_id'],
        'location_name': row['location_name'],
        'location_type': 'mid_block',
        'vehicle_category': row['vehicle_category'],
        'composition_pct': row['source_percentage'],
        'data_status': 'derived' if not row['is_source_observation'] else 'observed',
        'source_year': 2018,
    })

vehicle_comp = pd.DataFrame(all_compositions)
save_cleaned(vehicle_comp, "mobility", "vehicle_composition_cleaned")
save_cleaned(rsd_clean, "mobility", "speed_distribution_cleaned")


# ============================================================
# 2. WEATHER (2024)
# ============================================================
log("\n" + "#"*60)
log("# DOMAIN: WEATHER")
log("#"*60)

log("\n--- Loading Gurgaon_Weather_Dataset_2024_Hourly_8784_Rows.csv ---")
weather = pd.read_csv(DATA_DIR / "Gurgaon_Weather_Dataset_2024_Hourly_8784_Rows.csv")
p = profile_dataset("weather_2024", weather)
print_profile("weather_2024", p)

# Standardize column names
weather_clean = weather.rename(columns={
    'timestamp_ist': 'timestamp',
    'temperature_c': 'temperature_c',
    'relative_humidity_pct': 'humidity_pct',
    'precipitation_mm': 'precipitation_mm',
    'surface_pressure_hpa': 'pressure_hpa',
    'wind_speed_kmh': 'wind_speed_kmh',
    'wind_direction': 'wind_direction',
})

# Parse timestamp
weather_clean['timestamp'] = pd.to_datetime(weather_clean['timestamp'], format='mixed')
weather_clean['date'] = weather_clean['timestamp'].dt.date.astype(str)
weather_clean['hour'] = weather_clean['timestamp'].dt.hour
weather_clean['month'] = weather_clean['timestamp'].dt.month
weather_clean['day_of_week'] = weather_clean['timestamp'].dt.day_name()

# Validate ranges
log("\n  Validation checks:")
log(f"  Temperature range: {weather_clean['temperature_c'].min():.1f} to {weather_clean['temperature_c'].max():.1f} °C")
log(f"  Humidity range: {weather_clean['humidity_pct'].min():.1f} to {weather_clean['humidity_pct'].max():.1f} %")
log(f"  Precipitation range: {weather_clean['precipitation_mm'].min():.1f} to {weather_clean['precipitation_mm'].max():.1f} mm")
log(f"  Wind speed range: {weather_clean['wind_speed_kmh'].min():.1f} to {weather_clean['wind_speed_kmh'].max():.1f} km/h")
log(f"  Pressure range: {weather_clean['pressure_hpa'].min():.1f} to {weather_clean['pressure_hpa'].max():.1f} hPa")

# Check for impossible values
temp_invalid = ((weather_clean['temperature_c'] < -10) | (weather_clean['temperature_c'] > 55)).sum()
humidity_invalid = ((weather_clean['humidity_pct'] < 0) | (weather_clean['humidity_pct'] > 100)).sum()
log(f"  Temperature out of plausible range (-10 to 55°C): {temp_invalid}")
log(f"  Humidity out of range (0-100%): {humidity_invalid}")

# Check date range
log(f"  Date range: {weather_clean['timestamp'].min()} to {weather_clean['timestamp'].max()}")
log(f"  Unique dates: {weather_clean['date'].nunique()}")

# Check duplicates
dup_timestamps = weather_clean.duplicated(subset=['timestamp']).sum()
log(f"  Duplicate timestamps: {dup_timestamps}")

# Handle wind direction: 'Calm' is a valid value (means no wind)
calm_count = (weather_clean['wind_direction'] == 'Calm').sum()
log(f"  Wind direction 'Calm' entries: {calm_count}")

# Add provenance
weather_clean['data_status'] = 'observed'
weather_clean['source_year'] = 2024
weather_clean['source_domain'] = 'weather'

# Drop city/lat/lon (constant — Gurugram)
weather_clean = weather_clean.drop(columns=['city'], errors='ignore')

log(f"\n  Final weather schema: {list(weather_clean.columns)}")
log(f"  Final rows: {len(weather_clean)}")

save_cleaned(weather_clean, "weather", "weather_cleaned")


# ============================================================
# 3. AIR QUALITY (2024)
# ============================================================
log("\n" + "#"*60)
log("# DOMAIN: AIR QUALITY")
log("#"*60)

log("\n--- Loading Gurgaon_Air_Quality_Dataset_2024_1464_Records.csv ---")
aq = pd.read_csv(DATA_DIR / "Gurgaon_Air_Quality_Dataset_2024_1464_Records.csv")
p = profile_dataset("air_quality_2024", aq)
print_profile("air_quality_2024", p)

# Standardize column names
aq_clean = aq.rename(columns={
    'date': 'date',
    'station_code': 'station_code',
    'station_name': 'station_name',
    'sector': 'sector',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'pm2_5_ug_m3': 'pm25',
    'pm10_ug_m3': 'pm10',
    'no2_ug_m3': 'no2',
    'so2_ug_m3': 'so2',
    'co_mg_m3': 'co',
    'o3_ug_m3': 'o3',
    'aqi_calculated': 'aqi',
    'air_quality_category': 'aqi_category',
})

# Parse date
aq_clean['date'] = pd.to_datetime(aq_clean['date'])
aq_clean['month'] = aq_clean['date'].dt.month
aq_clean['day_of_week'] = aq_clean['date'].dt.day_name()
aq_clean['date'] = aq_clean['date'].dt.date.astype(str)

# Validate ranges
log("\n  Validation checks:")
log(f"  Stations: {aq_clean['station_name'].unique().tolist()}")
log(f"  Records per station: {aq_clean['station_name'].value_counts().to_dict()}")
log(f"  Date range: {aq_clean['date'].min()} to {aq_clean['date'].max()}")
log(f"  PM2.5 range: {aq_clean['pm25'].min():.1f} to {aq_clean['pm25'].max():.1f}")
log(f"  PM10 range: {aq_clean['pm10'].min():.1f} to {aq_clean['pm10'].max():.1f}")
log(f"  AQI range: {aq_clean['aqi'].min():.0f} to {aq_clean['aqi'].max():.0f}")
log(f"  AQI categories: {aq_clean['aqi_category'].value_counts().to_dict()}")

# Check for negative pollutant values
for pol in ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']:
    neg_count = (aq_clean[pol] < 0).sum()
    null_count = aq_clean[pol].isnull().sum()
    log(f"  {pol}: negatives={neg_count}, nulls={null_count}")

# Check for impossible coordinates
lat_range = (aq_clean['latitude'].min(), aq_clean['latitude'].max())
lon_range = (aq_clean['longitude'].min(), aq_clean['longitude'].max())
log(f"  Latitude range: {lat_range} (Gurugram ~28.4-28.5)")
log(f"  Longitude range: {lon_range} (Gurugram ~76.9-77.1)")

# Check duplicate dates per station
dup_station_date = aq_clean.duplicated(subset=['station_code', 'date']).sum()
log(f"  Duplicate station+date: {dup_station_date}")

# Add provenance
aq_clean['data_status'] = 'observed'
aq_clean['source_year'] = 2024
aq_clean['source_domain'] = 'air_quality'

log(f"\n  Final AQ schema: {list(aq_clean.columns)}")
log(f"  Final rows: {len(aq_clean)}")

save_cleaned(aq_clean, "air_quality", "air_quality_cleaned")


# Also clean the DPR air quality context (2019 monthly)
log("\n--- Loading air_quality_context.csv (DPR 2019) ---")
aq_ctx = pd.read_csv(DATA_DIR / "air_quality_context.csv")
p = profile_dataset("air_quality_context_2019", aq_ctx)
print_profile("air_quality_context_2019", p)

aq_ctx_clean = aq_ctx.copy()
aq_ctx_clean['data_status'] = 'contextual'
aq_ctx_clean['source_year'] = 2019
aq_ctx_clean['source_domain'] = 'air_quality'
aq_ctx_clean['note'] = 'DPR Table 2.13 — contextual only, not for temporal joins with 2024 data'

save_cleaned(aq_ctx_clean, "air_quality", "air_quality_context_dpr2019", parquet=False)


# ============================================================
# 4. GEOGRAPHY
# ============================================================
log("\n" + "#"*60)
log("# DOMAIN: GEOGRAPHY")
log("#"*60)

log("\n--- Loading Gurgaon_Geographical_GIS_Dataset_123_Sectors.csv ---")
geo = pd.read_csv(DATA_DIR / "Gurgaon_Geographical_GIS_Dataset_123_Sectors.csv")
p = profile_dataset("geography", geo)
print_profile("geography", p)

# Standardize column names (already clean)
geo_clean = geo.copy()

# Validate coordinates
log("\n  Validation checks:")
log(f"  Latitude range: {geo_clean['latitude'].min():.4f} to {geo_clean['latitude'].max():.4f}")
log(f"  Longitude range: {geo_clean['longitude'].min():.4f} to {geo_clean['longitude'].max():.4f}")
log(f"  Elevation range: {geo_clean['elevation_meters'].min()} to {geo_clean['elevation_meters'].max()} m")
log(f"  Administrative zones: {geo_clean['administrative_zone'].nunique()}")
log(f"  Zone distribution:")
for zone, count in geo_clean['administrative_zone'].value_counts().items():
    log(f"    - {zone}: {count} sectors")
log(f"  Land use types: {geo_clean['primary_land_use'].nunique()}")
log(f"  Civic authorities: {geo_clean['civic_authority'].unique().tolist()}")

# Check for duplicate sector IDs
dup_sectors = geo_clean.duplicated(subset=['sector_id']).sum()
log(f"  Duplicate sector IDs: {dup_sectors}")

# Add provenance
geo_clean['data_status'] = 'reference'
geo_clean['source_domain'] = 'geography'

save_cleaned(geo_clean, "geography", "geography_cleaned", parquet=False)


# ============================================================
# 5. SYNTHETIC BENCHMARK — Profile only, label clearly
# ============================================================
log("\n" + "#"*60)
log("# SYNTHETIC BENCHMARK (profile only)")
log("#"*60)

log("\n--- Loading gurugram_traffic_master_consolidated.csv ---")
synth = pd.read_csv(DATA_DIR / "gurugram_traffic_master_consolidated.csv", nrows=5)
synth_full = pd.read_csv(DATA_DIR / "gurugram_traffic_master_consolidated.csv")
p = profile_dataset("traffic_master_SYNTHETIC", synth_full)
print_profile("traffic_master_SYNTHETIC", p)

log(f"\n  ⚠️  THIS IS SYNTHETIC/BENCHMARK DATA")
log(f"  Generated via stochastic expansion from DPR daily totals")
log(f"  Must NOT be presented as observed traffic")
log(f"  Total rows: {len(synth_full)}")
log(f"  Columns: {len(synth_full.columns)}")
log(f"  Date range: {synth_full['survey_date'].min()} to {synth_full['survey_date'].max()}")
log(f"  Locations: {synth_full['location_name'].nunique()}")
log(f"  Location types: {synth_full['location_type'].value_counts().to_dict()}")

# Do NOT save to processed — it's benchmark only, stays in data/
# Just document it

# ============================================================
# 6. SUMMARY
# ============================================================
log("\n" + "#"*60)
log("# STAGE 2 SUMMARY")
log("#"*60)

log("\nFiles created in data/processed/:")
for root, dirs, files in os.walk(PROCESSED_DIR):
    for f in sorted(files):
        fpath = Path(root) / f
        size = fpath.stat().st_size
        log(f"  {fpath.relative_to(PROJECT_ROOT)} — {size:,} bytes")

log("\nDataset row counts (cleaned):")
log(f"  traffic_cleaned.csv: {len(traffic_cleaned)} locations")
log(f"  vehicle_composition_cleaned.csv: {len(vehicle_comp)} records")
log(f"  speed_distribution_cleaned.csv: {len(rsd_clean)} records")
log(f"  weather_cleaned.csv: {len(weather_clean)} rows")
log(f"  air_quality_cleaned.csv: {len(aq_clean)} rows")
log(f"  air_quality_context_dpr2019.csv: {len(aq_ctx_clean)} rows")
log(f"  geography_cleaned.csv: {len(geo_clean)} rows")
log(f"  traffic_master_SYNTHETIC (NOT processed): {len(synth_full)} rows")

log("\nAll cleaning operations completed successfully.")
log(f"Timestamp: {datetime.now().isoformat()}")
