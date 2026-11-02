"""
UrbanSphere — FastAPI Analytics Backend Application
===================================================
Exposes Big Data aggregations (MapReduce, Spark SQL) and Machine Learning models
(AQI Random Forest Classification, K-Means Clustering, Isolation Forest Anomaly Detection)
through performant REST API endpoints, and serves the interactive frontend dashboard.
"""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import router as health_router
from backend.app.api.traffic import router as traffic_router
from backend.app.api.weather import router as weather_router
from backend.app.api.air_quality import router as air_quality_router
from backend.app.api.predict import router as predict_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.geography import router as geography_router

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(
    title="UrbanSphere — Urban Big Data Analytics API",
    description=(
        "Production REST API for Gurugram Big Data Analytics Platform. "
        "Integrates Hadoop MapReduce outputs, PySpark SQL analytical aggregates, "
        "and Scikit-Learn Machine Learning models."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers under /api/v1
API_PREFIX = "/api/v1"
app.include_router(health_router, prefix=API_PREFIX)
app.include_router(traffic_router, prefix=API_PREFIX)
app.include_router(weather_router, prefix=API_PREFIX)
app.include_router(air_quality_router, prefix=API_PREFIX)
app.include_router(predict_router, prefix=API_PREFIX)
app.include_router(analytics_router, prefix=API_PREFIX)
app.include_router(geography_router, prefix=API_PREFIX)

@app.get("/api")
def api_root():
    return {
        "platform": "UrbanSphere — Urban Big Data Analytics Platform",
        "city": "Gurugram, Haryana, India",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": f"{API_PREFIX}/health",
            "metadata": f"{API_PREFIX}/metadata/summary",
            "traffic_corridors": f"{API_PREFIX}/traffic/corridors",
            "traffic_modal_split": f"{API_PREFIX}/traffic/modal-split",
            "weather_monthly": f"{API_PREFIX}/weather/monthly",
            "weather_wind_dispersion": f"{API_PREFIX}/weather/wind-dispersion",
            "air_quality_seasonal": f"{API_PREFIX}/air-quality/seasonal",
            "air_quality_daily_timeline": f"{API_PREFIX}/air-quality/daily-timeline",
            "predict_aqi": f"{API_PREFIX}/predict/aqi",
            "predict_regime": f"{API_PREFIX}/predict/regime",
            "analytics_clusters": f"{API_PREFIX}/analytics/clusters",
            "analytics_anomalies": f"{API_PREFIX}/analytics/anomalies",
            "analytics_correlations": f"{API_PREFIX}/analytics/correlations",
            "geography_sectors": f"{API_PREFIX}/geography/sectors"
        }
    }

# Mount static asset folders for dashboard
if (FRONTEND_DIR / "css").exists():
    app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
if (FRONTEND_DIR / "js").exists():
    app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")
if (FRONTEND_DIR / "public").exists():
    app.mount("/public", StaticFiles(directory=str(FRONTEND_DIR / "public")), name="public")

# Mount /dashboard as static directory
if FRONTEND_DIR.exists():
    app.mount("/dashboard", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="dashboard")

# Root endpoint serves index.html for web browsers, or JSON sitemap for API clients
@app.get("/")
def root(request: Request):
    accept = request.headers.get("accept", "")
    if "application/json" in accept and "text/html" not in accept:
        return api_root()
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return api_root()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
