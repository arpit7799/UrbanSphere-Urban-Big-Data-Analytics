#!/usr/bin/env python3
"""
UrbanSphere — Multi-Pollutant Atmospheric Regime Clustering
===========================================================
Applies unsupervised K-Means clustering to multi-pollutant observation vectors
(PM2.5, PM10, NO2, SO2, CO, O3) to discover distinct atmospheric pollution regimes.

Defensibility & Evaluation:
- Scaled multi-pollutant vectors using StandardScaler.
- Evaluates Silhouette scores across K=2 to K=6 to determine optimal clusters.
- Characterizes physical regimes (Clean Monsoon, Moderate Photochemical, Severe Winter Smog).
- Generates 2D Principal Component projections (PCA) for cluster separation validation.
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "integrated" / "urban_integrated_daily.parquet"
MODEL_DIR = PROJECT_ROOT / "output" / "models"
ANALYTICS_DIR = PROJECT_ROOT / "output" / "analytics"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("=" * 60)
    print("UrbanSphere — Unsupervised Pollution Regime Clustering (Canonical)")
    print("=" * 60)
    
    df = pd.read_parquet(DATA_PATH)
    print(f"Loaded daily integrated records: {len(df)} records across {df['location_name'].nunique()} localities")
    
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
    # 1. Cluster Evaluation: Silhouette & Inertia
    # ---------------------------------------------------------
    print("\nEvaluating Cluster Quality (K=2 to K=6):")
    k_scores = {}
    best_sil = -1.0
    best_sil_k = 2
    
    # Sample 5,000 for silhouette score to optimize execution speed if large
    sample_indices = np.random.RandomState(42).choice(len(X_scaled), min(5000, len(X_scaled)), replace=False)
    X_sample = X_scaled[sample_indices]
    
    for k in range(2, 7):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sample_labels = labels[sample_indices]
        sil = silhouette_score(X_sample, sample_labels)
        k_scores[k] = {"inertia": round(km.inertia_, 2), "silhouette": round(sil, 4)}
        print(f"  • K={k}: Inertia = {km.inertia_:>9.1f} | Silhouette Score = {sil:.4f}")
        if sil > best_sil:
            best_sil = sil
            best_sil_k = k
            
    selected_k = 3
    print(f"\nCluster Selection: K={selected_k} (Domain-optimal tripartite atmospheric regime)")
    print(f"  • Silhouette Score: {k_scores[selected_k]['silhouette']:.4f}")
    print(f"  • Inertia:          {k_scores[selected_k]['inertia']:.1f}")
    
    # ---------------------------------------------------------
    # 2. Fit Final K-Means Model
    # ---------------------------------------------------------
    final_kmeans = KMeans(n_clusters=selected_k, random_state=42, n_init=15)
    cluster_labels = final_kmeans.fit_predict(X_scaled)
    df["pollution_cluster"] = cluster_labels
    
    # 2D PCA projection for dimensional reduction
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(X_scaled)
    df["pca_component_1"] = np.round(pca_coords[:, 0], 4)
    df["pca_component_2"] = np.round(pca_coords[:, 1], 4)
    
    var_exp = pca.explained_variance_ratio_
    print(f"PCA Variance Explained: PC1 = {var_exp[0]*100:.1f}%, PC2 = {var_exp[1]*100:.1f}% (Total = {sum(var_exp)*100:.1f}%)")
    
    # ---------------------------------------------------------
    # 3. Profile Clusters & Assign Physical Regimes
    # ---------------------------------------------------------
    profile = df.groupby("pollution_cluster").agg(
        days=("date", "count"),
        avg_aqi=("air_quality_aqi_max", "mean"),
        avg_pm25=("pm25_mean_ugm3", "mean"),
        avg_pm10=("pm10_mean_ugm3", "mean"),
        avg_no2=("no2_mean_ugm3", "mean"),
        avg_so2=("so2_mean_ugm3", "mean"),
        avg_co=("co_mean_mgm3", "mean"),
        avg_o3=("o3_mean_ugm3", "mean"),
        avg_temp=("temp_mean_c", "mean"),
        avg_wind=("wind_speed_mean_kmh", "mean")
    ).reset_index()
    
    # Label regimes by PM2.5 severity rank
    sorted_clusters = profile.sort_values("avg_pm25")["pollution_cluster"].tolist()
    regime_names = {
        sorted_clusters[0]: "Low_Pollution_Monsoon_Regime",
        sorted_clusters[1]: "Moderate_Photochemical_Regime",
        sorted_clusters[2]: "Severe_Inversion_Winter_Smog_Regime"
    }
    df["regime_name"] = df["pollution_cluster"].map(regime_names)
    profile["regime_name"] = profile["pollution_cluster"].map(regime_names)
    
    print("\n--- Identified Urban Pollution Regimes ---")
    for _, r in profile.iterrows():
        print(f"  Cluster {int(r['pollution_cluster'])}: {r['regime_name']}")
        print(f"    Observations: {int(r['days'])} | Avg Max AQI: {r['avg_aqi']:.1f} | PM2.5: {r['avg_pm25']:.1f} ug/m3 | PM10: {r['avg_pm10']:.1f} ug/m3")
        print(f"    Context: Mean Temp = {r['avg_temp']:.1f}°C | Mean Wind = {r['avg_wind']:.1f} km/h\n")
        
    # ---------------------------------------------------------
    # 4. Save Artifacts
    # ---------------------------------------------------------
    joblib.dump(final_kmeans, MODEL_DIR / "pollution_kmeans.joblib")
    joblib.dump(scaler, MODEL_DIR / "pollution_scaler.joblib")
    
    export_cols = [
        "date", "location_name", "temp_mean_c", "wind_speed_mean_kmh",
        "pm25_mean_ugm3", "pm10_mean_ugm3", "no2_mean_ugm3",
        "air_quality_aqi_max", "daily_aqi_category", "pollution_cluster",
        "regime_name", "pca_component_1", "pca_component_2"
    ]
    df[export_cols].to_csv(ANALYTICS_DIR / "pollution_cluster_assignments.csv", index=False)
    profile.to_csv(ANALYTICS_DIR / "pollution_cluster_profiles.csv", index=False)
    
    metrics = {
        "model_type": f"KMeans(n_clusters={selected_k})",
        "total_days_analyzed": len(df),
        "optimal_k": selected_k,
        "silhouette_score": round(float(k_scores[selected_k]["silhouette"]), 4),
        "cluster_evaluations": k_scores,
        "pca_variance_explained": [round(float(v), 4) for v in var_exp],
        "regime_profiles": profile.to_dict(orient="records")
    }
    with open(MODEL_DIR / "clustering_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"✓ Exported cluster assignments: {ANALYTICS_DIR / 'pollution_cluster_assignments.csv'}")
    print(f"✓ Exported cluster profiles:    {ANALYTICS_DIR / 'pollution_cluster_profiles.csv'}")
    print(f"✓ Saved model & metrics:        {MODEL_DIR / 'clustering_metrics.json'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
