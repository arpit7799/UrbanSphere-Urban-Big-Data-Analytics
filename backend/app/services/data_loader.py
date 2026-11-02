"""
UrbanSphere Backend — Analytical Data Loader Service (Canonical)
===============================================================
Provides fast cached access to all precomputed Spark, MapReduce, and ML datasets.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
PROCESSED_DIR = DATA_DIR / "processed" / "integrated"

class DataLoader:
    _instance = None
    
    def __init__(self):
        self._cache = {}
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _read_csv(self, path: Path) -> List[Dict[str, Any]]:
        key = str(path)
        if key not in self._cache:
            if not path.exists():
                return []
            df = pd.read_csv(path)
            df = df.replace({np.nan: None})
            self._cache[key] = df.to_dict(orient="records")
        return self._cache[key]

    def _read_json(self, path: Path) -> Dict[str, Any]:
        key = str(path)
        if key not in self._cache:
            if not path.exists():
                return {}
            with open(path, "r") as f:
                self._cache[key] = json.load(f)
        return self._cache[key]

    # 1. Traffic & Mobility
    def get_corridor_capacity(self) -> List[Dict[str, Any]]:
        return self._read_csv(OUTPUT_DIR / "spark" / "corridor_capacity_stress.csv")

    def get_vehicle_modal_split(self) -> List[Dict[str, Any]]:
        return self._read_csv(OUTPUT_DIR / "spark" / "vehicle_modal_split.csv")

    def get_traffic_locations(self) -> List[Dict[str, Any]]:
        return self._read_csv(DATA_DIR / "dataset_geography_gurugram.csv")

    # 2. Climate & Weather
    def get_monthly_climate(self) -> List[Dict[str, Any]]:
        return self._read_csv(OUTPUT_DIR / "spark" / "monthly_climate_extremes.csv")

    def get_wind_dispersion(self) -> List[Dict[str, Any]]:
        return self._read_csv(OUTPUT_DIR / "spark" / "wind_pollution_dispersion.csv")

    # 3. Air Quality
    def get_seasonal_air_quality(self, locality: Optional[str] = None) -> List[Dict[str, Any]]:
        records = self._read_csv(OUTPUT_DIR / "spark" / "seasonal_air_quality_profiles.csv")
        if locality:
            records = [r for r in records if r.get("station_name") == locality]
        return records

    def get_daily_timeline(self, locality: Optional[str] = None, year: Optional[int] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        parquet_path = PROCESSED_DIR / "urban_integrated_daily.parquet"
        if not parquet_path.exists():
            return {"total": 0, "records": []}
            
        key = "daily_timeline_df"
        if key not in self._cache:
            df = pd.read_parquet(parquet_path)
            df = df.replace({np.nan: None})
            self._cache[key] = df
        else:
            df = self._cache[key]
            
        df_filtered = df
        if locality:
            df_filtered = df_filtered[df_filtered["location_name"] == locality]
        if year is not None:
            df_filtered = df_filtered[pd.to_datetime(df_filtered["date"]).dt.year == year]
            
        total = len(df_filtered)
        slice_records = df_filtered.iloc[offset : offset + limit].to_dict(orient="records")
        return {"total": total, "records": slice_records}

    # 4. Machine Learning & Statistical Analytics
    def get_cluster_profiles(self) -> Dict[str, Any]:
        profiles = self._read_csv(OUTPUT_DIR / "analytics" / "pollution_cluster_profiles.csv")
        metrics = self._read_json(OUTPUT_DIR / "models" / "clustering_metrics.json")
        return {"profiles": profiles, "metrics": metrics}

    def get_cluster_assignments_sample(self, limit: int = 100) -> List[Dict[str, Any]]:
        records = self._read_csv(OUTPUT_DIR / "analytics" / "pollution_cluster_assignments.csv")
        return records[:limit]

    def get_anomalies(self, phenotype: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        records = self._read_csv(OUTPUT_DIR / "analytics" / "pollution_anomalies.csv")
        metrics = self._read_json(OUTPUT_DIR / "models" / "anomaly_detection_metrics.json")
        
        flagged = [r for r in records if r.get("is_anomaly_isolation_forest") or r.get("is_pm_zscore_outlier")]
        if phenotype:
            flagged = [r for r in flagged if r.get("anomaly_phenotype") == phenotype]
            
        return {
            "total_flagged": len(flagged),
            "metrics": metrics,
            "records": flagged[:limit]
        }

    def get_correlations(self, subset: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._read_csv(OUTPUT_DIR / "analytics" / "statistical_correlations_with_pvalues.csv")

    def get_feature_importances(self) -> List[Dict[str, Any]]:
        return self._read_csv(OUTPUT_DIR / "analytics" / "weather_feature_importances.csv")

    # 5. Geography
    def get_geography_sectors(self) -> List[Dict[str, Any]]:
        return self._read_csv(DATA_DIR / "dataset_geography_gurugram.csv")

    def get_transit_corridors_summary(self) -> List[Dict[str, Any]]:
        return self._read_csv(OUTPUT_DIR / "spark" / "transit_corridor_sectors.csv")

data_loader = DataLoader.get_instance()
