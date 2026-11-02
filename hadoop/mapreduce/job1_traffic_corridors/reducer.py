#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 1: Traffic Corridor Volume & Capacity Stress Analysis
Reducer: Aggregates total vehicle volumes, PCUs, and peak concentration ratios by location type.
"""

import sys

def emit_result(loc_type, total_v, total_p, morning_p, morning_cnt, evening_p, evening_cnt, count):
    if count == 0:
        return
    avg_v = total_v / count
    avg_p = total_p / count
    pcu_factor = (total_p / total_v) if total_v > 0 else 1.0
    avg_mp = (morning_p / morning_cnt) if morning_cnt > 0 else 0.0
    avg_ep = (evening_p / evening_cnt) if evening_cnt > 0 else 0.0
    
    # Header emitted if not already printed:
    # location_type \t num_locations,total_vehicles,total_pcu,avg_vehicles,avg_pcu,pcu_factor,avg_morning_peak_pcu,avg_evening_peak_pcu
    print(f"{loc_type}\t{count},{total_v:.1f},{total_p:.1f},{avg_v:.1f},{avg_p:.1f},{pcu_factor:.2f},{avg_mp:.1f},{avg_ep:.1f}")

def main():
    current_key = None
    total_vehicles = 0.0
    total_pcu = 0.0
    total_morning_pcu = 0.0
    count_morning = 0
    total_evening_pcu = 0.0
    count_evening = 0
    count = 0

    print("#location_type\tlocation_count,total_vehicles,total_pcu,avg_vehicles_per_loc,avg_pcu_per_loc,pcu_factor,avg_morning_peak_pcu,avg_evening_peak_pcu")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        key, val_str = parts[0], parts[1]
        vals = val_str.split(",")
        if len(vals) < 5:
            continue

        try:
            v = float(vals[0])
            p = float(vals[1])
            mp = float(vals[2])
            ep = float(vals[3])
            c = int(vals[4])
        except ValueError:
            continue

        if current_key == key:
            total_vehicles += v
            total_pcu += p
            if mp >= 0:
                total_morning_pcu += mp
                count_morning += 1
            if ep >= 0:
                total_evening_pcu += ep
                count_evening += 1
            count += c
        else:
            if current_key is not None:
                emit_result(current_key, total_vehicles, total_pcu, total_morning_pcu, count_morning, total_evening_pcu, count_evening, count)
            current_key = key
            total_vehicles = v
            total_pcu = p
            if mp >= 0:
                total_morning_pcu = mp
                count_morning = 1
            else:
                total_morning_pcu = 0.0
                count_morning = 0
            if ep >= 0:
                total_evening_pcu = ep
                count_evening = 1
            else:
                total_evening_pcu = 0.0
                count_evening = 0
            count = c

    if current_key is not None:
        emit_result(current_key, total_vehicles, total_pcu, total_morning_pcu, count_morning, total_evening_pcu, count_evening, count)

if __name__ == "__main__":
    main()
