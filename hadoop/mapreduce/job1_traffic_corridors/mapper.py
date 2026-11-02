#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 1: Traffic Corridor Volume & Capacity Stress Analysis
Mapper: Parses traffic records from dataset_traffic_gurugram.csv, extracts road_type
        (or location_type), hourly vehicle_count, and total_pcu, tagging morning/evening peak hours.
"""

import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    header = None
    
    for row in reader:
        if not row:
            continue
        
        # Detect header row
        if header is None:
            lower_row = [c.strip().lower() for c in row]
            if "road_type" in lower_row or "location_type" in lower_row or "vehicle_count" in lower_row:
                header = lower_row
                continue
            else:
                header = []
        
        try:
            if header and ("road_type" in header or "location_type" in header):
                loc_type_col = "road_type" if "road_type" in header else "location_type"
                loc_type = row[header.index(loc_type_col)].strip()
                
                v_col = "vehicle_count" if "vehicle_count" in header else "daily_total_vehicles"
                p_col = "total_pcu" if "total_pcu" in header else "daily_total_pcu"
                
                v_str = row[header.index(v_col)].strip() if v_col in header else "0"
                p_str = row[header.index(p_col)].strip() if p_col in header else "0"
                
                hour = int(row[header.index("hour")].strip()) if "hour" in header else -1
                
                # Check for existing morning/evening peak columns if available
                if "morning_peak_pcu" in header:
                    mp_str = row[header.index("morning_peak_pcu")].strip()
                    ep_str = row[header.index("evening_peak_pcu")].strip()
                    morning_pcu = float(mp_str) if mp_str and mp_str != "nan" else -1.0
                    evening_pcu = float(ep_str) if ep_str and ep_str != "nan" else -1.0
                else:
                    # In hourly canonical dataset, identify peak intervals
                    pcu_val = float(p_str) if p_str and p_str != "nan" else 0.0
                    morning_pcu = pcu_val if 8 <= hour <= 11 else -1.0
                    evening_pcu = pcu_val if 17 <= hour <= 21 else -1.0
            else:
                # Default fallback
                loc_type = row[7].strip() if len(row) > 7 else "arterial"
                v_str = row[8].strip() if len(row) > 8 else "0"
                p_str = row[15].strip() if len(row) > 15 else "0"
                morning_pcu = -1.0
                evening_pcu = -1.0

            if not loc_type:
                continue

            vehicles = float(v_str) if v_str and v_str != "nan" else 0.0
            pcu = float(p_str) if p_str and p_str != "nan" else 0.0

            # Emit: road_type \t vehicles,pcu,morning_pcu,evening_pcu,1
            print(f"{loc_type}\t{vehicles:.1f},{pcu:.1f},{morning_pcu:.1f},{evening_pcu:.1f},1")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()
