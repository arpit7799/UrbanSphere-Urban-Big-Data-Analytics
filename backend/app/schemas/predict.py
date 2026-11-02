from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class AQIPredictionRequest(BaseModel):
    temp_min_c: float = Field(..., description="Minimum daily temperature in Celsius", example=11.2)
    temp_max_c: float = Field(..., description="Maximum daily temperature in Celsius", example=22.4)
    temp_mean_c: float = Field(..., description="Mean daily temperature in Celsius", example=16.8)
    temp_diurnal_range_c: Optional[float] = Field(None, description="Diurnal temperature range (auto-calculated if omitted)", example=11.2)
    humidity_mean_pct: float = Field(..., description="Mean relative humidity percentage (0-100)", example=72.0)
    precipitation_total_mm: float = Field(0.0, description="Total daily precipitation in mm", example=0.0)
    surface_pressure_mean_hpa: float = Field(1008.0, description="Mean surface pressure in hPa", example=1008.5)
    wind_speed_mean_kmh: float = Field(10.0, description="Mean wind speed in km/h", example=9.5)
    wind_speed_max_kmh: float = Field(18.0, description="Maximum wind gust speed in km/h", example=16.0)
    month: int = Field(..., ge=1, le=12, description="Month of the year (1-12)", example=12)

class WeatherFeatureDriver(BaseModel):
    feature: str
    importance: float
    value: float

class AQIPredictionResponse(BaseModel):
    predicted_aqi_category: str
    confidence: float
    class_probabilities: Dict[str, float]
    top_weather_drivers: List[WeatherFeatureDriver]
    model_version: str
    cross_validation_accuracy: float
    scientific_disclaimer: str

class PollutionRegimeRequest(BaseModel):
    pm25: float = Field(..., description="PM2.5 concentration in ug/m3", example=145.0)
    pm10: float = Field(..., description="PM10 concentration in ug/m3", example=260.0)
    no2: float = Field(..., description="NO2 concentration in ug/m3", example=65.0)
    so2: float = Field(..., description="SO2 concentration in ug/m3", example=14.0)
    co: float = Field(..., description="CO concentration in mg/m3", example=1.1)
    o3: float = Field(..., description="O3 concentration in ug/m3", example=32.0)

class PollutionRegimeResponse(BaseModel):
    cluster_id: int
    regime_name: str
    silhouette_score: float
    cluster_description: str
