#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 3: Meteorological Extremes & Diurnal Temperature Range
Mapper: Parses hourly weather observations, extracts year-month, temperature, humidity,
        precipitation, MSLP/pressure, and wind speed.
"""

import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    header = None

    for row in reader:
        if not row:
            continue

        if header is None:
            lower_row = [c.strip().lower() for c in row]
            if "temperature_c" in lower_row or "timestamp" in lower_row:
                header = lower_row
                continue
            else:
                header = []

        try:
            if header and "temperature_c" in header:
                date_str = row[header.index("date")].strip() if "date" in header else row[header.index("timestamp")].strip()
                ym = date_str[:7]
                
                t_str = row[header.index("temperature_c")].strip()
                h_str = row[header.index("relative_humidity_pct") if "relative_humidity_pct" in header else header.index("humidity_pct")].strip()
                p_str = row[header.index("precipitation_mm")].strip() if "precipitation_mm" in header else "0.0"
                
                # Prioritize mslp_hpa if present, otherwise surface_pressure_hpa
                p_col = "mslp_hpa" if "mslp_hpa" in header else ("surface_pressure_hpa" if "surface_pressure_hpa" in header else "pressure_hpa")
                m_str = row[header.index(p_col)].strip() if p_col in header else "1013.25"
                w_str = row[header.index("wind_speed_kmh")].strip() if "wind_speed_kmh" in header else "0.0"
            else:
                date_str = row[1].strip() if len(row) > 1 else ""
                ym = date_str[:7] if len(date_str) >= 7 else "2022-01"
                t_str = row[6].strip() if len(row) > 6 else "20.0"
                h_str = row[7].strip() if len(row) > 7 else "50.0"
                w_str = row[8].strip() if len(row) > 8 else "10.0"
                m_str = row[9].strip() if len(row) > 9 else "1013.25"
                p_str = row[11].strip() if len(row) > 11 else "0.0"

            if not ym or len(ym) < 7:
                continue

            temp = float(t_str) if t_str and t_str != "nan" else 20.0
            hum = float(h_str) if h_str and h_str != "nan" else 50.0
            precip = float(p_str) if p_str and p_str != "nan" else 0.0
            mslp = float(m_str) if m_str and m_str != "nan" else 1013.25
            wind = float(w_str) if w_str and w_str != "nan" else 0.0

            # Emit: year_month \t temp,hum,precip,mslp,wind,1
            print(f"{ym}\t{temp:.2f},{hum:.1f},{precip:.2f},{mslp:.1f},{wind:.1f},1")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()
