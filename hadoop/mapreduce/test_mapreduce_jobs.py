#!/usr/bin/env python3
"""
Unit and Integration Tests for UrbanSphere MapReduce Jobs
========================================================
Tests mapper and reducer handling of:
1. Canonical datasets and schemas
2. Normal valid rows and headers
3. Malformed rows / missing values
4. End-to-end POSIX pipe execution
"""

import subprocess
import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PYTHON = sys.executable

def run_pipe(mapper_script, reducer_script, input_data):
    p_map = subprocess.Popen([PYTHON, mapper_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_map, err_map = p_map.communicate(input=input_data)
    assert p_map.returncode == 0, f"Mapper failed: {err_map}"

    # Sort
    lines = [l for l in out_map.strip().split("\n") if l]
    lines.sort()
    sorted_input = "\n".join(lines) + "\n" if lines else ""

    p_red = subprocess.Popen([PYTHON, reducer_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_red, err_red = p_red.communicate(input=sorted_input)
    assert p_red.returncode == 0, f"Reducer failed: {err_red}"
    return out_red

class TestMapReduceJobs(unittest.TestCase):
    """Unit test cases for the 4 Hadoop MapReduce jobs."""

    def test_job1_canonical_unit(self):
        mapper = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job1_traffic_corridors/mapper.py")
        reducer = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job1_traffic_corridors/reducer.py")
        raw_data = """timestamp,date,hour,location_name,latitude,longitude,road_name,road_type,vehicle_count,two_wheeler_count,car_count,auto_rickshaw_count,bus_count,truck_count,other_vehicle_count,total_pcu,average_speed_kmh,congestion_level
2024-05-01 09:00:00,2024-05-01,9,Cyber City,28.49,77.09,Cyber City Ring Road,arterial,500,200,200,40,20,30,10,550.0,25.0,High
2024-05-01 18:00:00,2024-05-01,18,Cyber City,28.49,77.09,Cyber City Ring Road,arterial,600,250,250,40,20,30,10,650.0,22.0,High
MALFORMED,ROW,TOO,FEW
"""
        out = run_pipe(mapper, reducer, raw_data)
        self.assertIn("arterial", out)
        self.assertIn("2,1100.0,1200.0,550.0,600.0,1.09,550.0,650.0", out)

    def test_job2_canonical_unit(self):
        mapper = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job2_vehicle_composition/mapper.py")
        reducer = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job2_vehicle_composition/reducer.py")
        raw_data = """timestamp,date,hour,location_name,latitude,longitude,road_name,road_type,vehicle_count,two_wheeler_count,car_count,auto_rickshaw_count,bus_count,truck_count,other_vehicle_count,total_pcu,average_speed_kmh,congestion_level
2024-05-01 09:00:00,2024-05-01,9,Cyber City,28.49,77.09,Cyber City Ring Road,arterial,100,40,30,10,5,10,5,110.0,25.0,High
2024-05-01 10:00:00,2024-05-01,10,Cyber City,28.49,77.09,Cyber City Ring Road,arterial,200,80,60,20,10,20,10,220.0,25.0,High
"""
        out = run_pipe(mapper, reducer, raw_data)
        self.assertIn("car\t2,30.00,30.00,30.00,2,0", out)
        self.assertIn("two_wheeler\t2,40.00,40.00,40.00,2,0", out)

    def test_job3_canonical_unit(self):
        mapper = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job3_weather_extremes/mapper.py")
        reducer = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job3_weather_extremes/reducer.py")
        raw_data = """timestamp,date,hour,location_name,latitude,longitude,temperature_c,relative_humidity_pct,wind_speed_kmh,surface_pressure_hpa,cloud_cover_pct,precipitation_mm,weather_condition,aqi,aqi_category
2024-05-01 00:00:00,2024-05-01,0,Cyber City,28.49,77.09,30.0,50.0,10.0,980.0,20.0,0.0,Clear,150,Moderate
2024-05-01 14:00:00,2024-05-01,14,Cyber City,28.49,77.09,42.0,20.0,25.0,975.0,10.0,5.0,Clear,220,Poor
"""
        out = run_pipe(mapper, reducer, raw_data)
        self.assertIn("2024-05\t2,30.0,42.0,36.00,12.0,1,0,1,5.0,977.5,35.0", out)

    def test_job4_canonical_unit(self):
        mapper = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job4_air_quality_profiling/mapper.py")
        reducer = os.path.join(PROJECT_ROOT, "hadoop/mapreduce/job4_air_quality_profiling/reducer.py")
        raw_data = """timestamp,date,hour,location_name,latitude,longitude,pm25_ugm3,pm10_ugm3,no2_ugm3,so2_ugm3,co_mg_m3,o3_ugm3,aqi,aqi_category
2024-01-15 09:00:00,2024-01-15,9,Cyber City,28.49,77.09,120.0,250.0,40.0,10.0,2.0,30.0,305,Very Poor
2024-01-16 10:00:00,2024-01-16,10,Cyber City,28.49,77.09,300.0,500.0,60.0,20.0,3.5,40.0,420,Severe
"""
        out = run_pipe(mapper, reducer, raw_data)
        self.assertIn("Canonical_Benchmark\tCyber City\tWinter\t2,362.5,420.0,210.0,300.0,375.0,500.0,50.0,15.0,2.75,35.0,2,100.0,2,100.0,1", out)

if __name__ == "__main__":
    unittest.main()
