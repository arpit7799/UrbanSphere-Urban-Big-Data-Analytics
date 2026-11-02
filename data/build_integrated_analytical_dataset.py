#!/usr/bin/env python3
"""
UrbanSphere — Canonical Multi-Domain Integration Pipeline
=========================================================
Integrates the four canonical datasets (Weather/AQI, Traffic, Air Quality, Geography)
on (timestamp, location_name) and saves optimized Parquet analytical datasets.

Key Rules Followed:
- Explicit provenance: weather_aqi vs air_quality_aqi.
- Validates 1:1 join cardinality.
- Checks row count preservation across all joins.
- Exports hourly integrated dataset and daily aggregated analytical dataset.
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed" / "integrated"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("=" * 60)
    print("UrbanSphere — Multi-Domain Integration Pipeline")
    print("=" * 60)

    weather_path = DATA_DIR / "dataset_weather_gurugram_with_aqi.csv"
    traffic_path = DATA_DIR / "dataset_traffic_gurugram.csv"
    air_path = DATA_DIR / "dataset_air_quality_gurugram.csv"
    geo_path = DATA_DIR / "dataset_geography_gurugram.csv"

    print("1. Loading raw canonical datasets...")
    df_w = pd.read_csv(weather_path)
    df_t = pd.read_csv(traffic_path)
    df_a = pd.read_csv(air_path)
    df_g = pd.read_csv(geo_path)

    initial_counts = {
        "weather": len(df_w),
        "traffic": len(df_t),
        "air_quality": len(df_a),
        "geography": len(df_g)
    }
    print(f"  Weather rows:     {initial_counts['weather']}")
    print(f"  Traffic rows:     {initial_counts['traffic']}")
    print(f"  Air Quality rows: {initial_counts['air_quality']}")
    print(f"  Geography rows:   {initial_counts['geography']}")

    # 2. Preserve explicit provenance for independently generated AQI fields
    df_w = df_w.rename(columns={
        "aqi": "weather_aqi",
        "aqi_category": "weather_aqi_category"
    })
    
    df_a = df_a.rename(columns={
        "aqi": "air_quality_aqi",
        "aqi_category": "air_quality_aqi_category"
    })

    # Drop redundant coordinates from traffic and air quality (geography is single source of truth)
    df_t = df_t.drop(columns=["latitude", "longitude", "date", "hour"], errors="ignore")
    df_a = df_a.drop(columns=["latitude", "longitude", "date", "hour"], errors="ignore")

    # 3. Perform Joins with Cardinality Verification
    print("\n2. Executing joins on (timestamp, location_name)...")
    
    # Step A: Weather + Traffic
    df_wt = pd.merge(df_w, df_t, on=["timestamp", "location_name"], how="inner")
    print(f"  Weather + Traffic merged: {len(df_wt)} rows")
    if len(df_wt) != initial_counts["weather"]:
        print(f"  WARNING: Cardinality mismatch in Weather + Traffic join!")

    # Step B: + Air Quality
    df_wta = pd.merge(df_wt, df_a, on=["timestamp", "location_name"], how="inner")
    print(f"  + Air Quality merged:     {len(df_wta)} rows")
    if len(df_wta) != initial_counts["weather"]:
        print(f"  WARNING: Cardinality mismatch in Air Quality join!")

    # Step C: + Geography (on location_name)
    df_integrated = pd.merge(df_wta, df_g, on="location_name", how="inner")
    print(f"  + Geography merged:       {len(df_integrated)} rows")
    if len(df_integrated) != initial_counts["weather"]:
        print(f"  WARNING: Cardinality mismatch in Geography join!")

    # Convert timestamp
    df_integrated["timestamp"] = pd.to_datetime(df_integrated["timestamp"])
    df_integrated["year"] = df_integrated["timestamp"].dt.year
    df_integrated["month"] = df_integrated["timestamp"].dt.month
    df_integrated["day"] = df_integrated["timestamp"].dt.day
    df_integrated["is_weekend"] = df_integrated["timestamp"].dt.dayofweek.isin([5, 6])

    # 4. Save Hourly Integrated Parquet
    hourly_parquet_path = PROCESSED_DIR / "urban_integrated_hourly.parquet"
    df_integrated.to_parquet(hourly_parquet_path, index=False)
    print(f"\n✓ Saved Hourly Integrated Parquet: {hourly_parquet_path} ({hourly_parquet_path.stat().st_size / 1024 / 1024:.2f} MB)")

    # 5. Build Daily Aggregated Analytical Dataset
    print("\n3. Building daily integrated dataset...")
    df_daily = df_integrated.groupby(["date", "location_name"]).agg(
        # Weather
        temp_mean_c=("temperature_c", "mean"),
        temp_min_c=("temperature_c", "min"),
        temp_max_c=("temperature_c", "max"),
        humidity_mean_pct=("relative_humidity_pct", "mean"),
        wind_speed_mean_kmh=("wind_speed_kmh", "mean"),
        wind_speed_max_kmh=("wind_speed_kmh", "max"),
        surface_pressure_mean_hpa=("surface_pressure_hpa", "mean"),
        precipitation_total_mm=("precipitation_mm", "sum"),
        weather_aqi_mean=("weather_aqi", "mean"),
        
        # Traffic
        total_vehicles=("vehicle_count", "sum"),
        total_pcu=("total_pcu", "sum"),
        avg_speed_kmh=("average_speed_kmh", "mean"),
        peak_hour_vehicles=("vehicle_count", "max"),
        
        # Air Quality
        pm25_mean_ugm3=("pm25_ugm3", "mean"),
        pm10_mean_ugm3=("pm10_ugm3", "mean"),
        no2_mean_ugm3=("no2_ugm3", "mean"),
        so2_mean_ugm3=("so2_ugm3", "mean"),
        co_mean_mgm3=("co_mg_m3", "mean"),
        o3_mean_ugm3=("o3_ugm3", "mean"),
        air_quality_aqi_max=("air_quality_aqi", "max"),
        air_quality_aqi_mean=("air_quality_aqi", "mean"),
        
        # Metadata
        latitude=("latitude_x", "first"),
        longitude=("longitude_x", "first"),
        locality_type=("locality_type", "first"),
        representative_corridor=("representative_corridor", "first")
    ).reset_index()

    # Calculate derived diurnal range
    df_daily["temp_diurnal_range_c"] = np.round(df_daily["temp_max_c"] - df_daily["temp_min_c"], 2)

    # Classify CPCB Daily AQI Category from air_quality_aqi_max
    def get_aqi_category(val):
        if val <= 50: return "Good"
        elif val <= 100: return "Satisfactory"
        elif val <= 200: return "Moderate"
        elif val <= 300: return "Poor"
        elif val <= 400: return "Very Poor"
        else: return "Severe"
        
    df_daily["daily_aqi_category"] = df_daily["air_quality_aqi_max"].apply(get_aqi_category)

    daily_parquet_path = PROCESSED_DIR / "urban_integrated_daily.parquet"
    df_daily.to_parquet(daily_parquet_path, index=False)
    print(f"✓ Saved Daily Integrated Parquet:  {daily_parquet_path} ({daily_parquet_path.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"  Daily records: {len(df_daily)} (1096 days * 12 localities = 13,152)")

    # 6. Save Integration Metadata
    metadata = {
        "pipeline_version": "2.0.0-canonical-migration",
        "hourly_total_records": len(df_integrated),
        "daily_total_records": len(df_daily),
        "total_localities": df_integrated["location_name"].nunique(),
        "localities_list": sorted(df_integrated["location_name"].unique()),
        "columns_in_hourly": list(df_integrated.columns),
        "columns_in_daily": list(df_daily.columns),
        "timestamp_start": str(df_integrated["timestamp"].min()),
        "timestamp_end": str(df_integrated["timestamp"].max()),
        "aqi_provenance_handling": "Preserved both weather_aqi and air_quality_aqi explicitly without overwriting."
    }

    with open(PROCESSED_DIR / "integration_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Saved Integration Metadata:      {PROCESSED_DIR / 'integration_metadata.json'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
