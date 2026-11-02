-- =============================================================================
-- UrbanSphere — PySpark SQL Analytical Query Suite (Canonical 2022-2024 Datasets)
-- =============================================================================
-- Tables registered from canonical datasets:
--   - traffic (data/dataset_traffic_gurugram.csv)
--   - weather (data/dataset_weather_gurugram_with_aqi.csv)
--   - air_quality (data/dataset_air_quality_gurugram.csv)
--   - geography (data/dataset_geography_gurugram.csv)
--   - urban_daily (data/processed/integrated/urban_integrated_daily.parquet)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Query 1: Corridor Volume & Road Type Analysis
-- -----------------------------------------------------------------------------
SELECT 
    road_type AS location_type,
    COUNT(DISTINCT location_name) AS location_count,
    ROUND(SUM(vehicle_count), 1) AS total_vehicles,
    ROUND(SUM(total_pcu), 1) AS total_pcu,
    ROUND(AVG(vehicle_count), 1) AS avg_vehicles_per_loc,
    ROUND(AVG(total_pcu), 1) AS avg_pcu_per_loc,
    ROUND(SUM(total_pcu) / SUM(vehicle_count), 2) AS pcu_to_vehicle_ratio,
    ROUND(AVG(CASE WHEN hour BETWEEN 8 AND 11 THEN total_pcu ELSE NULL END), 1) AS avg_morning_peak_pcu,
    ROUND(AVG(CASE WHEN hour BETWEEN 17 AND 21 THEN total_pcu ELSE NULL END), 1) AS avg_evening_peak_pcu
FROM traffic
GROUP BY road_type
ORDER BY total_pcu DESC;

-- -----------------------------------------------------------------------------
-- Query 2: Vehicle Fleet Composition & Modal Split Distribution
-- -----------------------------------------------------------------------------
SELECT 
    'two_wheeler' AS vehicle_category, COUNT(*) AS observation_count,
    ROUND(SUM(two_wheeler_count) * 100.0 / SUM(vehicle_count), 2) AS mean_share_pct,
    ROUND(MIN(two_wheeler_count * 100.0 / vehicle_count), 2) AS min_share_pct,
    ROUND(MAX(two_wheeler_count * 100.0 / vehicle_count), 2) AS max_share_pct,
    COUNT(DISTINCT location_name) AS observed_locations, 0 AS derived_locations
FROM traffic WHERE vehicle_count > 0
UNION ALL
SELECT 
    'car' AS vehicle_category, COUNT(*) AS observation_count,
    ROUND(SUM(car_count) * 100.0 / SUM(vehicle_count), 2) AS mean_share_pct,
    ROUND(MIN(car_count * 100.0 / vehicle_count), 2) AS min_share_pct,
    ROUND(MAX(car_count * 100.0 / vehicle_count), 2) AS max_share_pct,
    COUNT(DISTINCT location_name) AS observed_locations, 0 AS derived_locations
FROM traffic WHERE vehicle_count > 0
UNION ALL
SELECT 
    'auto_rickshaw' AS vehicle_category, COUNT(*) AS observation_count,
    ROUND(SUM(auto_rickshaw_count) * 100.0 / SUM(vehicle_count), 2) AS mean_share_pct,
    ROUND(MIN(auto_rickshaw_count * 100.0 / vehicle_count), 2) AS min_share_pct,
    ROUND(MAX(auto_rickshaw_count * 100.0 / vehicle_count), 2) AS max_share_pct,
    COUNT(DISTINCT location_name) AS observed_locations, 0 AS derived_locations
FROM traffic WHERE vehicle_count > 0
UNION ALL
SELECT 
    'bus' AS vehicle_category, COUNT(*) AS observation_count,
    ROUND(SUM(bus_count) * 100.0 / SUM(vehicle_count), 2) AS mean_share_pct,
    ROUND(MIN(bus_count * 100.0 / vehicle_count), 2) AS min_share_pct,
    ROUND(MAX(bus_count * 100.0 / vehicle_count), 2) AS max_share_pct,
    COUNT(DISTINCT location_name) AS observed_locations, 0 AS derived_locations
FROM traffic WHERE vehicle_count > 0
UNION ALL
SELECT 
    'truck' AS vehicle_category, COUNT(*) AS observation_count,
    ROUND(SUM(truck_count) * 100.0 / SUM(vehicle_count), 2) AS mean_share_pct,
    ROUND(MIN(truck_count * 100.0 / vehicle_count), 2) AS min_share_pct,
    ROUND(MAX(truck_count * 100.0 / vehicle_count), 2) AS max_share_pct,
    COUNT(DISTINCT location_name) AS observed_locations, 0 AS derived_locations
FROM traffic WHERE vehicle_count > 0
UNION ALL
SELECT 
    'other_vehicle' AS vehicle_category, COUNT(*) AS observation_count,
    ROUND(SUM(other_vehicle_count) * 100.0 / SUM(vehicle_count), 2) AS mean_share_pct,
    ROUND(MIN(other_vehicle_count * 100.0 / vehicle_count), 2) AS min_share_pct,
    ROUND(MAX(other_vehicle_count * 100.0 / vehicle_count), 2) AS max_share_pct,
    COUNT(DISTINCT location_name) AS observed_locations, 0 AS derived_locations
FROM traffic WHERE vehicle_count > 0;

-- -----------------------------------------------------------------------------
-- Query 3: Multi-Year Monthly Climate Baselines & Extreme Weather Hours
-- -----------------------------------------------------------------------------
SELECT 
    SUBSTRING(date, 1, 7) AS year_month,
    COUNT(*) AS total_hours,
    ROUND(MIN(temperature_c), 1) AS t_min_c,
    ROUND(MAX(temperature_c), 1) AS t_max_c,
    ROUND(AVG(temperature_c), 2) AS t_mean_c,
    ROUND(MAX(temperature_c) - MIN(temperature_c), 1) AS dtr_c,
    SUM(CASE WHEN temperature_c >= 40.0 THEN 1 ELSE 0 END) AS heatwave_hours,
    SUM(CASE WHEN temperature_c <= 7.0 THEN 1 ELSE 0 END) AS coldwave_hours,
    SUM(CASE WHEN wind_speed_kmh >= 20.0 THEN 1 ELSE 0 END) AS high_wind_hours,
    ROUND(SUM(COALESCE(precipitation_mm, 0)), 1) AS precipitation_total_mm,
    ROUND(AVG(surface_pressure_hpa), 1) AS mean_mslp_hpa,
    ROUND(AVG(relative_humidity_pct), 1) AS mean_humidity_pct
FROM weather
GROUP BY SUBSTRING(date, 1, 7)
ORDER BY year_month ASC;

-- -----------------------------------------------------------------------------
-- Query 4: Multi-Locality Air Quality Profiling & NAAQS Threshold Indicators
-- -----------------------------------------------------------------------------
SELECT 
    'Canonical_Benchmark' AS provenance,
    location_name AS station_name,
    CASE 
        WHEN CAST(SUBSTRING(date, 6, 2) AS INT) IN (12, 1, 2) THEN 'Winter'
        WHEN CAST(SUBSTRING(date, 6, 2) AS INT) IN (3, 4, 5) THEN 'Pre-Monsoon_Summer'
        WHEN CAST(SUBSTRING(date, 6, 2) AS INT) IN (6, 7, 8, 9) THEN 'Monsoon'
        ELSE 'Post-Monsoon'
    END AS season,
    COUNT(*) AS total_days,
    ROUND(AVG(aqi), 1) AS mean_aqi,
    ROUND(MAX(aqi), 1) AS max_aqi,
    ROUND(AVG(pm25_ugm3), 1) AS mean_pm25,
    ROUND(MAX(pm25_ugm3), 1) AS max_pm25,
    ROUND(AVG(pm10_ugm3), 1) AS mean_pm10,
    ROUND(MAX(pm10_ugm3), 1) AS max_pm10,
    ROUND(AVG(no2_ugm3), 1) AS mean_no2,
    ROUND(AVG(so2_ugm3), 1) AS mean_so2,
    ROUND(AVG(co_mg_m3), 2) AS mean_co_mg_m3,
    ROUND(AVG(o3_ugm3), 1) AS mean_o3,
    SUM(CASE WHEN pm25_ugm3 > 60.0 THEN 1 ELSE 0 END) AS pm25_naaqs_exceed_days,
    ROUND(SUM(CASE WHEN pm25_ugm3 > 60.0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pm25_exceed_pct,
    SUM(CASE WHEN pm10_ugm3 > 100.0 THEN 1 ELSE 0 END) AS pm10_naaqs_exceed_days,
    ROUND(SUM(CASE WHEN pm10_ugm3 > 100.0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pm10_exceed_pct,
    SUM(CASE WHEN aqi > 400.0 THEN 1 ELSE 0 END) AS severe_aqi_days
FROM air_quality
GROUP BY 
    location_name,
    CASE 
        WHEN CAST(SUBSTRING(date, 6, 2) AS INT) IN (12, 1, 2) THEN 'Winter'
        WHEN CAST(SUBSTRING(date, 6, 2) AS INT) IN (3, 4, 5) THEN 'Pre-Monsoon_Summer'
        WHEN CAST(SUBSTRING(date, 6, 2) AS INT) IN (6, 7, 8, 9) THEN 'Monsoon'
        ELSE 'Post-Monsoon'
    END
ORDER BY location_name, season;

-- -----------------------------------------------------------------------------
-- Query 5: Atmospheric Ventilation & Pollutant Dispersion Analysis
-- -----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN wind_speed_mean_kmh < 5.0 THEN '1_Stagnant (<5 km/h)'
        WHEN wind_speed_mean_kmh BETWEEN 5.0 AND 10.0 THEN '2_Light_Breeze (5-10 km/h)'
        WHEN wind_speed_mean_kmh BETWEEN 10.0 AND 15.0 THEN '3_Moderate_Breeze (10-15 km/h)'
        ELSE '4_Strong_Dispersion (>15 km/h)'
    END AS ventilation_category,
    COUNT(*) AS total_days,
    ROUND(AVG(wind_speed_mean_kmh), 1) AS avg_wind_speed_kmh,
    ROUND(AVG(pm25_mean_ugm3), 1) AS avg_pm25_ug_m3,
    ROUND(AVG(pm10_mean_ugm3), 1) AS avg_pm10_ug_m3,
    ROUND(AVG(no2_mean_ugm3), 1) AS avg_no2_ug_m3,
    ROUND(AVG(air_quality_aqi_max), 1) AS avg_max_aqi,
    SUM(CASE WHEN air_quality_aqi_max > 400.0 THEN 1 ELSE 0 END) AS severe_aqi_days,
    ROUND(SUM(CASE WHEN air_quality_aqi_max > 400.0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS severe_aqi_day_pct
FROM urban_daily
GROUP BY 
    CASE 
        WHEN wind_speed_mean_kmh < 5.0 THEN '1_Stagnant (<5 km/h)'
        WHEN wind_speed_mean_kmh BETWEEN 5.0 AND 10.0 THEN '2_Light_Breeze (5-10 km/h)'
        WHEN wind_speed_mean_kmh BETWEEN 10.0 AND 15.0 THEN '3_Moderate_Breeze (10-15 km/h)'
        ELSE '4_Strong_Dispersion (>15 km/h)'
    END
ORDER BY ventilation_category ASC;

-- -----------------------------------------------------------------------------
-- Query 6: Spatial Transit Corridor & Municipal Zone Profile
-- -----------------------------------------------------------------------------
SELECT 
    representative_corridor AS nearest_transit_corridor,
    COUNT(location_id) AS sector_count,
    ROUND(MIN(latitude), 4) AS min_latitude,
    ROUND(MAX(latitude), 4) AS max_latitude,
    ROUND(MIN(longitude), 4) AS min_longitude,
    ROUND(MAX(longitude), 4) AS max_longitude,
    235.0 AS mean_elevation_m
FROM geography
GROUP BY representative_corridor
ORDER BY sector_count DESC;
