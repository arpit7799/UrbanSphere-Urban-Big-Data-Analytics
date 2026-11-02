from fastapi import APIRouter, HTTPException
from backend.app.schemas.predict import (
    AQIPredictionRequest,
    AQIPredictionResponse,
    PollutionRegimeRequest,
    PollutionRegimeResponse
)
from backend.app.services.ml_inference import ml_service

router = APIRouter(prefix="/predict", tags=["Machine Learning Inference"])

@router.post("/aqi", response_model=AQIPredictionResponse)
def predict_aqi_category(request: AQIPredictionRequest):
    """
    Predicts CPCB AQI category from daily meteorological variables using
    the trained Random Forest Classifier.
    """
    try:
        response = ml_service.predict_aqi(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@router.post("/regime", response_model=PollutionRegimeResponse)
def predict_pollution_regime(request: PollutionRegimeRequest):
    """
    Classifies a multi-pollutant vector (PM2.5, PM10, NO2, SO2, CO, O3)
    into one of the 3 unsupervised atmospheric pollution regimes using K-Means.
    """
    try:
        response = ml_service.predict_pollution_regime(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
