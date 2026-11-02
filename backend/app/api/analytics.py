from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.common import APIResponse
from backend.app.services.data_loader import data_loader

router = APIRouter(prefix="/analytics", tags=["Advanced Machine Learning & Statistics"])

@router.get("/clusters", response_model=APIResponse)
def get_pollution_clusters():
    """Returns K-Means multi-pollutant atmospheric regime profiles and silhouette evaluation."""
    data = data_loader.get_cluster_profiles()
    sample_assignments = data_loader.get_cluster_assignments_sample(limit=30)
    return APIResponse(
        status="success",
        total_records=len(data.get("profiles", [])),
        data={
            "regime_profiles": data.get("profiles", []),
            "clustering_metrics": data.get("metrics", {}),
            "sample_assignments": sample_assignments
        },
        metadata={
            "algorithm": "KMeans(n_clusters=3, random_state=42)",
            "features_used": ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"],
            "variance_explained_pca": "82.9% (PC1: 60.8%, PC2: 22.1%)",
            "interpretation": "3 distinct seasonal regimes: Monsoon Washout, Photochemical, and Winter Thermal Inversion"
        }
    )

@router.get("/anomalies", response_model=APIResponse)
def get_pollution_anomalies(
    phenotype: Optional[str] = Query(None, description="Filter by phenotype (e.g., Post_Monsoon_Biomass_Firework_Smog_Shock)"),
    limit: int = Query(50, ge=1, le=100)
):
    """Returns extreme atmospheric outlier days flagged by Isolation Forest (5%) and PM Z-Scores (>2.5)."""
    data = data_loader.get_anomalies(phenotype=phenotype, limit=limit)
    return APIResponse(
        status="success",
        total_records=data["total_flagged"],
        data={
            "flagged_episodes": data["records"],
            "metrics": data["metrics"]
        },
        metadata={
            "total_anomalies_flagged": data["total_flagged"],
            "phenotype_filter": phenotype,
            "detection_method": "Multivariate Isolation Forest (contamination=0.05) combined with PM Z-score (>2.5)"
        }
    )

@router.get("/correlations", response_model=APIResponse)
def get_statistical_correlations(
    subset: Optional[str] = Query(
        None, 
        description="Filter by data era: 'Full_Integrated_2022_2024', 'Reanalysis_CAMS_2022_2023', or 'Ground_Station_CPCB_2024'"
    )
):
    """Returns Pearson linear & Spearman rank correlations with exact two-tailed p-values and 95% CIs."""
    data = data_loader.get_correlations(subset=subset)
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "era_filter": subset or "Full_Integrated_2022_2024",
            "confidence_intervals": "95% via Fisher z-transformation",
            "scientific_note": "Correlations demonstrate statistical association, not unidirectional causation."
        }
    )

@router.get("/feature-importances", response_model=APIResponse)
def get_weather_feature_importances():
    """Returns Random Forest meteorological feature importances ranking atmospheric drivers."""
    data = data_loader.get_feature_importances()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "model": "Random Forest Classifier (100 estimators, max depth 6)",
            "primary_drivers": ["Mean Temperature", "Mean Sea-Level Pressure", "Mean Relative Humidity"]
        }
    )
