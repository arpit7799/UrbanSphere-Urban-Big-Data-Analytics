#!/usr/bin/env python3
"""
UrbanSphere MapReduce Output Verification Engine (Canonical Datasets)
=====================================================================
Independently calculates ground-truth aggregations from the canonical CSVs
using Pandas and validates that MapReduce text outputs match with precision.
"""

import os
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output/mapreduce")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def test_verify_job1():
    print("Verifying Job 1: Traffic Corridors (Canonical)...")
    out_file = os.path.join(OUTPUT_DIR, "job1_traffic_corridors_canonical.txt")
    assert os.path.exists(out_file), f"Output file missing: {out_file}"

    mr_rows = {}
    with open(out_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            loc_type = parts[0]
            vals = [float(x) for x in parts[1].split(",")]
            mr_rows[loc_type] = {
                "count": int(vals[0]),
                "total_vehicles": vals[1],
                "total_pcu": vals[2],
            }

    df = pd.read_csv(os.path.join(DATA_DIR, "dataset_traffic_gurugram.csv"), usecols=["road_type", "vehicle_count", "total_pcu"])
    gt = df.groupby("road_type").agg(
        count=("vehicle_count", "count"),
        total_vehicles=("vehicle_count", "sum"),
        total_pcu=("total_pcu", "sum")
    ).to_dict("index")

    assert len(mr_rows) == len(gt), f"Road type count mismatch: {len(mr_rows)} vs {len(gt)}"
    total_mr_count = sum(r["count"] for r in mr_rows.values())
    assert total_mr_count == 315648, f"Total records must be 315648, got {total_mr_count}"

    for r_type, g in gt.items():
        assert r_type in mr_rows, f"Missing road type: {r_type}"
        m = mr_rows[r_type]
        assert m["count"] == g["count"], f"Count mismatch for {r_type}"
        assert abs(m["total_vehicles"] - g["total_vehicles"]) < 1.0, f"Vehicle mismatch for {r_type}"
        assert abs(m["total_pcu"] - g["total_pcu"]) < 1.0, f"PCU mismatch for {r_type}"
    print(f"  ✓ Job 1 Verified: All {len(gt)} road types, volume sums ({sum(g['total_vehicles'] for g in gt.values()):,.0f} veh), and PCUs match ground truth.")

def test_verify_job2():
    print("Verifying Job 2: Vehicle Composition (Canonical)...")
    out_file = os.path.join(OUTPUT_DIR, "job2_vehicle_composition_modal_split.txt")
    assert os.path.exists(out_file), f"Output file missing: {out_file}"

    mr_rows = {}
    with open(out_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            cat = parts[0]
            vals = [float(x) for x in parts[1].split(",")]
            mr_rows[cat] = {
                "count": int(vals[0]),
                "mean_share_pct": vals[1],
                "min_share_pct": vals[2],
                "max_share_pct": vals[3]
            }

    df = pd.read_csv(os.path.join(DATA_DIR, "dataset_traffic_gurugram.csv"), usecols=[
        "vehicle_count", "two_wheeler_count", "car_count", "auto_rickshaw_count",
        "bus_count", "truck_count", "other_vehicle_count"
    ])

    expected_cats = {
        "two_wheeler": (df["two_wheeler_count"] / df["vehicle_count"].replace(0, np.nan) * 100).mean(),
        "car": (df["car_count"] / df["vehicle_count"].replace(0, np.nan) * 100).mean(),
        "auto_rickshaw": (df["auto_rickshaw_count"] / df["vehicle_count"].replace(0, np.nan) * 100).mean(),
        "bus": (df["bus_count"] / df["vehicle_count"].replace(0, np.nan) * 100).mean(),
        "truck": (df["truck_count"] / df["vehicle_count"].replace(0, np.nan) * 100).mean(),
        "other_vehicle": (df["other_vehicle_count"] / df["vehicle_count"].replace(0, np.nan) * 100).mean()
    }

    assert len(mr_rows) == 6, f"Expected 6 vehicle categories, got {len(mr_rows)}"
    for cat, exp_mean in expected_cats.items():
        assert cat in mr_rows, f"Missing category: {cat}"
        m = mr_rows[cat]
        assert m["count"] == 315648
        assert abs(m["mean_share_pct"] - exp_mean) < 0.1, f"Share mismatch for {cat}: MR={m['mean_share_pct']}, GT={exp_mean:.2f}"
    print(f"  ✓ Job 2 Verified: All 6 vehicle categories across 315,648 observations match ground truth.")

def test_verify_job3():
    print("Verifying Job 3: Weather Extremes (Canonical)...")
    out_file = os.path.join(OUTPUT_DIR, "job3_weather_extremes_monthly.txt")
    assert os.path.exists(out_file), f"Output file missing: {out_file}"

    mr_rows = {}
    with open(out_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            ym = parts[0]
            vals = [float(x) for x in parts[1].split(",")]
            mr_rows[ym] = {
                "hours": int(vals[0]),
                "t_min": vals[1],
                "t_max": vals[2],
                "t_mean": vals[3],
                "heatwave_hrs": int(vals[5]),
                "coldwave_hrs": int(vals[6])
            }

    df = pd.read_csv(os.path.join(DATA_DIR, "dataset_weather_gurugram_with_aqi.csv"), usecols=["date", "temperature_c"])
    df["ym"] = df["date"].str[:7]
    gt = df.groupby("ym").agg(
        hours=("temperature_c", "count"),
        t_min=("temperature_c", "min"),
        t_max=("temperature_c", "max"),
        t_mean=("temperature_c", "mean"),
        heatwave_hrs=("temperature_c", lambda s: (s >= 40.0).sum()),
        coldwave_hrs=("temperature_c", lambda s: (s <= 7.0).sum()),
    ).to_dict("index")

    assert len(mr_rows) == 36, f"Expected 36 months, got {len(mr_rows)}"
    total_hours = sum(r["hours"] for r in mr_rows.values())
    assert total_hours == 315648, f"Expected 315648 total hours, got {total_hours}"

    for ym, g in gt.items():
        assert ym in mr_rows, f"Missing month: {ym}"
        m = mr_rows[ym]
        assert m["hours"] == g["hours"]
        assert abs(m["t_min"] - round(g["t_min"], 1)) < 0.2
        assert abs(m["t_max"] - round(g["t_max"], 1)) < 0.2
        assert abs(m["t_mean"] - round(g["t_mean"], 2)) < 0.05
        assert m["heatwave_hrs"] == g["heatwave_hrs"]
        assert m["coldwave_hrs"] == g["coldwave_hrs"]
    print("  ✓ Job 3 Verified: 36 monthly sequences and 315,648 hours match ground truth.")

def test_verify_job4():
    print("Verifying Job 4: Air Quality Profiling (Canonical)...")
    out_file = os.path.join(OUTPUT_DIR, "job4_air_quality_profiling_seasonal.txt")
    assert os.path.exists(out_file), f"Output file missing: {out_file}"

    mr_rows = {}
    with open(out_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            prov, stn, season = parts[0], parts[1], parts[2]
            vals = [float(x) for x in parts[3].split(",")]
            mr_rows[(prov, stn, season)] = {
                "hours": int(vals[0]),
                "mean_aqi": vals[1],
                "mean_pm25": vals[3],
                "pm25_exc_hours": int(vals[11]),
                "severe_hours": int(vals[15])
            }

    df = pd.read_csv(os.path.join(DATA_DIR, "dataset_air_quality_gurugram.csv"), usecols=["date", "location_name", "aqi", "pm25_ugm3"])
    df["month"] = pd.to_datetime(df["date"]).dt.month
    def get_season(m):
        if m in [12, 1, 2]: return "Winter"
        elif m in [3, 4, 5]: return "Pre-Monsoon_Summer"
        elif m in [6, 7, 8, 9]: return "Monsoon"
        else: return "Post-Monsoon"

    df["season"] = df["month"].apply(get_season)
    df["prov"] = "Canonical_Benchmark"

    gt = df.groupby(["prov", "location_name", "season"]).agg(
        hours=("aqi", "count"),
        mean_aqi=("aqi", "mean"),
        mean_pm25=("pm25_ugm3", "mean"),
        pm25_exc_hours=("pm25_ugm3", lambda s: (s > 60).sum()),
        severe_hours=("aqi", lambda s: (s > 400).sum())
    ).to_dict("index")

    assert len(mr_rows) == 48, f"Expected 48 groups (12 localities x 4 seasons), got {len(mr_rows)}"
    total_hours = sum(r["hours"] for r in mr_rows.values())
    assert total_hours == 315648, f"Expected 315648 total hours, got {total_hours}"

    for k, g in gt.items():
        assert k in mr_rows, f"Missing group: {k}"
        m = mr_rows[k]
        assert m["hours"] == g["hours"]
        assert abs(m["mean_aqi"] - round(g["mean_aqi"], 1)) < 0.2
        assert abs(m["mean_pm25"] - round(g["mean_pm25"], 1)) < 0.2
        assert m["pm25_exc_hours"] == g["pm25_exc_hours"]
        assert m["severe_hours"] == g["severe_hours"]
    print("  ✓ Job 4 Verified: 48 locality-season profiles and 315,648 hours match ground truth.")

if __name__ == "__main__":
    print("=" * 60)
    print("Running MapReduce Output Independent Verification (Canonical)...")
    print("=" * 60)
    test_verify_job1()
    test_verify_job2()
    test_verify_job3()
    test_verify_job4()
    print("=" * 60)
    print("ALL MAPREDUCE OUTPUTS MATHEMATICALLY VERIFIED AGAINST CANONICAL GROUND TRUTH!")
    print("=" * 60)
