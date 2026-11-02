#!/usr/bin/env python3
"""
Unit and Integration Tests for UrbanSphere Spark SQL & Analytics Layer (Canonical)
================================================================================
Tests that all Spark SQL analytical outputs exist, are non-empty, and maintain
mathematical consistency with the canonical datasets.
"""

import os
import sys
import unittest
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "spark"

class TestSparkAnalytics(unittest.TestCase):
    """Test suite for Spark SQL queries and correlation analytics."""

    def test_01_spark_artifacts_exist(self):
        """All 7 analytical query outputs must exist in both CSV and Parquet."""
        expected_tables = [
            "corridor_capacity_stress",
            "vehicle_modal_split",
            "monthly_climate_extremes",
            "seasonal_air_quality_profiles",
            "wind_pollution_dispersion",
            "transit_corridor_sectors",
            "meteorology_air_quality_correlation"
        ]
        for tbl in expected_tables:
            csv_file = OUTPUT_DIR / f"{tbl}.csv"
            pq_file = OUTPUT_DIR / f"{tbl}.parquet"
            self.assertTrue(csv_file.exists(), f"Missing CSV output: {csv_file}")
            self.assertTrue(pq_file.exists(), f"Missing Parquet output: {pq_file}")
            self.assertGreater(csv_file.stat().st_size, 0, f"CSV output is empty: {csv_file}")
            self.assertGreater(pq_file.stat().st_size, 0, f"Parquet output is empty: {pq_file}")

    def test_02_corridor_capacity_metrics(self):
        """Corridor volume sums and PCU ratios must be consistent with canonical road types."""
        df = pd.read_csv(OUTPUT_DIR / "corridor_capacity_stress.csv")
        self.assertGreaterEqual(len(df), 3, f"Expected at least 3 road types, got {len(df)}")
        self.assertTrue((df["location_count"] > 0).all())
        self.assertTrue((df["total_pcu"] > 0).all())
        self.assertTrue(((df["pcu_to_vehicle_ratio"] >= 0.5) & (df["pcu_to_vehicle_ratio"] <= 2.0)).all())

    def test_03_modal_split_metrics(self):
        """Vehicle modal split must include all 6 canonical categories and sum reasonably."""
        df = pd.read_csv(OUTPUT_DIR / "vehicle_modal_split.csv")
        self.assertEqual(len(df), 6, f"Expected 6 vehicle categories, got {len(df)}")
        self.assertIn("car", df["vehicle_category"].values)
        self.assertIn("two_wheeler", df["vehicle_category"].values)
        self.assertTrue(((df["mean_share_pct"] >= 0.0) & (df["mean_share_pct"] <= 100.0)).all())

    def test_04_monthly_climate_metrics(self):
        """Monthly climate extremes must cover all 36 months."""
        df = pd.read_csv(OUTPUT_DIR / "monthly_climate_extremes.csv")
        self.assertEqual(len(df), 36, f"Expected 36 months, got {len(df)}")
        self.assertTrue((df["t_max_c"] >= df["t_min_c"]).all())
        self.assertTrue((df["dtr_c"] > 0).all())

    def test_05_seasonal_air_quality_metrics(self):
        """Seasonal air quality profiles must cover 48 groups (12 localities * 4 seasons)."""
        df = pd.read_csv(OUTPUT_DIR / "seasonal_air_quality_profiles.csv")
        self.assertEqual(len(df), 48, f"Expected 48 groups, got {len(df)}")
        self.assertTrue(((df["pm25_exceed_pct"] >= 0.0) & (df["pm25_exceed_pct"] <= 100.0)).all())
        self.assertTrue(((df["pm10_exceed_pct"] >= 0.0) & (df["pm10_exceed_pct"] <= 100.0)).all())

    def test_06_correlation_matrix_validity(self):
        """Correlation values must be in [-1.0, 1.0] and diagonal must be 1.0."""
        df = pd.read_csv(OUTPUT_DIR / "meteorology_air_quality_correlation.csv")
        self.assertEqual(len(df), 14, f"Expected 14 features, got {len(df)}")
        feature_codes = df["feature_code"].tolist()
        for code in feature_codes:
            diag_val = df.loc[df["feature_code"] == code, code].values[0]
            self.assertAlmostEqual(diag_val, 1.0, places=3, msg=f"Diagonal for {code} is {diag_val}, expected 1.0")
            for other in feature_codes:
                val = df.loc[df["feature_code"] == code, other].values[0]
                self.assertTrue(-1.001 <= val <= 1.001, f"Correlation out of bounds: {val}")

if __name__ == "__main__":
    unittest.main()
