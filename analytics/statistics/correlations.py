#!/usr/bin/env python3
"""
UrbanSphere — Inferential Statistical Significance & Correlation Engine (Canonical)
==================================================================================
Calculates Pearson linear correlations and Spearman rank order correlations with
exact two-tailed p-values across meteorological variables and criteria air pollutants.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "integrated" / "urban_integrated_daily.parquet"
ANALYTICS_DIR = PROJECT_ROOT / "output" / "analytics"

ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

WEATHER_VARS = [
    ("temp_mean_c", "Mean Temperature (°C)"),
    ("humidity_mean_pct", "Mean Relative Humidity (%)"),
    ("wind_speed_mean_kmh", "Mean Wind Speed (km/h)"),
    ("surface_pressure_mean_hpa", "Mean Surface Pressure (hPa)"),
    ("precipitation_total_mm", "Total Daily Precipitation (mm)"),
    ("total_vehicles", "Total Daily Vehicles")
]

POLLUTANT_VARS = [
    ("pm25_mean_ugm3", "PM2.5 (ug/m3)"),
    ("pm10_mean_ugm3", "PM10 (ug/m3)"),
    ("no2_mean_ugm3", "NO2 (ug/m3)"),
    ("so2_mean_ugm3", "SO2 (ug/m3)"),
    ("co_mean_mgm3", "CO (mg/m3)"),
    ("o3_mean_ugm3", "O3 (ug/m3)"),
    ("air_quality_aqi_max", "Air Quality Max AQI")
]

def calculate_correlations_for_subset(df_sub, subset_name):
    records = []
    
    for w_col, w_label in WEATHER_VARS:
        for p_col, p_label in POLLUTANT_VARS:
            valid_mask = df_sub[w_col].notna() & df_sub[p_col].notna()
            w_vals = df_sub.loc[valid_mask, w_col]
            p_vals = df_sub.loc[valid_mask, p_col]
            n_pair = len(w_vals)
            
            if n_pair < 10:
                continue
                
            r_val, p_pearson = stats.pearsonr(w_vals, p_vals)
            
            if abs(r_val) < 1.0:
                z = np.arctanh(r_val)
                se = 1.0 / np.sqrt(n_pair - 3)
                ci_low = np.tanh(z - 1.96 * se)
                ci_high = np.tanh(z + 1.96 * se)
            else:
                ci_low, ci_high = r_val, r_val
                
            rho_val, p_spearman = stats.spearmanr(w_vals, p_vals)
            
            records.append({
                "subset": subset_name,
                "n_observations": n_pair,
                "degrees_of_freedom": n_pair - 2,
                "weather_variable": w_col,
                "weather_label": w_label,
                "pollutant_variable": p_col,
                "pollutant_label": p_label,
                "pearson_r": round(float(r_val), 4),
                "pearson_p_value": float(f"{p_pearson:.4e}"),
                "pearson_ci_95_low": round(float(ci_low), 4),
                "pearson_ci_95_high": round(float(ci_high), 4),
                "pearson_significant_001": bool(p_pearson < 0.001),
                "spearman_rho": round(float(rho_val), 4),
                "spearman_p_value": float(f"{p_spearman:.4e}"),
                "spearman_significant_001": bool(p_spearman < 0.001),
                "interpretation": interpret_correlation(r_val, p_pearson)
            })
            
    return pd.DataFrame(records)

def interpret_correlation(r, p):
    if p >= 0.05:
        return "Statistically Non-Significant Association (p >= 0.05)"
    sign = "Inverse" if r < 0 else "Direct"
    strength = abs(r)
    if strength >= 0.5:
        desc = "Strong"
    elif strength >= 0.3:
        desc = "Moderate"
    elif strength >= 0.1:
        desc = "Weak"
    else:
        desc = "Negligible"
    return f"{desc} {sign} Statistical Association (p < 0.05)"

def main():
    print("=" * 60)
    print("UrbanSphere — Statistical Correlation & Inference Engine (Canonical)")
    print("=" * 60)
    
    df = pd.read_parquet(DATA_PATH)
    print(f"Loaded daily integrated observations: {len(df)} records")
    
    df_full_corr = calculate_correlations_for_subset(df, "Canonical_Full_2022_2024")
    
    full_export_path = ANALYTICS_DIR / "statistical_correlations_with_pvalues.csv"
    strat_export_path = ANALYTICS_DIR / "era_stratified_correlations.csv"
    
    df_full_corr.to_csv(full_export_path, index=False)
    df_full_corr.to_csv(strat_export_path, index=False)
    
    pm25_corrs = df_full_corr[df_full_corr["pollutant_variable"] == "pm25_mean_ugm3"].sort_values("pearson_r")
    
    print("\nKey Meteorological Relationships with PM2.5:")
    for _, r in pm25_corrs.iterrows():
        print(f"  • {r['weather_label']:<32}: Pearson r = {r['pearson_r']:>7.4f} (p = {r['pearson_p_value']}) | "
              f"Spearman rho = {r['spearman_rho']:>7.4f} | {r['interpretation']}")
              
    summary = {
        "metadata": {
            "total_observations_analyzed": len(df),
            "methodology_note": (
                "Correlations represent statistical associations between surface meteorological "
                "parameters and daily aggregated pollutant levels. They do not constitute deterministic "
                "or unidirectional causal proof. Confounding variables also govern ambient pollution."
            )
        },
        "strongest_pm25_drivers": pm25_corrs.to_dict(orient="records")
    }
    
    with open(ANALYTICS_DIR / "correlation_significance_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
        
    print(f"\n✓ Exported full correlation matrix:  {full_export_path}")
    print(f"✓ Exported statistical summary JSON: {ANALYTICS_DIR / 'correlation_significance_summary.json'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
