#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 4: Multi-Locality Air Quality Profiling & NAAQS Threshold Exceedances
Mapper: Parses hourly air quality observations, categorizes season, and emits
        pollutants with NAAQS 24-hr threshold exceedance flags (PM2.5 > 60, PM10 > 100, AQI > 400).
"""

import sys
import csv

def get_season(month_int):
    if month_int in (12, 1, 2):
        return "Winter"
    elif month_int in (3, 4, 5):
        return "Pre-Monsoon_Summer"
    elif month_int in (6, 7, 8, 9):
        return "Monsoon"
    else:
        return "Post-Monsoon"

def main():
    reader = csv.reader(sys.stdin)
    header = None

    for row in reader:
        if not row:
            continue

        if header is None:
            lower_row = [c.strip().lower() for c in row]
            if "location_name" in lower_row or "station_name" in lower_row or "pm25_ugm3" in lower_row or "pm25" in lower_row:
                header = lower_row
                continue
            else:
                header = []

        try:
            if header and ("location_name" in header or "station_name" in header):
                stn_col = "location_name" if "location_name" in header else "station_name"
                stn = row[header.index(stn_col)].strip()
                
                date_str = row[header.index("date")].strip() if "date" in header else row[header.index("timestamp")].strip()
                month = int(date_str[5:7]) if len(date_str) >= 7 else 1
                season = get_season(month)
                
                if "data_status" in header and "obs" in row[header.index("data_status")].lower():
                    prov = "Observed_CAAQMS_Station"
                else:
                    prov = "Canonical_Benchmark"
                
                p25_col = "pm25_ugm3" if "pm25_ugm3" in header else ("pm25" if "pm25" in header else "pm2_5_ug_m3")
                p10_col = "pm10_ugm3" if "pm10_ugm3" in header else ("pm10" if "pm10" in header else "pm10_ug_m3")
                no2_col = "no2_ugm3" if "no2_ugm3" in header else ("no2" if "no2" in header else "no2_ug_m3")
                so2_col = "so2_ugm3" if "so2_ugm3" in header else ("so2" if "so2" in header else "so2_ug_m3")
                co_col = "co_mg_m3" if "co_mg_m3" in header else ("co" if "co" in header else "co_mg_m3")
                o3_col = "o3_ugm3" if "o3_ugm3" in header else ("o3" if "o3" in header else "o3_ug_m3")
                aqi_col = "aqi" if "aqi" in header else "daily_city_max_aqi"
                
                p25_str = row[header.index(p25_col)].strip()
                p10_str = row[header.index(p10_col)].strip()
                no2_str = row[header.index(no2_col)].strip()
                so2_str = row[header.index(so2_col)].strip()
                co_str = row[header.index(co_col)].strip()
                o3_str = row[header.index(o3_col)].strip()
                aqi_str = row[header.index(aqi_col)].strip()
            else:
                prov = "Canonical_Benchmark"
                stn = row[3].strip() if len(row) > 3 else "Locality"
                date_str = row[1].strip() if len(row) > 1 else ""
                month = int(date_str[5:7]) if len(date_str) >= 7 else 1
                season = get_season(month)
                p25_str = row[6].strip() if len(row) > 6 else "50"
                p10_str = row[7].strip() if len(row) > 7 else "100"
                no2_str = row[8].strip() if len(row) > 8 else "40"
                so2_str = row[9].strip() if len(row) > 9 else "15"
                co_str = row[10].strip() if len(row) > 10 else "1.0"
                o3_str = row[11].strip() if len(row) > 11 else "40"
                aqi_str = row[12].strip() if len(row) > 12 else "150"

            if not stn:
                continue

            pm25 = float(p25_str) if p25_str and p25_str != "nan" else 0.0
            pm10 = float(p10_str) if p10_str and p10_str != "nan" else 0.0
            no2 = float(no2_str) if no2_str and no2_str != "nan" else 0.0
            so2 = float(so2_str) if so2_str and so2_str != "nan" else 0.0
            co = float(co_str) if co_str and co_str != "nan" else 0.0
            o3 = float(o3_str) if o3_str and o3_str != "nan" else 0.0
            aqi = float(aqi_str) if aqi_str and aqi_str != "nan" else 0.0

            # NAAQS Reference Threshold comparisons (PM2.5 > 60, PM10 > 100, Severe AQI > 400)
            is_pm25_exc = 1 if pm25 > 60.0 else 0
            is_pm10_exc = 1 if pm10 > 100.0 else 0
            is_severe = 1 if aqi > 400.0 else 0

            # Emit: prov \t stn \t season \t aqi,pm25,pm10,no2,so2,co,o3,is_pm25_exc,is_pm10_exc,is_severe,1
            print(f"{prov}\t{stn}\t{season}\t{aqi:.1f},{pm25:.1f},{pm10:.1f},{no2:.1f},{so2:.1f},{co:.2f},{o3:.1f},{is_pm25_exc},{is_pm10_exc},{is_severe},1")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()
