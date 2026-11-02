"""
UrbanSphere — Comprehensive Frontend & Backend Integration Test Suite
Verifies all static frontend assets, views, and FastAPI backend endpoints.
"""

from pathlib import Path
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_frontend_static_serving():
    # 1. Main index
    r = client.get("/")
    assert r.status_code == 200
    assert "<!DOCTYPE html>" in r.text
    assert "UrbanSphere" in r.text
    assert "Overview" in r.text
    print("✓ GET / (Dashboard Index): 200 OK")

    # 2. Dashboard alias
    r = client.get("/dashboard/")
    assert r.status_code == 200
    assert "<!DOCTYPE html>" in r.text
    print("✓ GET /dashboard/: 200 OK")

    # 3. CSS files
    for css in ["/css/main.css", "/css/components.css"]:
        r = client.get(css)
        assert r.status_code == 200
        assert len(r.text) > 100
        print(f"✓ GET {css}: 200 OK ({len(r.text)} chars)")

    # 4. JS modules
    js_modules = [
        "/js/app.js",
        "/js/api.js",
        "/js/charts.js",
        "/js/map.js",
        "/js/views/overview.js",
        "/js/views/traffic.js",
        "/js/views/air_quality.js",
        "/js/views/weather.js",
        "/js/views/geography.js",
        "/js/views/analytics.js",
        "/js/views/explorer.js",
        "/js/views/reports.js"
    ]
    for js in js_modules:
        r = client.get(js)
        assert r.status_code == 200, f"Failed to load {js}"
        assert len(r.text) > 50
        print(f"✓ GET {js}: 200 OK ({len(r.text)} chars)")

    # 5. Night image asset
    r = client.get("/public/images/gurugram_night.jpg")
    assert r.status_code == 200
    assert len(r.content) > 100000  # ~1MB image
    print(f"✓ GET /public/images/gurugram_night.jpg: 200 OK ({len(r.content):,} bytes)")


def test_backend_analytical_endpoints():
    endpoints = [
        ("/api", "API Index Metadata"),
        ("/api/v1/health", "System Health"),
        ("/api/v1/metadata/summary", "Project Metadata Summary"),
        ("/api/v1/geography/sectors", "12 Gurugram Localities"),
        ("/api/v1/geography/corridors", "Transit Corridors"),
        ("/api/v1/traffic/corridors", "Corridor Capacity Stress"),
        ("/api/v1/traffic/modal-split", "Vehicle Modal Split"),
        ("/api/v1/traffic/locations", "Traffic Localities"),
        ("/api/v1/weather/monthly", "Monthly Climate Extremes"),
        ("/api/v1/weather/wind-dispersion", "Wind Pollution Dispersion"),
        ("/api/v1/air-quality/seasonal", "Seasonal Air Quality Profiles"),
        ("/api/v1/air-quality/daily-timeline?limit=10", "Daily Integrated Timeline"),
        ("/api/v1/analytics/clusters", "K-Means Multi-Pollutant Regimes"),
        ("/api/v1/analytics/anomalies?limit=10", "Isolation Forest Atmospheric Outliers"),
        ("/api/v1/analytics/correlations", "Statistical Correlations with p-values"),
        ("/api/v1/analytics/feature-importances", "Weather Feature Importances")
    ]

    for ep, desc in endpoints:
        r = client.get(ep)
        assert r.status_code == 200, f"Failed on {ep}: {r.status_code}"
        data = r.json()
        print(f"✓ GET {ep:40s} -> 200 OK ({desc})")


def test_ml_inference_endpoints():
    # 1. Random Forest AQI Prediction
    payload_aqi = {
        "temp_min_c": 11.2,
        "temp_max_c": 22.4,
        "temp_mean_c": 16.8,
        "humidity_mean_pct": 72.0,
        "precipitation_total_mm": 0.0,
        "surface_pressure_mean_hpa": 1012.0,
        "wind_speed_mean_kmh": 8.5,
        "wind_speed_max_kmh": 14.0,
        "month": 12
    }
    r = client.post("/api/v1/predict/aqi", json=payload_aqi)
    assert r.status_code == 200
    res = r.json()
    assert "predicted_aqi_category" in res
    assert "confidence" in res
    assert "class_probabilities" in res
    assert "top_weather_drivers" in res
    print(f"✓ POST /api/v1/predict/aqi -> 200 OK (Category: {res['predicted_aqi_category']}, Conf: {res['confidence']:.2f})")

    # 2. K-Means Pollution Regime Prediction
    payload_regime = {
        "pm25": 145.0,
        "pm10": 260.0,
        "no2": 65.0,
        "so2": 14.0,
        "co": 1.1,
        "o3": 32.0
    }
    r = client.post("/api/v1/predict/regime", json=payload_regime)
    assert r.status_code == 200
    res = r.json()
    assert "cluster_id" in res
    assert "regime_name" in res
    assert "cluster_description" in res
    print(f"✓ POST /api/v1/predict/regime -> 200 OK (Cluster #{res['cluster_id']}: {res['regime_name']})")


if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING URBANSPHERE FRONTEND & BACKEND INTEGRATION TEST SUITE")
    print("=" * 70)
    test_frontend_static_serving()
    print("-" * 70)
    test_backend_analytical_endpoints()
    print("-" * 70)
    test_ml_inference_endpoints()
    print("=" * 70)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

