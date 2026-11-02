#!/usr/bin/env python3
"""
UrbanSphere — Machine Learning & Analytics Test Suite (Canonical)
=================================================================
Validates model bundles, evaluation metrics, defensibility invariants,
and output analytical datasets for:
1. AQI Category Classification (Random Forest vs Baseline)
2. Atmospheric Pollution Regime Clustering (K-Means, K=3)
3. Acute Atmospheric Anomaly Detection (Isolation Forest & Z-Scores)
4. Statistical Correlations & Significance Testing (Pearson & Spearman)
"""

import json
from pathlib import Path
import unittest
import joblib
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "output" / "models"
ANALYTICS_DIR = PROJECT_ROOT / "output" / "analytics"

class TestMachineLearningLayer(unittest.TestCase):
    
    # -------------------------------------------------------------------------
    # 1. AQI Classification Tests
    # -------------------------------------------------------------------------
    def test_01_classification_model_and_scaler_loadable(self):
        """Model bundle and feature scaler must exist and be loadable with joblib."""
        rf_path = MODEL_DIR / "aqi_classifier_rf.joblib"
        scaler_path = MODEL_DIR / "aqi_scaler.joblib"
        
        self.assertTrue(rf_path.exists(), f"Missing model: {rf_path}")
        self.assertTrue(scaler_path.exists(), f"Missing scaler: {scaler_path}")
        
        model = joblib.load(rf_path)
        scaler = joblib.load(scaler_path)
        
        self.assertIsNotNone(model)
        self.assertIsNotNone(scaler)
        self.assertGreaterEqual(len(model.classes_), 4)

    def test_02_classification_metrics_and_baseline_comparison(self):
        """Classification metrics must show Random Forest outperforms Dummy baseline."""
        metrics_path = MODEL_DIR / "classification_metrics.json"
        self.assertTrue(metrics_path.exists(), f"Missing metrics: {metrics_path}")
        
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
        dummy_acc = metrics["dummy_baseline_accuracy"]
        rf_cv_acc = metrics["stratified_5fold_accuracy"]
        test_acc = metrics["holdout_test_accuracy"]
        
        self.assertGreater(rf_cv_acc, dummy_acc, "RF CV accuracy must outperform baseline")
        self.assertGreater(test_acc, 0.70, "Holdout accuracy must exceed 70% for defensibility")
        self.assertIn("timeseries_split_accuracy", metrics, "Must include TimeSeriesSplit for temporal evaluation")

    # -------------------------------------------------------------------------
    # 2. Multi-Pollutant Clustering Tests
    # -------------------------------------------------------------------------
    def test_03_weather_feature_importances(self):
        """Feature importances must rank physical drivers (temperature, humidity) at top."""
        fi_path = ANALYTICS_DIR / "weather_feature_importances.csv"
        self.assertTrue(fi_path.exists(), f"Missing file: {fi_path}")
        
        df_fi = pd.read_csv(fi_path)
        self.assertGreaterEqual(len(df_fi), 6)
        
        self.assertAlmostEqual(df_fi["importance"].sum(), 1.0, places=2)
        top_features = df_fi.head(3)["feature"].tolist()
        has_primary_driver = any(f in top_features for f in ["temp_mean_c", "temp_min_c", "temp_max_c", "humidity_mean_pct"])
        self.assertTrue(has_primary_driver, "Top feature importances must include a key meteorological driver")

    def test_04_clustering_model_and_profiles(self):
        """K-Means clustering must have K=3, silhouette > 0.40, and valid regime profiles."""
        km_path = MODEL_DIR / "pollution_kmeans.joblib"
        metrics_path = MODEL_DIR / "clustering_metrics.json"
        profiles_path = ANALYTICS_DIR / "pollution_cluster_profiles.csv"
        
        self.assertTrue(km_path.exists())
        self.assertTrue(metrics_path.exists())
        self.assertTrue(profiles_path.exists())
        
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
        self.assertEqual(metrics["optimal_k"], 3)
        self.assertGreater(metrics["silhouette_score"], 0.40)
        
        df_prof = pd.read_csv(profiles_path)
        self.assertEqual(len(df_prof), 3)
        
        pm25_sorted = df_prof.sort_values("avg_pm25")
        self.assertEqual(pm25_sorted.iloc[0]["regime_name"], "Low_Pollution_Monsoon_Regime")
        self.assertEqual(pm25_sorted.iloc[-1]["regime_name"], "Severe_Inversion_Winter_Smog_Regime")

    # -------------------------------------------------------------------------
    # 3. Anomaly Detection Tests
    # -------------------------------------------------------------------------
    def test_05_anomaly_detection_outputs(self):
        """Anomaly detection must flag ~5% outliers and produce categorized phenotypes."""
        anom_path = ANALYTICS_DIR / "pollution_anomalies.csv"
        metrics_path = MODEL_DIR / "anomaly_detection_metrics.json"
        
        self.assertTrue(anom_path.exists())
        self.assertTrue(metrics_path.exists())
        
        df_anom = pd.read_csv(anom_path)
        self.assertEqual(len(df_anom), 13152)
        
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
        iso_rate = metrics["isolation_forest_count"] / metrics["total_days_analyzed"]
        self.assertAlmostEqual(iso_rate, 0.05, places=2)
        
        phenotypes = set(df_anom["anomaly_phenotype"].unique())
        self.assertIn("Post_Monsoon_Biomass_Firework_Smog_Shock", phenotypes)
        self.assertIn("Severe_Winter_Inversion_Stagnation", phenotypes)

    # -------------------------------------------------------------------------
    # 4. Statistical Significance Tests
    # -------------------------------------------------------------------------
    def test_06_statistical_correlations_validity(self):
        """Correlations must have bounded r in [-1, 1] and valid p-values in [0, 1]."""
        corr_path = ANALYTICS_DIR / "statistical_correlations_with_pvalues.csv"
        self.assertTrue(corr_path.exists())
        
        df_corr = pd.read_csv(corr_path)
        self.assertGreater(len(df_corr), 20)
        
        self.assertTrue((df_corr["pearson_r"] >= -1.0).all())
        self.assertTrue((df_corr["pearson_r"] <= 1.0).all())
        self.assertTrue((df_corr["spearman_rho"] >= -1.0).all())
        self.assertTrue((df_corr["spearman_rho"] <= 1.0).all())
        self.assertTrue((df_corr["pearson_p_value"] >= 0.0).all())
        self.assertTrue((df_corr["pearson_p_value"] <= 1.0).all())
        
        temp_pm25 = df_corr[(df_corr["weather_variable"] == "temp_mean_c") & 
                            (df_corr["pollutant_variable"] == "pm25_mean_ugm3")]
        self.assertEqual(len(temp_pm25), 1)
        r_val = temp_pm25.iloc[0]["pearson_r"]
        self.assertLess(r_val, -0.4, "Temperature must exhibit strong inverse correlation with PM2.5")

if __name__ == "__main__":
    unittest.main()
