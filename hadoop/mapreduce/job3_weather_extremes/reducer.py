#!/usr/bin/env python3
"""
UrbanSphere MapReduce Job 3: Meteorological Extremes & Diurnal Temperature Range
Reducer: Aggregates hourly meteorological observations into monthly climate indicators:
         T_min, T_max, T_mean, DTR, heatwave hours (T>=40C), coldwave hours (T<=7C),
         high-wind hours (>=20 km/h), total precipitation, mean MSLP, and mean humidity.
"""

import sys

def emit_result(ym, t_sum, t_min, t_max, h_sum, p_sum, m_sum, w_sum, hw_count, cw_count, wind_count, count):
    if count == 0:
        return
    t_mean = t_sum / count
    dtr = t_max - t_min
    h_mean = h_sum / count
    m_mean = m_sum / count
    w_mean = w_sum / count
    
    print(f"{ym}\t{count},{t_min:.1f},{t_max:.1f},{t_mean:.2f},{dtr:.1f},{hw_count},{cw_count},{wind_count},{p_sum:.1f},{m_mean:.1f},{h_mean:.1f}")

def main():
    current_key = None
    t_sum = 0.0
    t_min = float("inf")
    t_max = float("-inf")
    h_sum = 0.0
    p_sum = 0.0
    m_sum = 0.0
    w_sum = 0.0
    hw_count = 0
    cw_count = 0
    wind_count = 0
    count = 0

    print("#year_month\ttotal_hours,t_min_c,t_max_c,t_mean_c,dtr_c,heatwave_hours,coldwave_hours,high_wind_hours,precipitation_total_mm,mean_mslp_hpa,mean_humidity_pct")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        key, val_str = parts[0], parts[1]
        vals = val_str.split(",")
        if len(vals) < 6:
            continue

        try:
            temp = float(vals[0])
            hum = float(vals[1])
            precip = float(vals[2])
            mslp = float(vals[3])
            wind = float(vals[4])
            c = int(vals[5])
        except ValueError:
            continue

        is_hw = 1 if temp >= 40.0 else 0
        is_cw = 1 if temp <= 7.0 else 0
        is_wind = 1 if wind >= 20.0 else 0

        if current_key == key:
            t_sum += temp
            if temp < t_min: t_min = temp
            if temp > t_max: t_max = temp
            h_sum += hum
            p_sum += precip
            m_sum += mslp
            w_sum += wind
            hw_count += is_hw
            cw_count += is_cw
            wind_count += is_wind
            count += c
        else:
            if current_key is not None:
                emit_result(current_key, t_sum, t_min, t_max, h_sum, p_sum, m_sum, w_sum, hw_count, cw_count, wind_count, count)
            current_key = key
            t_sum = temp
            t_min = temp
            t_max = temp
            h_sum = hum
            p_sum = precip
            m_sum = mslp
            w_sum = wind
            hw_count = is_hw
            cw_count = is_cw
            wind_count = is_wind
            count = c

    if current_key is not None:
        emit_result(current_key, t_sum, t_min, t_max, h_sum, p_sum, m_sum, w_sum, hw_count, cw_count, wind_count, count)

if __name__ == "__main__":
    main()
