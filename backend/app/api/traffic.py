from fastapi import APIRouter
from backend.app.schemas.common import APIResponse
from backend.app.services.data_loader import data_loader

router = APIRouter(prefix="/traffic", tags=["Traffic & Mobility"])

@router.get("/corridors", response_model=APIResponse)
def get_traffic_corridors():
    """Returns corridor capacity stress, peak PCUs, and road class metrics from Spark SQL."""
    data = data_loader.get_corridor_capacity()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "Corridor traffic volumes and peak PCUs aggregated across canonical road types",
            "source": "Canonical Traffic Dataset & PySpark SQL Analysis",
            "road_classes": [r.get("location_type") for r in data]
        }
    )

@router.get("/modal-split", response_model=APIResponse)
def get_vehicle_modal_split():
    """Returns vehicle composition percentages and modal split distributions."""
    data = data_loader.get_vehicle_modal_split()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "Modal split percentages across 6 canonical vehicle categories",
            "vehicle_categories": ["two_wheeler", "car", "auto_rickshaw", "bus", "truck", "other_vehicle"]
        }
    )

@router.get("/locations", response_model=APIResponse)
def get_traffic_locations():
    """Returns the 12 canonical localities with geographical coordinates."""
    data = data_loader.get_traffic_locations()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "12 canonical study localities in Gurugram",
            "total_localities": len(data)
        }
    )
