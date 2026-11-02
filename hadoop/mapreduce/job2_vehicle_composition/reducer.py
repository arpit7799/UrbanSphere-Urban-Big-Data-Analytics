#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 2: Vehicle Modal Split & Fleet Distribution
Reducer: Computes mean modal share percentage, min/max ranges, and observation counts per vehicle category.
"""

import sys

def emit_result(cat, total_pct, min_pct, max_pct, count_obs, count_der, count_tot):
    if count_tot == 0:
        return
    mean_pct = total_pct / count_tot
    print(f"{cat}\t{count_tot},{mean_pct:.2f},{min_pct:.2f},{max_pct:.2f},{count_obs},{count_der}")

def main():
    current_key = None
    total_pct = 0.0
    min_pct = float("inf")
    max_pct = float("-inf")
    count_obs = 0
    count_der = 0
    count_tot = 0

    print("#vehicle_category\ttotal_observations,mean_share_pct,min_share_pct,max_share_pct,observed_locations,derived_locations")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        key, val_str = parts[0], parts[1]
        vals = val_str.split(",")
        if len(vals) < 3:
            continue

        try:
            pct = float(vals[0])
            status = vals[1].strip().lower()
            c = int(vals[2])
        except ValueError:
            continue

        if current_key == key:
            total_pct += pct
            if pct < min_pct: min_pct = pct
            if pct > max_pct: max_pct = pct
            if "obs" in status: count_obs += 1
            elif "der" in status: count_der += 1
            count_tot += c
        else:
            if current_key is not None:
                emit_result(current_key, total_pct, min_pct, max_pct, count_obs, count_der, count_tot)
            current_key = key
            total_pct = pct
            min_pct = pct
            max_pct = pct
            count_obs = 1 if "obs" in status else 0
            count_der = 1 if "der" in status else 0
            count_tot = c

    if current_key is not None:
        emit_result(current_key, total_pct, min_pct, max_pct, count_obs, count_der, count_tot)

if __name__ == "__main__":
    main()
