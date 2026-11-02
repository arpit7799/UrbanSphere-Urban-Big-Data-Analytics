#!/usr/bin/env python3
"""
UrbanSphere Data Platform — Canonical Data Integrity Test Suite
================================================================
Validates the four authoritative canonical datasets, mathematical invariants,
geographic mappings, integrated datasets, and structural constraints.
"""

import os
import unittest
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
INTEGRATED_DIR = os.path.join(DATA_DIR, "processed", "integrated")

class TestCanonicalDataIntegrity(unittest.TestCase):
    """Test suite for UrbanSphere canonical datasets and data pipeline."""

    @classmethod
    def setUpClass(cls):
        cls.weather_path = os.path.join(DATA_DIR, "dataset_weather_gurugram_with_aqi.csv")
        cls.traffic_path = os.path.join(DATA_DIR, "dataset_traffic_gurugram.csv")
        cls.aq_path = os.path.join(DATA_DIR, "dataset_air_quality_gurugram.csv")
        cls.geo_path = os.path.join(DATA_DIR, "dataset_geography_gurugram.csv")
        cls.hourly_parquet = os.path.join(INTEGRATED_DIR, "urban_integrated_hourly.parquet")
        cls.daily_parquet = os.path.join(INTEGRATED_DIR, "urban_integrated_daily.parquet")

    def test_01_canonical_files_exist_and_dimensions(self):
        """Verify the 4 canonical CSV files exist with exact expected dimensions."""
        self.assertTrue(os.path.exists(self.weather_path), "Weather CSV missing")
        self.assertTrue(os.path.exists(self.traffic_path), "Traffic CSV missing")
        self.assertTrue(os.path.exists(self.aq_path), "Air quality CSV missing")
        self.assertTrue(os.path.exists(self.geo_path), "Geography CSV missing")

        geo_df = pd.read_csv(self.geo_path)
        self.assertEqual(len(geo_df), 12, "Geography must have exactly 12 records")
        self.assertEqual(len(geo_df.columns), 11, "Geography must have 11 columns")

        # Fast line count check for the large 315,648 row files
        for p, expected_rows, expected_cols in [
            (self.weather_path, 315648, 15),
            (self.traffic_path, 315648, 18),
            (self.aq_path, 315648, 14),
        ]:
            sample = pd.read_csv(p, nrows=5)
            self.assertEqual(len(sample.columns), expected_cols, f"{os.path.basename(p)} column count mismatch")
            with open(p, "rb") as f:
                lines = sum(1 for _ in f) - 1 # exclude header
            self.assertEqual(lines, expected_rows, f"{os.path.basename(p)} row count mismatch")

    def test_02_geography_localities_mapping(self):
        """Geography must define 12 unique localities with coordinates in Gurugram bounding box."""
        geo_df = pd.read_csv(self.geo_path)
        self.assertEqual(geo_df["location_id"].nunique(), 12)
        self.assertEqual(geo_df["location_name"].nunique(), 12)
        self.assertTrue(((geo_df["latitude"] >= 28.3) & (geo_df["latitude"] <= 28.6)).all())
        self.assertTrue(((geo_df["longitude"] >= 76.8) & (geo_df["longitude"] <= 77.2)).all())

        # Check hourly locality names map 1:1 to geography
        geo_names = set(geo_df["location_name"])
        for p in [self.weather_path, self.traffic_path, self.aq_path]:
            # Read unique location_names
            locs = pd.read_csv(p, usecols=["location_name"])["location_name"].unique()
            self.assertEqual(set(locs), geo_names, f"Localities in {os.path.basename(p)} do not match geography")

    def test_03_traffic_invariants(self):
        """Traffic vehicle categories must sum exactly to vehicle_count with nonnegative counts and speeds."""
        # Read a representative chunk to verify invariant
        df = pd.read_csv(self.traffic_path, nrows=50000)
        cat_sum = (
            df["two_wheeler_count"]
            + df["car_count"]
            + df["auto_rickshaw_count"]
            + df["bus_count"]
            + df["truck_count"]
            + df["other_vehicle_count"]
        )
        diff = (cat_sum - df["vehicle_count"]).abs().sum()
        self.assertEqual(diff, 0, "Vehicle category breakdown does not sum to vehicle_count")
        self.assertTrue((df["vehicle_count"] >= 0).all(), "Negative vehicle count found")
        self.assertTrue((df["total_pcu"] >= 0).all(), "Negative total_pcu found")
        self.assertTrue(((df["average_speed_kmh"] >= 0) & (df["average_speed_kmh"] <= 120)).all(), "Speed outside bounds")

    def test_04_weather_invariants(self):
        """Weather variables must adhere to realistic meteorological ranges."""
        df = pd.read_csv(self.weather_path, nrows=50000)
        self.assertTrue(((df["temperature_c"] >= -5) & (df["temperature_c"] <= 55)).all())
        self.assertTrue(((df["relative_humidity_pct"] >= 0) & (df["relative_humidity_pct"] <= 100)).all())
        self.assertTrue(((df["surface_pressure_hpa"] >= 900) & (df["surface_pressure_hpa"] <= 1050)).all())
        self.assertTrue((df["wind_speed_kmh"] >= 0).all())
        self.assertTrue((df["precipitation_mm"] >= 0).all())

    def test_05_air_quality_invariants(self):
        """Pollutants must be nonnegative, PM10 >= PM2.5, and AQI within standard range."""
        df = pd.read_csv(self.aq_path, nrows=50000)
        for pol in ["pm25_ugm3", "pm10_ugm3", "no2_ugm3", "so2_ugm3", "co_mg_m3", "o3_ugm3"]:
            self.assertTrue((df[pol] >= 0).all(), f"Negative values found in {pol}")
        self.assertTrue((df["pm10_ugm3"] >= df["pm25_ugm3"]).all(), "PM10 < PM2.5 violation found")
        self.assertTrue(((df["aqi"] >= 0) & (df["aqi"] <= 500)).all(), "AQI outside 0-500 scale")

    def test_06_timestamp_coverage(self):
        """Verify timestamp range covers 2022-01-01 00:00 to 2024-12-31 23:00."""
        # Read head and tail
        head = pd.read_csv(self.traffic_path, nrows=12)
        self.assertEqual(head["timestamp"].iloc[0], "2022-01-01 00:00:00")
        tail = pd.read_csv(self.traffic_path, skiprows=315648 - 12 + 1, header=None)
        self.assertTrue("2024-12-31 23:00:00" in tail[0].values)

    def test_07_integrated_datasets_and_aqi_provenance(self):
        """Integrated parquet datasets must exist, maintain 1:1 join integrity, and preserve dual AQI."""
        self.assertTrue(os.path.exists(self.hourly_parquet), "Hourly integrated parquet missing")
        self.assertTrue(os.path.exists(self.daily_parquet), "Daily integrated parquet missing")

        # Check hourly parquet schema and counts
        h_df = pd.read_parquet(self.hourly_parquet, columns=["weather_aqi", "air_quality_aqi", "location_name"])
        self.assertEqual(len(h_df), 315648, "Integrated hourly parquet row count mismatch")
        self.assertIn("weather_aqi", h_df.columns, "weather_aqi column missing")
        self.assertIn("air_quality_aqi", h_df.columns, "air_quality_aqi column missing")

        # Check daily parquet counts
        d_df = pd.read_parquet(self.daily_parquet)
        self.assertEqual(len(d_df), 13152, "Integrated daily parquet row count mismatch")

    def test_08_no_obsolete_raw_or_backup_directories(self):
        """Verify obsolete raw/backup/benchmark directories have been removed per user policy."""
        for d in ["raw", "backup", "benchmark", "backup_pre_remediation"]:
            p = os.path.join(DATA_DIR, d)
            self.assertFalse(os.path.exists(p), f"Obsolete directory {d} should not exist under data/")

if __name__ == "__main__":
    unittest.main()
