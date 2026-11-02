"""
UrbanSphere Backend — Machine Learning Inference Service (Canonical)
===================================================================
Executes live inference on trained models (Random Forest Classifier & K-Means Clustering).
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import numpy as np
import joblib

from backend.app.schemas.predict import (
    AQIPredictionRequest,
    AQIPredictionResponse,
    WeatherFeatureDriver,
    PollutionRegimeRequest,
    PollutionRegimeResponse
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "output" / "models"
ANALYTICS_DIR = PROJECT_ROOT / "output" / "analytics"

class MLInferenceService:
    _instance = None
    
    def __init__(self):
        self._rf_model = None
        self._scaler = None
        self._kmeans = None
        self._kmeans_scaler = None
        self._feature_importances = []
        self._metrics = {}
        self._cluster_metrics = {}
        self._load_artifacts()
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_artifacts(self):
        rf_path = MODEL_DIR / "aqi_classifier_rf.joblib"
        km_path = MODEL_DIR / "pollution_kmeans.joblib"
        km_scaler_path = MODEL_DIR / "pollution_scaler.joblib"
        metrics_path = MODEL_DIR / "classification_metrics.json"
        km_metrics_path = MODEL_DIR / "clustering_metrics.json"
        fi_path = ANALYTICS_DIR / "weather_feature_importances.csv"

        if rf_path.exists():
            self._rf_model = joblib.load(rf_path)
        if km_path.exists():
            self._kmeans = joblib.load(km_path)
        if km_scaler_path.exists():
            self._kmeans_scaler = joblib.load(km_scaler_path)
        if metrics_path.exists():
            with open(metrics_path, "r") as f:
                self._metrics = json.load(f)
        if km_metrics_path.exists():
            with open(km_metrics_path, "r") as f:
                self._cluster_metrics = json.load(f)
        if fi_path.exists():
            self._feature_importances = pd.read_csv(fi_path).to_dict(orient="records")

    def predict_aqi(self, req: AQIPredictionRequest) -> AQIPredictionResponse:
        if self._rf_model is None:
            raise RuntimeError("Random Forest AQI model is not loaded.")
            
        diurnal_range = (
            req.temp_diurnal_range_c 
            if req.temp_diurnal_range_c is not None 
            else round(req.temp_max_c - req.temp_min_c, 2)
        )
        
        # Exact feature ordering required by the trained model
        input_data = pd.DataFrame([{
            "temp_min_c": req.temp_min_c,
            "temp_max_c": req.temp_max_c,
            "temp_mean_c": req.temp_mean_c,
            "temp_diurnal_range_c": diurnal_range,
            "humidity_mean_pct": req.humidity_mean_pct,
            "precipitation_total_mm": req.precipitation_total_mm,
            "surface_pressure_mean_hpa": req.surface_pressure_mean_hpa,
            "wind_speed_mean_kmh": req.wind_speed_mean_kmh,
            "wind_speed_max_kmh": req.wind_speed_max_kmh,
            "month": req.month
        }])
        
        predicted_category = self._rf_model.predict(input_data)[0]
        probs_raw = self._rf_model.predict_proba(input_data)[0]
        classes = self._rf_model.classes_
        
        class_probs = {c: round(float(p), 4) for c, p in zip(classes, probs_raw)}
        confidence = class_probs.get(predicted_category, 0.0)
        
        # Map feature values with importance weights
        drivers = []
        for item in self._feature_importances[:5]:
            feat_name = item["feature"]
            val = float(input_data[feat_name].iloc[0])
            drivers.append(WeatherFeatureDriver(
                feature=feat_name,
                importance=round(float(item["importance"]), 4),
                value=round(val, 2)
            ))
            
        return AQIPredictionResponse(
            predicted_aqi_category=predicted_category,
            confidence=confidence,
            class_probabilities=class_probs,
            top_weather_drivers=drivers,
            model_version="RandomForestClassifier(n_estimators=100, max_depth=8)",
            cross_validation_accuracy=self._metrics.get("stratified_5fold_accuracy", 0.8507),
            scientific_disclaimer=(
                "Scientific Caution: Meteorological variables account for ~55-75% of variation. "
                "The remaining variance is governed by unmodeled anthropogenic emissions, biomass burning, "
                "and boundary layer dynamics. This output represents an exploratory statistical association."
            )
        )

    def predict_pollution_regime(self, req: PollutionRegimeRequest) -> PollutionRegimeResponse:
        if self._kmeans is None or self._kmeans_scaler is None:
            raise RuntimeError("K-Means clustering model or scaler is not loaded.")
            
        feature_vector = pd.DataFrame([{
            "pm25_mean_ugm3": req.pm25,
            "pm10_mean_ugm3": req.pm10,
            "no2_mean_ugm3": req.no2,
            "so2_mean_ugm3": req.so2,
            "co_mean_mgm3": req.co,
            "o3_mean_ugm3": req.o3
        }])
        
        scaled = self._kmeans_scaler.transform(feature_vector)
        cluster_id = int(self._kmeans.predict(scaled)[0])
        
        descriptions = {
            0: (
                "Low Pollution Monsoon / High Dispersion Regime: "
                "Characterized by lowest PM2.5 (~70 ug/m3), elevated summer/monsoon temperatures, "
                "and vigorous atmospheric convective dispersion."
            ),
            1: (
                "Severe Winter Inversion / Smog Stagnation Regime: "
                "Extreme particulate trapping with PM2.5 nearing 200 ug/m3, severe AQI (>350), "
                "shallow boundary layer, and calm anticyclonic winter conditions."
            ),
            2: (
                "Moderate Photochemical / Transition Regime: "
                "Intermediate particulate levels with active secondary photochemistry (elevated O3/NO2) "
                "and moderate temperatures."
            )
        }
        
        regime_names = {
            0: "Low_Pollution_Monsoon_Regime",
            1: "Severe_Inversion_Winter_Smog_Regime",
            2: "Moderate_Photochemical_Regime"
        }
        
        return PollutionRegimeResponse(
            cluster_id=cluster_id,
            regime_name=regime_names.get(cluster_id, f"Cluster_{cluster_id}"),
            silhouette_score=self._cluster_metrics.get("silhouette_score", 0.5443),
            cluster_description=descriptions.get(cluster_id, "Standard Urban Pollution Regime")
        )

ml_service = MLInferenceService.get_instance()
