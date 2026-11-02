from fastapi import APIRouter
from backend.app.schemas.common import APIResponse
from backend.app.services.data_loader import data_loader

router = APIRouter(prefix="/weather", tags=["Climate & Meteorology"])

@router.get("/monthly", response_model=APIResponse)
def get_monthly_climate():
    """Returns monthly climatological summaries, precipitation, and extreme hours from Spark SQL."""
    data = data_loader.get_monthly_climate()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "Monthly aggregates across 26,304 hourly meteorological records (2022-2024)",
            "source": "Open-Meteo ERA5 / Reanalysis and Ground Observations",
            "variables": ["temp_mean_c", "temp_max_c", "temp_min_c", "precipitation_total_mm", "heatwave_hours", "frost_risk_hours"]
        }
    )

@router.get("/wind-dispersion", response_model=APIResponse)
def get_wind_dispersion():
    """Returns pollution concentrations grouped by wind-speed regime."""
    data = data_loader.get_wind_dispersion()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "Cross-tabulation of wind speed categories against ambient PM2.5 and PM10",
            "caution": "Exploratory association: planetary boundary layer height also co-governs dispersion"
        }
    )
