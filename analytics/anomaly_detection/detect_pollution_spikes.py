#!/usr/bin/env python3
"""
UrbanSphere — Multi-Pollutant Atmospheric Anomaly Detection (Canonical)
=======================================================================
Detects extreme pollution episodes, seasonal smog shocks, and dust storm
outliers across Gurugram using unsupervised Isolation Forest and univariate Z-score filtering.
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "integrated" / "urban_integrated_daily.parquet"
MODEL_DIR = PROJECT_ROOT / "output" / "models"
ANALYTICS_DIR = PROJECT_ROOT / "output" / "analytics"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

def categorize_anomaly(row):
    if not row["is_anomaly_isolation_forest"] and not row["is_pm_zscore_outlier"]:
        return "Normal_Atmospheric_Range"
        
    date_str = str(row["date"])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    pm25 = row["pm25_mean_ugm3"]
    pm10 = row["pm10_mean_ugm3"]
    temp = row["temp_mean_c"]
    ratio = pm25 / pm10 if pm10 > 0 else 0.5

    # 1. Post-monsoon agricultural burning & Diwali window (mid-October to late November)
    if (month == 10 and day >= 15) or month == 11:
        if pm25 > 150:
            return "Post_Monsoon_Biomass_Firework_Smog_Shock"
            
    # 2. Winter thermal inversion (December to January)
    if month in (12, 1) and temp < 18.0 and pm25 > 180:
        return "Severe_Winter_Inversion_Stagnation"
        
    # 3. Pre-monsoon coarse mineral dust storms (March to June, PM10 dominant)
    if month in (3, 4, 5, 6) and pm10 > 300 and ratio < 0.45:
        return "Pre_Monsoon_Coarse_Dust_Storm_Event"
        
    # 4. Fallback acute spike
    return "Multi_Pollutant_Acute_Spike"

def main():
    print("=" * 60)
    print("UrbanSphere — Atmospheric Anomaly Detection Engine (Canonical)")
    print("=" * 60)
    
    df = pd.read_parquet(DATA_PATH)
    print(f"Loaded daily integrated observations: {len(df)} records")
    
    pollutant_cols = [
        "pm25_mean_ugm3",
        "pm10_mean_ugm3",
        "no2_mean_ugm3",
        "so2_mean_ugm3",
        "co_mean_mgm3",
        "o3_mean_ugm3"
    ]
    
    X = df[pollutant_cols].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # ---------------------------------------------------------
    # 1. Fit Isolation Forest
    # ---------------------------------------------------------
    iso_forest = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    )
    iso_preds = iso_forest.fit_predict(X_scaled)
    anomaly_scores = iso_forest.decision_function(X_scaled)
    
    df["is_anomaly_isolation_forest"] = iso_preds == -1
    df["isolation_anomaly_score"] = np.round(anomaly_scores, 4)
    
    # ---------------------------------------------------------
    # 2. Calculate Statistical Z-Scores
    # ---------------------------------------------------------
    pm25_mean = df["pm25_mean_ugm3"].mean()
    pm25_std = df["pm25_mean_ugm3"].std()
    pm10_mean = df["pm10_mean_ugm3"].mean()
    pm10_std = df["pm10_mean_ugm3"].std()
    
    df["pm25_zscore"] = np.round((df["pm25_mean_ugm3"] - pm25_mean) / pm25_std, 2)
    df["pm10_zscore"] = np.round((df["pm10_mean_ugm3"] - pm10_mean) / pm10_std, 2)
    
    df["is_pm_zscore_outlier"] = (df["pm25_zscore"] > 2.5) | (df["pm10_zscore"] > 2.5)
    
    # ---------------------------------------------------------
    # 3. Categorize Anomaly Phenotypes
    # ---------------------------------------------------------
    df["anomaly_phenotype"] = df.apply(categorize_anomaly, axis=1)
    
    anomalies_df = df[df["is_anomaly_isolation_forest"] | df["is_pm_zscore_outlier"]].copy()
    total_anomalies = len(anomalies_df)
    iso_anomalies_count = int(df["is_anomaly_isolation_forest"].sum())
    zscore_anomalies_count = int(df["is_pm_zscore_outlier"].sum())
    
    print(f"\nAnomaly Summary:")
    print(f"  • Isolation Forest Anomalies (5% contamination): {iso_anomalies_count} records")
    print(f"  • Univariate PM Z-Score Outliers (Z > 2.5):      {zscore_anomalies_count} records")
    print(f"  • Total Union of Atmospheric Anomalies:          {total_anomalies} records")
    
    print("\nAnomaly Phenotype Breakdown:")
    phenotype_counts = anomalies_df["anomaly_phenotype"].value_counts()
    for pheno, cnt in phenotype_counts.items():
        print(f"  • {pheno}: {cnt} records")
        
    # ---------------------------------------------------------
    # 4. Save Models & Output Datasets
    # ---------------------------------------------------------
    joblib.dump(iso_forest, MODEL_DIR / "isolation_forest_anomaly.joblib")
    joblib.dump(scaler, MODEL_DIR / "anomaly_scaler.joblib")
    
    export_cols = [
        "date", "location_name", "temp_mean_c", "wind_speed_mean_kmh",
        "pm25_mean_ugm3", "pm10_mean_ugm3", "no2_mean_ugm3",
        "so2_mean_ugm3", "co_mean_mgm3", "o3_mean_ugm3",
        "air_quality_aqi_max", "daily_aqi_category",
        "is_anomaly_isolation_forest", "isolation_anomaly_score",
        "pm25_zscore", "pm10_zscore", "is_pm_zscore_outlier", "anomaly_phenotype"
    ]
    
    df[export_cols].to_csv(ANALYTICS_DIR / "pollution_anomalies.csv", index=False)
    
    top_spikes = anomalies_df.sort_values("pm25_mean_ugm3", ascending=False).head(5)
    metrics = {
        "model_type": "IsolationForest(contamination=0.05, n_estimators=100)",
        "total_days_analyzed": len(df),
        "total_anomalies_flagged": total_anomalies,
        "isolation_forest_count": iso_anomalies_count,
        "zscore_outlier_count": zscore_anomalies_count,
        "phenotype_distribution": phenotype_counts.to_dict(),
        "top_anomalous_episodes": top_spikes[[
            "date", "location_name", "air_quality_aqi_max", "daily_aqi_category",
            "pm25_mean_ugm3", "pm10_mean_ugm3", "temp_mean_c",
            "anomaly_phenotype"
        ]].to_dict(orient="records")
    }
    
    with open(MODEL_DIR / "anomaly_detection_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"\n✓ Exported anomaly dataset: {ANALYTICS_DIR / 'pollution_anomalies.csv'}")
    print(f"✓ Saved model bundle:      {MODEL_DIR / 'isolation_forest_anomaly.joblib'}")
    print(f"✓ Saved metrics JSON:      {MODEL_DIR / 'anomaly_detection_metrics.json'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
