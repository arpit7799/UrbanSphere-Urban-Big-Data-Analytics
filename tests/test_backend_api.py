#!/usr/bin/env python3
"""
UrbanSphere — Backend API Integration Test Suite (Canonical 2022-2024)
=====================================================================
Validates that all FastAPI endpoints return HTTP 200, valid schemas,
and accurate data aggregated from Spark, MapReduce, and Scikit-Learn.
"""

import sys
from pathlib import Path
import unittest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.main import app

class TestBackendAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_root_endpoint(self):
        """GET /api must return platform metadata and API sitemap."""
        res = self.client.get("/api")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["platform"], "UrbanSphere — Urban Big Data Analytics Platform")
        self.assertIn("endpoints", data)
        self.assertIn("/api/v1/health", data["endpoints"]["health"])

    def test_02_health_and_metadata(self):
        """GET /api/v1/health and /api/v1/metadata/summary must report operational status."""
        res_h = self.client.get("/api/v1/health")
        self.assertEqual(res_h.status_code, 200)
        data_h = res_h.json()
        self.assertEqual(data_h["status"], "healthy")

        res_m = self.client.get("/api/v1/metadata/summary")
        self.assertEqual(res_m.status_code, 200)
        data_m = res_m.json()
        self.assertEqual(data_m["total_records"], 315648)

    def test_03_traffic_endpoints(self):
        """Traffic endpoints must return corridor stress, modal split, and 12 localities."""
        res_c = self.client.get("/api/v1/traffic/corridors")
        self.assertEqual(res_c.status_code, 200)
        data_c = res_c.json()
        self.assertGreaterEqual(data_c["total_records"], 3)

        res_m = self.client.get("/api/v1/traffic/modal-split")
        self.assertEqual(res_m.status_code, 200)
        data_m = res_m.json()
        self.assertEqual(data_m["total_records"], 6)

        res_l = self.client.get("/api/v1/traffic/locations")
        self.assertEqual(res_l.status_code, 200)
        data_l = res_l.json()
        self.assertEqual(data_l["total_records"], 12)

    def test_04_weather_endpoints(self):
        """Weather endpoints must return monthly climate extremes and wind dispersion."""
        res_w = self.client.get("/api/v1/weather/monthly")
        self.assertEqual(res_w.status_code, 200)
        data_w = res_w.json()
        self.assertEqual(data_w["total_records"], 36)

        res_d = self.client.get("/api/v1/weather/wind-dispersion")
        self.assertEqual(res_d.status_code, 200)
        data_d = res_d.json()
        self.assertGreaterEqual(data_d["total_records"], 2)

    def test_05_air_quality_endpoints(self):
        """Air quality endpoints must return seasonal profiles and daily timeline."""
        res_s = self.client.get("/api/v1/air-quality/seasonal")
        self.assertEqual(res_s.status_code, 200)
        data_s = res_s.json()
        self.assertEqual(data_s["total_records"], 48)  # 12 localities * 4 seasons

        res_t = self.client.get("/api/v1/air-quality/daily-timeline?limit=10&offset=0")
        self.assertEqual(res_t.status_code, 200)
        data_t = res_t.json()
        self.assertEqual(data_t["total_records"], 13152)
        self.assertEqual(len(data_t["data"]), 10)

    def test_06_predict_aqi_endpoint(self):
        """POST /api/v1/predict/aqi must return valid predictions and disclaimers."""
        payload = {
            "temp_min_c": 9.5,
            "temp_max_c": 21.0,
            "temp_mean_c": 14.5,
            "humidity_mean_pct": 78.0,
            "precipitation_total_mm": 0.0,
            "surface_pressure_mean_hpa": 1008.0,
            "wind_speed_mean_kmh": 6.5,
            "wind_speed_max_kmh": 12.0,
            "month": 12
        }
        res = self.client.post("/api/v1/predict/aqi", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn(data["predicted_aqi_category"], ["Severe", "Very Poor", "Poor", "Moderate", "Satisfactory", "Good"])
        self.assertIn("class_probabilities", data)
        self.assertGreater(len(data["top_weather_drivers"]), 0)
        self.assertIn("Scientific Caution", data["scientific_disclaimer"])

    def test_07_predict_regime_endpoint(self):
        """POST /api/v1/predict/regime must classify 6 pollutants into K=3 regime."""
        payload = {
            "pm25": 45.0,
            "pm10": 85.0,
            "no2": 25.0,
            "so2": 12.0,
            "co": 0.7,
            "o3": 40.0
        }
        res = self.client.post("/api/v1/predict/regime", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn(data["cluster_id"], [0, 1, 2])
        self.assertIn(data["regime_name"], [
            "Low_Pollution_Monsoon_Regime",
            "Moderate_Photochemical_Regime",
            "Severe_Inversion_Winter_Smog_Regime"
        ])

    def test_08_analytics_endpoints(self):
        """Analytics endpoints must return clusters, anomalies, and correlations."""
        res_c = self.client.get("/api/v1/analytics/clusters")
        self.assertEqual(res_c.status_code, 200)
        data_c = res_c.json()
        self.assertEqual(len(data_c["data"]["regime_profiles"]), 3)

        res_a = self.client.get("/api/v1/analytics/anomalies?limit=20")
        self.assertEqual(res_a.status_code, 200)
        data_a = res_a.json()
        self.assertEqual(data_a["total_records"], 658)

        res_corr = self.client.get("/api/v1/analytics/correlations")
        self.assertEqual(res_corr.status_code, 200)
        data_corr = res_corr.json()
        self.assertGreater(data_corr["total_records"], 20)

    def test_09_geography_endpoints(self):
        """Geography endpoints must return 12 localities and corridors."""
        res_s = self.client.get("/api/v1/geography/sectors")
        self.assertEqual(res_s.status_code, 200)
        data_s = res_s.json()
        self.assertEqual(data_s["total_records"], 12)

        res_c = self.client.get("/api/v1/geography/corridors")
        self.assertEqual(res_c.status_code, 200)
        data_c = res_c.json()
        self.assertGreaterEqual(data_c["total_records"], 5)

if __name__ == "__main__":
    unittest.main()
