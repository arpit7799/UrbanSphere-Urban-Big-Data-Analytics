# UrbanSphere — Hadoop Streaming MapReduce Processing Engine (Canonical)

## 1. Overview
The UrbanSphere MapReduce layer implements distributed batch aggregation pipelines using the **Apache Hadoop Streaming** paradigm (`stdin` $\to$ line processing $\to$ `stdout` tab-separated key-value pairs).

The jobs run in two operational modes:
1. **Local Mode (Standalone):** Executable on any POSIX system without requiring a running Hadoop cluster daemon via Unix pipes (`cat input.csv | python3 mapper.py | sort -k1,1 | python3 reducer.py > output.txt`).
2. **Cluster Mode (Distributed HDFS/YARN):** Submittable to a live Apache Hadoop cluster via `hadoop jar hadoop-streaming*.jar` reading from canonical datasets and writing to `/urbansphere/output/mapreduce/`.

---

## 2. Implemented MapReduce Jobs (Canonical 2022–2024 Datasets)

### Job 1: Traffic Corridor Volume & Capacity Stress Analysis
* **Directory:** `job1_traffic_corridors/` (`mapper.py`, `reducer.py`)
* **Input Dataset:** `data/dataset_traffic_gurugram.csv` (Canonical 315,648 hourly records).
* **Mapper Key-Value Contract:**
  * **Key:** `road_type` (e.g., `arterial`, `highway_arterial`, `junction_arterial`, `urban`, `urban_arterial`)
  * **Value:** `vehicle_count,total_pcu,morning_peak_pcu,evening_peak_pcu,1`
* **Reducer Output Schema:**
  `location_type \t location_count,total_vehicles,total_pcu,avg_vehicles_per_loc,avg_pcu_per_loc,pcu_factor,avg_morning_peak_pcu,avg_evening_peak_pcu`
* **Output Artifact:** `output/mapreduce/job1_traffic_corridors_canonical.txt`
* **Analytical Purpose:** Evaluates total arterial network load, volume-to-capacity ratios, and PCU conversion factors across road types.

---

### Job 2: Vehicle Modal Split & Fleet Distribution
* **Directory:** `job2_vehicle_composition/` (`mapper.py`, `reducer.py`)
* **Input Dataset:** `data/dataset_traffic_gurugram.csv` (Canonical 315,648 hourly records).
* **Mapper Key-Value Contract:**
  * **Key:** `vehicle_category` (e.g., `two_wheeler`, `car`, `auto_rickshaw`, `bus`, `truck`, `other_vehicle`)
  * **Value:** `composition_pct,data_status,1`
* **Reducer Output Schema:**
  `vehicle_category \t total_observations,mean_share_pct,min_share_pct,max_share_pct,observed_locations,derived_locations`
* **Output Artifact:** `output/mapreduce/job2_vehicle_composition_modal_split.txt`
* **Analytical Purpose:** Computes modal share hierarchy across Gurugram, identifying transit reliance on private vs. intermediate public transport (IPT).

---

### Job 3: Meteorological Extremes & Diurnal Temperature Range
* **Directory:** `job3_weather_extremes/` (`mapper.py`, `reducer.py`)
* **Input Dataset:** `data/dataset_weather_gurugram_with_aqi.csv` (Canonical 315,648 hourly records across 2022–2024).
* **Mapper Key-Value Contract:**
  * **Key:** `year_month` (e.g., `2024-05`)
  * **Value:** `temp,humidity,precipitation,pressure,wind_speed,1`
* **Reducer Output Schema:**
  `year_month \t total_hours,t_min_c,t_max_c,t_mean_c,dtr_c,heatwave_hours,coldwave_hours,high_wind_hours,precipitation_total_mm,mean_mslp_hpa,mean_humidity_pct`
* **Output Artifact:** `output/mapreduce/job3_weather_extremes_monthly.txt`
* **Analytical Purpose:** Establishes multi-year monthly climate baselines, Diurnal Temperature Range (DTR), heatwave hours ($T \ge 40^\circ\text{C}$), coldwave hours ($T \le 7^\circ\text{C}$), and barometric pressure patterns.

---

### Job 4: Multi-Station Air Quality Profiling & NAAQS Threshold Indicators
* **Directory:** `job4_air_quality_profiling/` (`mapper.py`, `reducer.py`)
* **Input Dataset:** `data/dataset_air_quality_gurugram.csv` (Canonical 315,648 hourly records).
* **Mapper Key-Value Contract:**
  * **Key:** `provenance \t location_name \t season` (e.g., `Canonical_Benchmark \t Cyber City \t Winter`)
  * **Value:** `aqi,pm25,pm10,no2,so2,co,o3,is_pm25_exceed,is_pm10_exceed,is_severe,1`
* **Reducer Output Schema:**
  `provenance \t station_name \t season \t total_hours,mean_aqi,max_aqi,mean_pm25,max_pm25,mean_pm10,max_pm10,mean_no2,mean_so2,mean_co_mg_m3,mean_o3,pm25_naaqs_exceed_hours,pm25_exceed_pct,pm10_naaqs_exceed_hours,pm10_exceed_pct,severe_aqi_hours`
* **Output Artifact:** `output/mapreduce/job4_air_quality_profiling_seasonal.txt`
* **Scientific Note:** Exceedances represent analytical comparisons against National Ambient Air Quality Standards (24-hour PM2.5 $> 60\,\mu\text{g/m}^3$; PM10 $> 100\,\mu\text{g/m}^3$; Severe AQI $> 400$). They indicate threshold violations for scientific evaluation, not legal enforcement determinations.

---

## 3. Execution & Verification

### Local Execution
```bash
bash hadoop/mapreduce/run_mapreduce_local.sh
```

### Mathematical Verification against Pandas Ground Truth
```bash
python3 hadoop/mapreduce/verify_mapreduce_outputs.py
```

### Unit Tests
```bash
python3 -m unittest hadoop/mapreduce/test_mapreduce_jobs.py
```
