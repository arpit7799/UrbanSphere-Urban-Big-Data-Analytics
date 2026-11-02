#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 4: Multi-Station Air Quality Profiling & NAAQS Threshold Exceedance Indicators
Reducer: Computes station-wise seasonal air quality metrics, mean/max concentrations,
         and counts days exceeding national standard reference thresholds (NAAQS PM2.5 > 60 ug/m3,
         PM10 > 100 ug/m3, and Severe AQI > 400).
         NOTE: Exceedances are analytical comparisons against NAAQS reference benchmarks,
               not legally established ambient violations.
"""

import sys

def emit_result(key_tuple, aqi_sum, aqi_max, pm25_sum, pm25_max, pm10_sum, pm10_max,
                no2_sum, so2_sum, co_sum, o3_sum, pm25_exc_cnt, pm10_exc_cnt, severe_cnt, count):
    if count == 0:
        return
    prov, stn, season = key_tuple
    mean_aqi = aqi_sum / count
    mean_pm25 = pm25_sum / count
    mean_pm10 = pm10_sum / count
    mean_no2 = no2_sum / count
    mean_so2 = so2_sum / count
    mean_co = co_sum / count
    mean_o3 = o3_sum / count
    pm25_exc_pct = (pm25_exc_cnt / count) * 100.0
    pm10_exc_pct = (pm10_exc_cnt / count) * 100.0

    print(f"{prov}\t{stn}\t{season}\t{count},{mean_aqi:.1f},{aqi_max:.1f},{mean_pm25:.1f},{pm25_max:.1f},{mean_pm10:.1f},{pm10_max:.1f},{mean_no2:.1f},{mean_so2:.1f},{mean_co:.2f},{mean_o3:.1f},{pm25_exc_cnt},{pm25_exc_pct:.1f},{pm10_exc_cnt},{pm10_exc_pct:.1f},{severe_cnt}")

def main():
    current_key = None
    aqi_sum = 0.0
    aqi_max = float("-inf")
    pm25_sum = 0.0
    pm25_max = float("-inf")
    pm10_sum = 0.0
    pm10_max = float("-inf")
    no2_sum = 0.0
    so2_sum = 0.0
    co_sum = 0.0
    o3_sum = 0.0
    pm25_exc_cnt = 0
    pm10_exc_cnt = 0
    severe_cnt = 0
    count = 0

    print("# NOTE: Exceedances represent analytical comparisons against NAAQS reference thresholds for scientific evaluation, not legal enforcement determinations.")
    print("#provenance\tstation_name\tseason\ttotal_days,mean_aqi,max_aqi,mean_pm25,max_pm25,mean_pm10,max_pm10,mean_no2,mean_so2,mean_co_mg_m3,mean_o3,pm25_naaqs_exceed_days,pm25_exceed_pct,pm10_naaqs_exceed_days,pm10_exceed_pct,severe_aqi_days")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 4:
            continue

        prov, stn, season, val_str = parts[0], parts[1], parts[2], parts[3]
        key = (prov, stn, season)

        vals = val_str.split(",")
        if len(vals) < 11:
            continue

        try:
            aqi = float(vals[0])
            pm25 = float(vals[1])
            pm10 = float(vals[2])
            no2 = float(vals[3])
            so2 = float(vals[4])
            co = float(vals[5])
            o3 = float(vals[6])
            is_pm25_exc = int(vals[7])
            is_pm10_exc = int(vals[8])
            is_severe = int(vals[9])
            c = int(vals[10])
        except ValueError:
            continue

        if current_key == key:
            aqi_sum += aqi
            if aqi > aqi_max: aqi_max = aqi
            pm25_sum += pm25
            if pm25 > pm25_max: pm25_max = pm25
            pm10_sum += pm10
            if pm10 > pm10_max: pm10_max = pm10
            no2_sum += no2
            so2_sum += so2
            co_sum += co
            o3_sum += o3
            pm25_exc_cnt += is_pm25_exc
            pm10_exc_cnt += is_pm10_exc
            severe_cnt += is_severe
            count += c
        else:
            if current_key is not None:
                emit_result(current_key, aqi_sum, aqi_max, pm25_sum, pm25_max, pm10_sum, pm10_max,
                            no2_sum, so2_sum, co_sum, o3_sum, pm25_exc_cnt, pm10_exc_cnt, severe_cnt, count)
            current_key = key
            aqi_sum = aqi
            aqi_max = aqi
            pm25_sum = pm25
            pm25_max = pm25
            pm10_sum = pm10
            pm10_max = pm10
            no2_sum = no2
            so2_sum = so2
            co_sum = co
            o3_sum = o3
            pm25_exc_cnt = is_pm25_exc
            pm10_exc_cnt = is_pm10_exc
            severe_cnt = is_severe
            count = c

    if current_key is not None:
        emit_result(current_key, aqi_sum, aqi_max, pm25_sum, pm25_max, pm10_sum, pm10_max,
                    no2_sum, so2_sum, co_sum, o3_sum, pm25_exc_cnt, pm10_exc_cnt, severe_cnt, count)

if __name__ == "__main__":
    main()
