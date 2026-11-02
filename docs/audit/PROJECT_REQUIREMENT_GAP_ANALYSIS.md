# UrbanSphere — Project Requirement Gap Analysis

> **Audit Date:** October 2026  
> **Auditor:** Big Data Architect & Academic Project Reviewer  
> **Course / Academic Mapping:** Big Data Analytics — CSE 3712 (B.Tech Computer Science & Engineering)  
> **Evaluation Scope:** 19 Core Functional and Analytical Objectives

---

## 1. Requirement Traceability Matrix

| Requirement | Required Data | Data Actually Available | Data Quality | Temporal Comp. | Geographic Comp. | Feasibility | Gap | Actionable Recommendation |
|:---|:---|:---|:---|:---|:---|:---:|:---|:---|
| **1. Data Acquisition** | 5 domains (Traffic, Weather, AQ, GIS, Events) | 4 domains present; Events completely missing | Mixed (DPR traffic authentic; Weather has UTC shift; AQ authentic; GIS null coords) | Disconnected (2018 vs 2022–2024) | Point / corridor data available; polygons missing | **Partially Feasible** | Events missing (0 records); raw Open-Meteo payloads missing | Drop events from primary scope; archive raw API fetch payloads in data/raw/. |
| **2. Cleaning & Validation** | Automated ETL pipelines for all raw files | Python/Pandas script exists in spark/preprocessing/data_cleaning.py | Script has hardcoded relative path bugs (looks in data/ instead of data/raw/) | N/A | N/A | **Feasible with Fixes** | Script currently fails on execution; uses Pandas not PySpark | Fix filepaths in data_cleaning.py; rewrite transformations using PySpark DataFrames. |
| **3. HDFS Ingestion & Storage** | Distributed filesystem with partitioned directories | Shell scripts and Python subprocess scripts exist | Valid shell commands, but Hadoop/HDFS not installed or running locally | N/A | N/A | **Feasible in Cluster / Docker** | Single-node Mac environment has no running HDFS daemon | Provide Docker Compose for local Hadoop (NameNode, DataNode) or mock HDFS paths. |
| **4. MapReduce Processing** | Java or Python Streaming MapReduce jobs | hadoop/mapreduce/ directory is completely empty (0 files) | N/A | N/A | N/A | **Blocked (Code Missing)** | Zero mappers or reducers written | Implement Python Hadoop Streaming mappers/reducers (e.g. daily weather summary, corridor PCU aggregation). |
| **5. PySpark Transformations** | PySpark DataFrames, cleansing, aggregation | spark/ preprocessing scripts use Pandas/NumPy; ingestion/ is empty | PySpark 4.2.0 installed and functional locally | N/A | N/A | **Fully Feasible** | Existing scripts do not leverage PySpark API | Refactor data_cleaning.py and data_integration.py to native PySpark DataFrame API. |
| **6. Spark SQL Queries** | Spark SQL analytical queries on Parquet | spark/sql/ is empty (.gitkeep only) | Parquet tables exist in data/processed/ | N/A | N/A | **Fully Feasible** | No .sql or Spark SQL scripts written | Create SQL scripts registered on Parquet tables answering core urban analytics questions. |
| **7. Temporal Analysis** | Multi-year time series across domains | Weather: 2022–2024 (hourly); AQ: 2024 daily + 2022–2023 reanalysis | 5.5-hr UTC/IST shift in weather; 215 missing days in 2022 AQ | Synchronous for Weather-AQ 2024 | Single city scale | **Feasible with Fixes** | Timezone offset distorts diurnal curves; traffic has no time series | Correct UTC offset; restrict continuous temporal analysis to 2024 environmental data. |
| **8. Spatial Analysis** | Sector centroids, station coords, GIS polygons | geography_cleaned.csv has 100% NULL coordinates; 4 AQ stations coords present | Cleaned geography coordinates completely nullified | N/A | Coordinates missing in processed geography | **Blocked by Null Data** | Cannot perform spatial joins, distance buffering, or GIS maps | Restore sector coordinates from raw GIS dataset into geography_cleaned.csv. |
| **9. Weather–AQ Analysis** | Simultaneous meteorological & air quality data | 8,784 hourly weather + 1,464 daily station AQ (2024) | High quality for 2024 ground observations | Exact daily temporal overlap | City-level overlap (4 monitoring stations) | **Fully Feasible** | AQ is daily; broadcasting to hours must be documented | Model daily weather vs. daily AQ; evaluate wind speed, humidity, temp vs. PM2.5/AQI. |
| **10. Traffic Analysis** | Traffic volumes, PCUs, compositions, speeds | 15 survey locations, 112 compositions, 8 speed bands from 2018 DPR | Level A authentic municipal engineering tables | Static survey snapshot (2018) | 15 specific corridor & intersection points | **Fully Feasible** | Static cross-section, not continuous time series | Analyze corridor volume/capacity ratios, peak hour factors, vehicle mix, and speed bands. |
| **11. Traffic–Weather Analysis** | Simultaneous traffic and weather observations | 2018 DPR traffic vs. 2024 weather (6-year gap) | High internal quality, but zero temporal overlap | Completely incompatible (2018 vs 2024) | Gurugram city | **Scientifically Infeasible** | Attempting correlation implies false contemporaneous causality | Explicitly document as separate, uncoupled analytical domains. Do not correlate. |
| **12. Event-Related Analysis** | Event dates, locations, crowd sizes, categories | Zero event records anywhere in repository | Completely missing (0 rows) | N/A | N/A | **Blocked (Data Absent)** | Cannot evaluate event impacts on mobility or air quality | Mark Events as Phase 2 future scope; remove false claims from README. |
| **13. Clustering** | Multi-attribute observations with valid features | Air quality stations (pollutants) or weather days (temp/humidity/wind) | Valid 2024 numerical features | Daily / hourly 2024 | 4 stations | **Fully Feasible** | Spatial sector clustering blocked by null coordinates | Implement K-Means / GMM on daily environmental profiles or traffic vehicle compositions. |
| **14. Classification** | Features and valid regulatory target labels | Weather features + CPCB AQI Category (Good to Severe) | Valid CPCB NAQI regulatory category in 2024 AQ data | Synchronous 2024 | Gurugram city | **Fully Feasible** | None for AQI; blocked for traffic/events | Train Random Forest / Decision Tree to classify CPCB AQI Category from weather metrics. |
| **15. Association Rule Mining** | Transactional or discretized condition records | Weather + AQ discretized into categorical condition states | Valid numerical data ready for binning | Synchronous 2024 | Gurugram city | **Fully Feasible** | Requires categorical discretizing | Apply Apriori / FP-Growth on binned urban conditions (e.g., {Low_Wind, Cold, Severe_AQI}). |
| **16. Anomaly Detection** | Continuous time series with baseline distributions | Hourly weather (temp, wind, rain); daily AQ (PM2.5, PM10) | Continuous hourly/daily 2024 sequences | Complete 2024 leap year | Multi-station | **Fully Feasible** | Must account for seasonal baseline shifts | Implement Isolation Forest / Z-score to detect extreme pollution episodes & heatwaves. |
| **17. Backend API (FastAPI)** | REST API serving analytical queries and predictions | backend/app/ directory is completely empty (0 files) | N/A | N/A | N/A | **Blocked (Code Missing)** | Zero API endpoints written | Implement FastAPI service exposing Spark SQL aggregations and ML inference endpoints. |
| **18. Dashboard (Next.js/React)** | Interactive frontend dashboard | frontend/ directory is completely empty (0 files) | N/A | N/A | N/A | **Blocked (Code Missing)** | Zero frontend code written | Build Next.js / TypeScript dashboard with charts (Leaflet/Mapbox, Recharts) consuming API. |
| **19. Performance Benchmarking** | Large-scale datasets for scaling experiments | 40,320 synthetic traffic rows; real datasets total ~12 MB | Real data too small to demonstrate cluster scale | Benchmarks are synthetic | Synthetic | **Feasible with Labeling** | Real data is ~12 MB (fits in RAM in milliseconds) | Formally label 100k+ rows as SYNTHETIC BENCHMARK for Spark/Hadoop scaling tests. |

---

## 2. Summary of Feasibility Status

- **Fully Feasible Right Now (with real data):** 6 requirements
  - PySpark Transformations, Spark SQL Queries, Weather–Air Quality Analytics, Traffic Corridor Analysis, Clustering, Classification, Association Rules, Anomaly Detection.
- **Feasible with Minor Data / Code Corrections:** 4 requirements
  - Data Cleaning Pipeline, Temporal Environmental Analysis, Benchmarking, HDFS Setup.
- **Blocked by Code or Pipeline Absence:** 4 requirements
  - MapReduce Jobs, Backend API (FastAPI), Frontend Dashboard (Next.js), Automated HDFS Execution.
- **Blocked by Data Absence / Data Quality Flaws:** 2 requirements
  - Spatial Analysis (blocked by null coordinates in ).
  - Event Analytics (blocked by 0 event records).
- **Scientifically Infeasible / Prohibited:** 1 requirement
  - Traffic–Weather / Traffic–AQ Cross-Domain Temporal Correlation (6-year temporal gap: 2018 vs. 2024).
