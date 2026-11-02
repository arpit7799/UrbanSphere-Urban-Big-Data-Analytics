#!/usr/bin/env python3
"""
UrbanSphere — PySpark Distributed SQL Analytics Runner
======================================================
Loads canonical datasets, registers Spark temporary views, executes
analytical SQL queries, and exports analytical result tables to output/spark/.
"""

import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed" / "integrated"
OUTPUT_DIR = PROJECT_ROOT / "output" / "spark"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_spark_session():
    """Initialize an optimized local SparkSession."""
    return (
        SparkSession.builder
        .appName("UrbanSphere_Spark_SQL_Analytics")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.driver.memory", "2g")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

def load_tables(spark):
    """Load canonical tables and register Temporary Views."""
    csv_tables = {
        "traffic": DATA_DIR / "dataset_traffic_gurugram.csv",
        "weather": DATA_DIR / "dataset_weather_gurugram_with_aqi.csv",
        "air_quality": DATA_DIR / "dataset_air_quality_gurugram.csv",
        "geography": DATA_DIR / "dataset_geography_gurugram.csv"
    }
    
    print("\n" + "=" * 60)
    print("Loading Canonical Tables into Spark Catalog...")
    print("=" * 60)
    
    for name, path in csv_tables.items():
        if not path.exists():
            raise FileNotFoundError(f"Canonical table not found: {path}")
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(str(path))
        df.createOrReplaceTempView(name)
        print(f"  ✓ Registered CSV view: '{name}' ({df.count()} rows, {len(df.columns)} cols)")

    daily_path = PROCESSED_DIR / "urban_integrated_daily.parquet"
    if daily_path.exists():
        df_daily = spark.read.parquet(str(daily_path))
        df_daily.createOrReplaceTempView("urban_daily")
        print(f"  ✓ Registered Parquet view: 'urban_daily' ({df_daily.count()} rows, {len(df_daily.columns)} cols)")

def save_output(df, name):
    """Save PySpark DataFrame results as both CSV and Parquet."""
    pdf = df.toPandas()
    csv_path = OUTPUT_DIR / f"{name}.csv"
    pq_path = OUTPUT_DIR / f"{name}.parquet"
    
    pdf.to_csv(csv_path, index=False)
    pdf.to_parquet(pq_path, index=False)
    print(f"  ✓ Exported: {csv_path.name} ({len(pdf)} rows)")

def run_analytics(spark):
    sql_path = Path(__file__).resolve().parent / "queries.sql"
    with open(sql_path, "r") as f:
        full_sql = f.read()

    # Split SQL file into discrete queries by stripping comments
    raw_queries = full_sql.split(";")
    clean_queries = []
    for q in raw_queries:
        lines = [l for l in q.splitlines() if not l.strip().startswith("--")]
        cq = "\n".join(lines).strip()
        if cq:
            clean_queries.append(cq)

    query_targets = [
        ("corridor_capacity_stress", "Query 1: Corridor Volume & Road Type Analysis"),
        ("vehicle_modal_split", "Query 2: Vehicle Fleet Composition & Modal Split"),
        ("monthly_climate_extremes", "Query 3: Monthly Climate Extremes & DTR"),
        ("seasonal_air_quality_profiles", "Query 4: Seasonal Air Quality & NAAQS Profiles"),
        ("wind_pollution_dispersion", "Query 5: Atmospheric Ventilation & Wind Dispersion"),
        ("transit_corridor_sectors", "Query 6: Spatial Typology & Corridor Sectors")
    ]

    print("\n" + "=" * 60)
    print("Executing Spark SQL Analytical Queries...")
    print("=" * 60)

    for i, (out_name, desc) in enumerate(query_targets):
        if i >= len(clean_queries):
            break
        q_sql = clean_queries[i]
        print(f"\n--- [{i+1}/6] {desc} ---")
        df_res = spark.sql(q_sql)
        df_res.show(5, truncate=False)
        save_output(df_res, out_name)

def main():
    print("Initializing Apache Spark Engine for UrbanSphere...")
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("ERROR")
    
    try:
        load_tables(spark)
        run_analytics(spark)
        print("\n" + "=" * 60)
        print("✓ PySpark SQL Analytics Pipeline Completed Successfully!")
        print("=" * 60)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
