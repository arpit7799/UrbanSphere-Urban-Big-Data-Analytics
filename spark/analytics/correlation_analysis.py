#!/usr/bin/env python3
"""
UrbanSphere — Multi-Domain Correlation & Dispersion Analytics
============================================================
Computes statistical Pearson correlation matrix between meteorological features,
traffic metrics, and air quality pollutants using PySpark on urban_integrated_daily.parquet.
Exports structured correlation matrix to output/spark/.
"""

from pathlib import Path
import pandas as pd
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "integrated"
OUTPUT_DIR = PROJECT_ROOT / "output" / "spark"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_spark_session():
    return (
        SparkSession.builder
        .appName("UrbanSphere_Correlation_Analytics")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.driver.memory", "2g")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

def main():
    print("=" * 60)
    print("Running Meteorological-Air Quality Correlation Analysis...")
    print("=" * 60)
    
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("ERROR")
    
    try:
        daily_path = PROCESSED_DIR / "urban_integrated_daily.parquet"
        df = spark.read.parquet(str(daily_path))
        print(f"Loaded daily integrated dataset: {df.count()} rows")
        
        feature_cols = [
            ("temp_mean_c", "Temperature (°C)"),
            ("humidity_mean_pct", "Humidity (%)"),
            ("wind_speed_mean_kmh", "Wind Speed (km/h)"),
            ("surface_pressure_mean_hpa", "Surface Pressure (hPa)"),
            ("precipitation_total_mm", "Precipitation (mm)"),
            ("pm25_mean_ugm3", "PM2.5 (ug/m3)"),
            ("pm10_mean_ugm3", "PM10 (ug/m3)"),
            ("no2_mean_ugm3", "NO2 (ug/m3)"),
            ("so2_mean_ugm3", "SO2 (ug/m3)"),
            ("co_mean_mgm3", "CO (mg/m3)"),
            ("o3_mean_ugm3", "Ozone (ug/m3)"),
            ("air_quality_aqi_max", "Air Quality Max AQI"),
            ("total_vehicles", "Total Daily Vehicles"),
            ("avg_speed_kmh", "Average Speed (km/h)")
        ]
        
        col_names = [c[0] for c in feature_cols]
        labels = [c[1] for c in feature_cols]
        
        corr_matrix = []
        for c1, l1 in feature_cols:
            row = {"feature": l1, "feature_code": c1}
            for c2, l2 in feature_cols:
                val = df.stat.corr(c1, c2)
                row[c2] = round(val, 4) if val is not None else 0.0
            corr_matrix.append(row)
            
        corr_df = pd.DataFrame(corr_matrix)
        
        print("\n--- Key Meteorological-Pollution Correlation Findings ---")
        for p in ["pm25_mean_ugm3", "pm10_mean_ugm3", "air_quality_aqi_max"]:
            row_p = corr_df[corr_df["feature_code"] == p].iloc[0]
            print(f"  • {row_p['feature']}:")
            print(f"      vs Wind Speed:        r = {row_p['wind_speed_mean_kmh']:+.3f} (Dispersion effect)")
            print(f"      vs Temperature:       r = {row_p['temp_mean_c']:+.3f} (Winter stagnation)")
            print(f"      vs Surface Pressure:  r = {row_p['surface_pressure_mean_hpa']:+.3f} (High pressure trap)")
            print(f"      vs Humidity:          r = {row_p['humidity_mean_pct']:+.3f}")
            
        csv_out = OUTPUT_DIR / "meteorology_air_quality_correlation.csv"
        pq_out = OUTPUT_DIR / "meteorology_air_quality_correlation.parquet"
        corr_df.to_csv(csv_out, index=False)
        corr_df.to_parquet(pq_out, index=False)
        print(f"\n✓ Exported Correlation Matrix: {csv_out.name} ({len(corr_df)}x{len(col_names)})")
        print("=" * 60)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
