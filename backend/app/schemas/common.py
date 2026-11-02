from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class APIResponse(BaseModel):
    status: str = "success"
    total_records: int
    data: Any
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    platform: str
    city: str
    total_tests_passed: int
    components: Dict[str, str]
