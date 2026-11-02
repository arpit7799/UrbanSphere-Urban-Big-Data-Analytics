#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 2: Vehicle Modal Split & Fleet Distribution
Mapper: Emits vehicle modal shares from dataset_traffic_gurugram.csv or vehicle composition tables.
"""

import sys
import csv

CATEGORIES = [
    ("two_wheeler", "two_wheeler_count"),
    ("car", "car_count"),
    ("auto_rickshaw", "auto_rickshaw_count"),
    ("bus", "bus_count"),
    ("truck", "truck_count"),
    ("other_vehicle", "other_vehicle_count")
]

def main():
    reader = csv.reader(sys.stdin)
    header = None

    for row in reader:
        if not row:
            continue

        if header is None:
            lower_row = [c.strip().lower() for c in row]
            if "vehicle_count" in lower_row or "two_wheeler_count" in lower_row or "vehicle_category" in lower_row:
                header = lower_row
                continue
            else:
                header = []

        try:
            if header and "vehicle_category" in header:
                cat = row[header.index("vehicle_category")].strip()
                pct_str = row[header.index("composition_pct") if "composition_pct" in header else header.index("source_percentage")].strip()
                status = row[header.index("data_status")].strip() if "data_status" in header else "observed"
                pct = float(pct_str) if pct_str and pct_str != "nan" else 0.0
                print(f"{cat}\t{pct:.4f},{status},1")
            elif header and "two_wheeler_count" in header:
                total_v = float(row[header.index("vehicle_count")].strip()) if "vehicle_count" in header else 0.0
                if total_v <= 0:
                    continue
                for cat_name, col_name in CATEGORIES:
                    if col_name in header:
                        cnt = float(row[header.index(col_name)].strip())
                        pct = (cnt / total_v) * 100.0
                        print(f"{cat_name}\t{pct:.4f},observed,1")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()
