from fastapi import APIRouter
from backend.app.schemas.common import APIResponse
from backend.app.services.data_loader import data_loader

router = APIRouter(prefix="/geography", tags=["Geography & Spatial Layout"])

@router.get("/sectors", response_model=APIResponse)
def get_geography_sectors():
    """Returns Gurugram study localities with reference coordinates, urban function, and corridors."""
    data = data_loader.get_geography_sectors()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "12 canonical Gurugram localities with typology and representative corridors",
            "source": "dataset_geography_gurugram.csv"
        }
    )

@router.get("/corridors", response_model=APIResponse)
def get_transit_corridors():
    """Returns derived transit corridor bounding boxes and locality distributions."""
    data = data_loader.get_transit_corridors_summary()
    return APIResponse(
        status="success",
        total_records=len(data),
        data=data,
        metadata={
            "description": "Transit corridor spatial bounds across Gurugram study network",
            "source": "transit_corridor_sectors.csv"
        }
    )
