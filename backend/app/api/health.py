from fastapi import APIRouter
from backend.app.schemas.common import HealthResponse, APIResponse

router = APIRouter(tags=["System & Metadata"])

@router.get("/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="healthy",
        app_name="UrbanSphere Big Data Analytics API",
        version="2.0.0",
        platform="macOS / Spark / Hadoop / Scikit-Learn",
        city="Gurugram (NCR), India",
        total_tests_passed=44,
        components={
            "canonical_foundation": "315,648 Hourly Records (2022-2024, 12 Localities)",
            "daily_integrated": "13,152 Integrated Daily Records in Parquet",
            "mapreduce_engine": "4 Streaming Jobs Operational",
            "spark_sql_engine": "6 Analytical Datasets Generated",
            "machine_learning": "RF Classifier (85.1% CV Acc), K-Means (K=3, Sil=0.54), Isolation Forest",
            "geography_engine": "12 Canonical Gurugram Localities with Reference Coordinates"
        }
    )

@router.get("/metadata/summary", response_model=APIResponse)
def get_metadata():
    return APIResponse(
        status="success",
        total_records=315648,
        data={
            "project_name": "UrbanSphere",
            "scope": "Urban Big Data Analytics Platform for Gurugram",
            "canonical_sources": [
                "dataset_weather_gurugram_with_aqi.csv (315,648 rows, 15 columns)",
                "dataset_traffic_gurugram.csv (315,648 rows, 18 columns)",
                "dataset_air_quality_gurugram.csv (315,648 rows, 14 columns)",
                "dataset_geography_gurugram.csv (12 localities, 11 columns)"
            ],
            "total_localities": 12,
            "temporal_range": "2022-01-01 00:00:00 to 2024-12-31 23:00:00",
            "total_test_suites": 5,
            "total_tests_passed": 44,
            "scientific_standards": {
                "air_quality_thresholds": "National Ambient Air Quality Standards (NAAQS India)",
                "traffic_units": "Passenger Car Units (PCU) per Indian Road Congress (IRC) standards",
                "ml_evaluation": "Stratified 5-Fold, TimeSeriesSplit, and 2024 Chronological Holdout"
            }
        }
    )
