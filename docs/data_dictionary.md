# UrbanSphere — Data Dictionary (Canonical 2022–2024 Datasets)

## 1. Canonical Weather Dataset (`data/dataset_weather_gurugram_with_aqi.csv`)
- **Rows**: 315,648 (Hourly records, 2022-01-01 00:00 to 2024-12-31 23:00, 12 localities)
- **Columns**: 15

| Column Name | Data Type | Units / Format | Description & Scientific Constraints |
|:---|:---:|:---:|:---|
| `timestamp` | string / timestamp | `YYYY-MM-DD HH:MM:SS` | Hourly local timestamp (IST, UTC+5:30) |
| `date` | string / date | `YYYY-MM-DD` | Calendar date |
| `hour` | integer | `0 - 23` | Hour of the day |
| `location_name` | string | Categorical (12 values) | Canonical urban locality name |
| `latitude` | float | Decimal degrees (°N) | Representative centroid latitude (28.35 - 28.51) |
| `longitude` | float | Decimal degrees (°E) | Representative centroid longitude (76.90 - 77.10) |
| `temperature_c` | float | °C | Ambient 2m air temperature (-5.0°C to 55.0°C) |
| `relative_humidity_pct`| float | % | Relative humidity (0% to 100%) |
| `wind_speed_kmh` | float | km/h | 10m horizontal wind speed (>= 0.0) |
| `surface_pressure_hpa`| float | hPa | Surface atmospheric pressure (900.0 to 1050.0 hPa) |
| `cloud_cover_pct` | float | % | Total cloud cover fraction (0% to 100%) |
| `precipitation_mm` | float | mm | Hourly liquid precipitation equivalent (>= 0.0) |
| `weather_condition` | string | Categorical | Weather state (`Clear`, `Haze`, `Rain`, etc.) |
| `aqi` | integer / float | Index units (0 - 500) | Weather-derived AQI estimate (`weather_aqi` in integrated tables) |
| `aqi_category` | string | Categorical (6 CPCB bins)| CPCB AQI band (`Good`, `Satisfactory`, `Moderate`, `Poor`, `Very Poor`, `Severe`) |

---

## 2. Canonical Traffic Dataset (`data/dataset_traffic_gurugram.csv`)
- **Rows**: 315,648 (Hourly records, 2022-01-01 00:00 to 2024-12-31 23:00, 12 localities)
- **Columns**: 18

| Column Name | Data Type | Units / Format | Description & Scientific Constraints |
|:---|:---:|:---:|:---|
| `timestamp` | string / timestamp | `YYYY-MM-DD HH:MM:SS` | Hourly local timestamp (IST) |
| `date` | string / date | `YYYY-MM-DD` | Calendar date |
| `hour` | integer | `0 - 23` | Hour of the day |
| `location_name` | string | Categorical | Canonical locality name |
| `latitude` | float | Decimal degrees | Locality latitude |
| `longitude` | float | Decimal degrees | Locality longitude |
| `road_name` | string | Categorical | Primary monitored corridor name |
| `road_type` | string | Categorical | Functional classification (`arterial`, `highway_arterial`, `junction_arterial`, `urban`, `urban_arterial`) |
| `vehicle_count` | integer | Count (>= 0) | Total observed vehicle count (exact sum of 6 categories below) |
| `two_wheeler_count` | integer | Count (>= 0) | Motorcycles, scooters, mopeds |
| `car_count` | integer | Count (>= 0) | Private cars, taxis, jeeps, SUVs |
| `auto_rickshaw_count`| integer | Count (>= 0) | Three-wheeled intermediate public transport |
| `bus_count` | integer | Count (>= 0) | Standard public transit and private buses |
| `truck_count` | integer | Count (>= 0) | Light and heavy commercial freight vehicles |
| `other_vehicle_count`| integer | Count (>= 0) | Tractors, non-motorized, special utility |
| `total_pcu` | float | Passenger Car Units | Equivalent volume using IRC-67 modal equivalence factors |
| `average_speed_kmh` | float | km/h | Average harmonic corridor travel speed (0 - 120 km/h) |
| `congestion_level` | string | Categorical | Operational congestion level (`Low`, `Medium`, `High`, `Severe`) |

---

## 3. Canonical Air Quality Dataset (`data/dataset_air_quality_gurugram.csv`)
- **Rows**: 315,648 (Hourly records, 2022-01-01 00:00 to 2024-12-31 23:00, 12 localities)
- **Columns**: 14

| Column Name | Data Type | Units / Format | Description & Scientific Constraints |
|:---|:---:|:---:|:---|
| `timestamp` | string / timestamp | `YYYY-MM-DD HH:MM:SS` | Hourly local timestamp (IST) |
| `date` | string / date | `YYYY-MM-DD` | Calendar date |
| `hour` | integer | `0 - 23` | Hour of the day |
| `location_name` | string | Categorical | Canonical locality name |
| `latitude` | float | Decimal degrees | Locality latitude |
| `longitude` | float | Decimal degrees | Locality longitude |
| `pm25_ugm3` | float | µg/m³ | Fine particulate matter (PM2.5 concentration, >= 0.0) |
| `pm10_ugm3` | float | µg/m³ | Coarse particulate matter (PM10 concentration, >= pm25_ugm3) |
| `no2_ugm3` | float | µg/m³ | Nitrogen dioxide concentration (>= 0.0) |
| `so2_ugm3` | float | µg/m³ | Sulfur dioxide concentration (>= 0.0) |
| `co_mg_m3` | float | mg/m³ | Carbon monoxide concentration (>= 0.0, ambient scale) |
| `o3_ugm3` | float | µg/m³ | Tropospheric surface ozone (>= 0.0) |
| `aqi` | integer / float | Index units (0 - 500) | Pollutant-derived AQI (`air_quality_aqi` in integrated tables) |
| `aqi_category` | string | Categorical | CPCB AQI band based on criteria pollutants |

---

## 4. Canonical Geography Dataset (`data/dataset_geography_gurugram.csv`)
- **Rows**: 12 (One representative record per locality)
- **Columns**: 11

| Column Name | Data Type | Description |
|:---|:---:|:---|
| `location_id` | string | Unique node identifier (`LOC_001` to `LOC_012`) |
| `location_name` | string | Canonical locality name |
| `latitude` | float | Representative centroid latitude |
| `longitude` | float | Representative centroid longitude |
| `locality_type` | string | Spatial typology (`Commercial_Core`, `Industrial_Belt`, `Transit_Hub`, etc.) |
| `urban_function` | string | Primary economic/land-use role |
| `representative_corridor`| string | Major connecting traffic corridor |
| `district` | string | Administrative district (`Gurugram`) |
| `state` | string | State (`Haryana`) |
| `country` | string | Country (`India`) |
| `geographic_scope` | string | Regional domain scope (`Gurugram Metropolitan Area`) |

---

## 5. Integrated Master Parquet (`data/processed/integrated/urban_integrated_hourly.parquet`)
- **Rows**: 315,648 (1:1 lossless join on `timestamp` and `location_name`)
- **Key Columns**:
  - `weather_aqi` & `weather_aqi_category`: Explicit provenance from weather benchmark.
  - `air_quality_aqi` & `air_quality_aqi_category`: Explicit provenance from criteria air pollutants.
  - Complete traffic vehicle breakdowns, speeds, congestion levels.
  - Complete meteorological surface variables.
  - Complete geographic typology attributes.
