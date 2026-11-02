from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.common import APIResponse
from backend.app.services.data_loader import data_loader

router = APIRouter(prefix="/air-quality", tags=["Air Quality & Pollution"])

@router.get("/seasonal", response_model=APIResponse)
def get_seasonal_air_quality(
    locality: Optional[str] = Query(None, description="Filter by locality (e.g., 'Cyber City', 'Badshahpur')")
):
    """Returns seasonal air quality profiles and NAAQS reference threshold exceedances."""
    data = data_loader.get_seasonal_air_quality(locality=locality)
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "Seasonal criteria pollutant concentrations and NAAQS 24-hr threshold comparison",
            "locality_filter": locality,
            "thresholds": "PM2.5: 60 ug/m3, PM10: 100 ug/m3, NO2: 80 ug/m3 (NAAQS Schedule VII)"
        }
    )

@router.get("/daily-timeline", response_model=APIResponse)
def get_daily_timeline(
    locality: Optional[str] = Query(None, description="Filter by locality name"),
    year: Optional[int] = Query(None, description="Filter by year (2022, 2023, 2024)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of daily records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """Returns the daily integrated meteorological and air quality timeline (13,152 locality-days)."""
    res = data_loader.get_daily_timeline(locality=locality, year=year, limit=limit, offset=offset)
    return APIResponse(
        status="success",
        total_records=res["total"],
        data=res["records"],
        metadata={
            "locality_filter": locality,
            "year_filter": year,
            "limit": limit,
            "offset": offset,
            "total_available": res["total"],
            "temporal_coverage": "2022-01-01 to 2024-12-31"
        }
    )
