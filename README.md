🌆 CityPulse

Urban Big Data Analytics Platform for Gurugram

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C6FF,50:0072FF,100:7F00FF&height=220&section=header&text=CityPulse&fontSize=70&fontColor=FFFFFF&animation=fadeIn&fontAlignY=35&desc=Urban%20Big%20Data%20Analytics%20for%20Gurugram&descAlignY=58&descSize=20" width="100%"/>
<br>
<br>

Turning heterogeneous urban data into meaningful intelligence.

</div>

⸻

📖 Project Overview

CityPulse is a Gurugram-focused Urban Big Data Analytics Platform designed to integrate and analyze heterogeneous urban datasets from multiple domains.

Instead of analyzing mobility, weather, air quality, events, and geography independently, CityPulse brings these datasets together into a common analytical framework.

The objective is to discover:

* 🕐 Temporal patterns
* 📍 Spatial patterns
* 🔗 Cross-domain relationships
* 🚨 Urban anomalies
* 🧩 Similar geographical behavior
* 📈 Statistical trends
* 🔎 Frequently occurring combinations of urban conditions

The project demonstrates how Hadoop, HDFS, MapReduce, PySpark, and Spark SQL can be combined with modern analytics and visualization technologies to solve a real-world urban data problem.

⸻

💡 Core Idea

<div align="center">
┌───────────────────────────────────────────────────────────────┐
│                       RAW URBAN DATA                          │
│                                                               │
│  🚗 Mobility   🌦️ Weather   🌫️ Air Quality   🎫 Events   🗺️ GIS │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                     BIG DATA PIPELINE                         │
│                                                               │
│        HDFS → MapReduce → PySpark → Spark SQL                 │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                    URBAN ANALYTICS                            │
│                                                               │
│  📊 Statistics  │  🧩 Clustering  │  🎯 Classification        │
│  🚨 Anomalies   │  🔗 Associations │  📈 Trend Analysis      │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                  CITYPULSE INTELLIGENCE                       │
│                                                               │
│              Interactive Urban Analytics Dashboard            │
└───────────────────────────────────────────────────────────────┘
</div>

⸻

🎯 Problem Statement

Modern cities generate massive amounts of heterogeneous data from transportation systems, environmental sensors, weather services, public events, and geographic information systems.

However, these datasets are usually:

* Stored in different formats
* Generated at different frequencies
* Associated with different geographic references
* Maintained by different systems
* Difficult to analyze together

This creates a major challenge:

How can heterogeneous urban datasets be integrated and processed at scale to discover meaningful temporal and spatial relationships within a city?

CityPulse addresses this challenge using a distributed Big Data processing pipeline focused on Gurugram.

⸻

🧠 Research Question

<div align="center">

🔬 Central Research Question

How can heterogeneous mobility, environmental, weather, event, and geographical data be processed at scale to discover meaningful temporal and spatial relationships in Gurugram’s urban environment?

</div>

Supporting Questions

Question	Analytical Goal
🌦️ How does weather relate to mobility?	Correlation & temporal analysis
🌫️ Are mobility patterns associated with air quality?	Cross-domain analysis
🎫 Do public events coincide with unusual mobility?	Event-context analysis
📍 Which areas show similar urban behavior?	Clustering
🚨 What constitutes unusual urban activity?	Anomaly detection
🔗 Which urban conditions frequently occur together?	Association rules
⚡ How effectively can distributed technologies process integrated data?	Performance benchmarking

⸻

🏙️ Why Gurugram?

Gurugram provides an interesting environment for urban analytics because of its:

* 🚗 High mobility activity
* 🏢 Dense commercial zones
* 🛣️ Major transportation corridors
* 🌫️ Significant environmental variation
* 🌦️ Seasonal weather changes
* 🎫 Frequent public and commercial events
* 📍 Diverse geographical areas

This makes Gurugram an appropriate case study for investigating interactions between mobility, environment, weather, events, and geography.

⸻

📦 Data Domains

CityPulse integrates multiple categories of urban data.

<div align="center">

Domain	Example Variables	Purpose
🚗 Mobility	Traffic, movement, timestamps, locations	Analyze urban movement
🌦️ Weather	Temperature, humidity, rainfall, wind	Environmental context
🌫️ Air Quality	PM2.5, PM10, NO₂, O₃, CO	Pollution analysis
🎫 Events	Type, location, date/time	Contextual information
🗺️ Geography	Coordinates, wards, zones	Spatial analysis

</div>

⸻

🔄 Data Integration Strategy

The core challenge is not simply collecting datasets.

The real challenge is making heterogeneous datasets analytically compatible.

CityPulse performs:

Different Sources
       │
       ▼
Schema Standardization
       │
       ▼
Timestamp Normalization
       │
       ▼
Geographic Normalization
       │
       ▼
Missing Value Handling
       │
       ▼
Duplicate Removal
       │
       ▼
Data Quality Validation
       │
       ▼
Temporal / Spatial Join
       │
       ▼
Integrated Urban Dataset

A potential analytical representation is:

timestamp
area_id
mobility_value
temperature
humidity
rainfall
wind_speed
pm25
pm10
event_indicator
event_type

The exact schema will depend on the final datasets selected during implementation.

⸻

🏗️ System Architecture

                         CITYPULSE
                            │
                            ▼
                 ┌─────────────────────┐
                 │  DATA ACQUISITION   │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      Mobility           Weather         Air Quality
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                    Events + Geography
                            │
                            ▼
                 ┌─────────────────────┐
                 │       HDFS          │
                 │ Distributed Storage │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     MapReduce       │
                 │ Distributed Jobs    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      PySpark        │
                 │ Processing & ETL    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Spark SQL       │
                 │ Query & Aggregation │
                 └──────────┬──────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │      ANALYTICS ENGINE      │
              ├────────────────────────────┤
              │ 📊 Statistics              │
              │ 🧩 Clustering              │
              │ 🎯 Classification          │
              │ 🔗 Association Rules       │
              │ 🚨 Anomaly Detection       │
              └──────────────┬─────────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │     FastAPI       │
                   │ Analytics Backend │
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │ Next.js + React   │
                   │ Interactive UI    │
                   └─────────┬─────────┘
                             │
                             ▼
                   🌆 CITYPULSE DASHBOARD

⸻

⚙️ How CityPulse Works

1️⃣ Data Acquisition

Data is collected from multiple heterogeneous sources.

Mobility ─────┐
Weather ──────┤
Air Quality ──┼──► CityPulse Data Layer
Events ───────┤
Geography ────┘

Each dataset is inspected for:

* Format
* Schema
* Size
* Timestamp resolution
* Geographic coverage
* Missing values
* Duplicate records
* Data quality
* Licensing / usage constraints

⸻

2️⃣ Distributed Storage — HDFS

Raw and processed datasets are organized inside Hadoop Distributed File System (HDFS).

Example:

/citypulse/
│
├── raw/
│   ├── mobility/
│   ├── weather/
│   ├── air_quality/
│   ├── events/
│   └── geography/
│
├── processed/
│   ├── mobility/
│   ├── weather/
│   ├── air_quality/
│   └── integrated/
│
└── output/
    ├── mapreduce/
    ├── analytics/
    └── reports/

HDFS demonstrates distributed storage concepts such as:

* Block-based storage
* Replication
* Fault tolerance
* Distributed access
* Large-scale file handling

⸻

🗺️ Geographic Integration

Geography is critical because urban behavior changes from one area to another.

CityPulse can transform raw coordinates into common geographic units such as:

Latitude + Longitude
          │
          ▼
Spatial Mapping
          │
          ▼
Gurugram Ward / Area
          │
          ▼
area_id

This enables questions such as:

Which areas show similar mobility and environmental behavior?

and:

Which areas experience unusual urban conditions?

⸻

⏱️ Temporal Integration

Datasets may use different time resolutions.

For example:

Mobility       → minute-level
Weather        → hourly
Air Quality    → hourly
Events         → event-based
Geography      → static

CityPulse therefore performs temporal normalization where appropriate.

Example:

10:00 ─┐
10:15 ─┤
10:30 ─┤──► 10:00–11:00 analytical window
10:45 ─┤
11:00 ─┘

This allows different domains to be analyzed together.

⸻

⚡ Big Data Processing Layer

Hadoop + HDFS

Used for:

* Distributed storage
* Dataset organization
* Large-file handling
* Hadoop ecosystem demonstration

MapReduce

Used to demonstrate distributed computation through:

* Mapper
* Shuffle
* Reducer
* Aggregation
* Distributed output

Example conceptual job:

Raw Mobility Data
       │
       ▼
     Mapper
       │
       ▼
(area_id, mobility_value)
       │
       ▼
    Shuffle
       │
       ▼
     Reducer
       │
       ▼
Area-level aggregation

⸻

🔥 PySpark Processing

PySpark forms the primary distributed data-processing layer.

Planned processing includes:

Raw Data
   ↓
DataFrame Creation
   ↓
Schema Validation
   ↓
Missing Value Handling
   ↓
Duplicate Removal
   ↓
Timestamp Processing
   ↓
Outlier Handling
   ↓
Feature Engineering
   ↓
Dataset Integration
   ↓
Parquet Storage

PySpark enables the project to demonstrate:

* Distributed DataFrames
* Transformations
* Actions
* Aggregations
* Joins
* Window operations
* Partitioning
* Caching
* Distributed computation

⸻

🧮 Spark SQL

Spark SQL enables analytical querying over the integrated dataset.

Example conceptual query:

SELECT
    area_id,
    AVG(mobility_value) AS avg_mobility,
    AVG(pm25) AS avg_pm25,
    AVG(temperature) AS avg_temperature
FROM integrated_urban_data
GROUP BY area_id;

This allows CityPulse to perform:

* Area-level aggregation
* Time-based analysis
* Cross-domain comparisons
* Filtering
* Grouping
* Statistical summaries

⸻

📊 Analytics Engine

CityPulse is not designed as a single machine-learning model.

Instead, it combines multiple analytical techniques.

<div align="center">
                 Integrated Dataset
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     Statistics       Data Mining      ML Analytics
          │              │              │
          │        ┌─────┴─────┐    ┌───┴────┐
          │        ▼           ▼    ▼        ▼
          │   Association   Clustering   Classification
          │      Rules
          │
          └──────────────┬──────────────┘
                         │
                         ▼
                 Anomaly Detection
                         │
                         ▼
                  Urban Insights
</div>

⸻

🧩 1. Clustering

Clustering groups geographically or behaviorally similar areas.

Potential objective:

Identify areas with similar mobility + environmental characteristics.

Example conceptual output:

Cluster 1 → High mobility / moderate pollution
Cluster 2 → Low mobility / low pollution
Cluster 3 → High mobility / high pollution
Cluster 4 → Event-sensitive areas

The exact clusters will be determined from the actual data.

⸻

🎯 2. Classification

Classification can be used to categorize urban conditions based on engineered features.

For example:

Urban Condition
      │
      ├── Normal
      ├── High Activity
      ├── High Pollution
      └── Unusual Condition

Classification is an analytical component rather than the sole purpose of CityPulse.

⸻

🚨 3. Anomaly Detection

Anomaly detection identifies observations that significantly deviate from expected patterns.

Example:

Normal Mobility
      │
      │  ▂▃▅▆▅▃▂
      │
      │
      │                 🚨
      │                 █
      │                 █
      └──────────────────────────► Time

Possible use cases:

* Unusual traffic activity
* Abnormal pollution levels
* Unexpected area behavior
* Event-associated deviations

⸻

🔗 4. Association Rule Mining

Association rules identify frequently occurring combinations of conditions.

Example:

High Mobility
      +
Low Wind
      +
High PM2.5
      ↓
Frequently Associated Condition

The purpose is to discover relationships, not necessarily causal relationships.

⸻

📐 Statistical Analysis

CityPulse will use descriptive and exploratory statistics to understand the integrated dataset.

Potential analysis includes:

* Mean
* Median
* Standard deviation
* Variance
* Percentiles
* Correlation
* Distribution analysis
* Time-series summaries
* Area-level comparisons

Example relationship analysis:

Weather ─────────► Mobility
   │
   ├──────────────► Air Quality
   │
   ▼
Environmental Context

⸻

🔍 Exploratory Data Analysis

EDA will examine:

Temporal Patterns

* Hourly behavior
* Daily patterns
* Weekday vs weekend
* Seasonal variation

Spatial Patterns

* Area-level mobility
* Pollution distribution
* Clustered urban behavior

Cross-Domain Patterns

Weather ↔ Mobility
Weather ↔ Air Quality
Events  ↔ Mobility
Mobility ↔ Air Quality

⸻

🖥️ Interactive Dashboard

The final application will provide a web-based interface for exploring the analytical results.

Planned Dashboard Components

Component	Purpose
📊 KPI Cards	High-level urban statistics
📈 Time-Series Charts	Temporal trends
🗺️ Interactive Map	Geographic analysis
🧩 Cluster View	Area segmentation
🚨 Anomaly View	Unusual conditions
🔗 Association View	Frequent combinations
🌦️ Weather Panel	Environmental context
🌫️ Air Quality Panel	Pollution analysis
🚗 Mobility Panel	Transportation patterns
🎫 Event Context	Event-based comparison

⸻

🎨 Planned User Experience

┌────────────────────────────────────────────────────────────┐
│                     🌆 CITYPULSE                           │
│               Gurugram Urban Intelligence                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  🚗 Mobility     🌦️ Weather     🌫️ Air Quality     🎫 Events │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│              🗺️ INTERACTIVE GURUGRAM MAP                  │
│                                                            │
├─────────────────────────────┬──────────────────────────────┤
│ 📈 Temporal Trends           │ 🚨 Anomalies                 │
│                             │                              │
├─────────────────────────────┼──────────────────────────────┤
│ 🧩 Area Clusters             │ 🔗 Associations              │
│                             │                              │
└─────────────────────────────┴──────────────────────────────┘

⸻

🛠️ Technology Stack

<div align="center">

Layer	Technologies
🐍 Programming	Python
🗄️ Distributed Storage	Hadoop HDFS
⚙️ Distributed Processing	Apache Hadoop / MapReduce
🔥 Big Data Processing	Apache Spark / PySpark
🧮 Query Engine	Spark SQL
📊 Analytics	Python / PySpark / ML techniques
🚀 Backend	FastAPI
⚛️ Frontend	Next.js / React
🔷 Language	TypeScript
📈 Visualization	Web-based interactive charts/maps
🔧 Version Control	Git / GitHub

</div>

⸻

🧱 Project Structure

CityPulse/
│
├── data/
│   ├── raw/
│   │   ├── mobility/
│   │   ├── weather/
│   │   ├── air_quality/
│   │   ├── events/
│   │   └── geography/
│   │
│   ├── processed/
│   └── sample/
│
├── hadoop/
│   ├── hdfs/
│   └── mapreduce/
│
├── spark/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── integration/
│   └── sql/
│
├── analytics/
│   ├── eda/
│   ├── statistics/
│   ├── clustering/
│   ├── classification/
│   ├── association/
│   └── anomaly_detection/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── services/
│       ├── schemas/
│       └── main.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   └── public/
│
├── notebooks/
│
├── tests/
│
├── docs/
│
├── requirements.txt
├── README.md
└── LICENSE

The exact structure may evolve as implementation progresses.

⸻

📈 Big Data Justification

CityPulse is designed around the principles of Big Data Analytics rather than simply applying machine learning to a small CSV file.

1️⃣ Volume

Historical and high-frequency datasets can produce large numbers of observations.

2️⃣ Variety

The project integrates:

CSV
JSON
API responses
Geospatial data
Time-series data
Structured datasets

3️⃣ Velocity

Some urban datasets can be generated at high temporal frequencies.

4️⃣ Veracity

Datasets may contain:

* Missing values
* Duplicate records
* Inconsistent timestamps
* Different geographic references
* Sensor anomalies

5️⃣ Value

The objective is to transform raw heterogeneous data into meaningful urban insights.

⸻

⚡ Scalability & Performance

A major objective is to demonstrate why distributed technologies are useful.

CityPulse will evaluate performance through metrics such as:

Dataset Size
     │
     ▼
┌───────────────────┐
│ Processing Method │
├───────────────────┤
│ Local Processing  │
│       vs          │
│ Spark Processing  │
└─────────┬─────────┘
          │
          ▼
Execution Time
Memory Usage
Throughput
Scalability

Where practical, benchmark datasets may be expanded for controlled performance testing.

Generated benchmark data will be clearly identified and will not be presented as real-world observations.

⸻

🧪 Testing & Validation

CityPulse will include testing across multiple layers.

🗄️ Data Layer

* Schema validation
* Missing-value checks
* Duplicate detection
* Timestamp validation
* Geographic validation

⚙️ Processing Layer

* HDFS verification
* MapReduce output validation
* Spark transformation tests
* Spark SQL query validation

🧠 Analytics Layer

* Model validation
* Statistical sanity checks
* Cluster evaluation
* Anomaly verification
* Association-rule validation

🌐 Application Layer

* API testing
* Frontend testing
* Integration testing
* End-to-end workflow testing

⸻

🔐 Data & Research Integrity

CityPulse follows a data-first and reproducible approach.

The project aims to:

* Document data sources
* Record dataset schemas
* Preserve preprocessing logic
* Separate raw and processed data
* Clearly distinguish real and generated data
* Avoid unsupported causal claims
* Document analytical assumptions
* Validate results before presenting them

Most importantly:

Correlation discovered by CityPulse will not automatically be interpreted as causation.

⸻

🗺️ Development Roadmap

<div align="center">

🚀 CityPulse Development Journey

PHASE 01  ████████████████████  Foundation
    ↓
PHASE 02  ████████████████████  Data Acquisition
    ↓
PHASE 03  ████████████████████  Hadoop + HDFS
    ↓
PHASE 04  ████████████████████  PySpark Integration
    ↓
PHASE 05  ████████████████████  EDA + Statistics
    ↓
PHASE 06  ████████████████████  Advanced Analytics
    ↓
PHASE 07  ████████████████████  Backend API
    ↓
PHASE 08  ████████████████████  Dashboard
    ↓
PHASE 09  ████████████████████  Testing + Optimization
    ↓
PHASE 10  ████████████████████  Final Demo + Documentation
</div>

⸻

📅 Project Timeline

Phase	Major Activities
01	Problem definition, objectives, research, datasets, architecture
02	Data acquisition, inspection, schema, initial exploration
03	Hadoop, HDFS and MapReduce
04	PySpark preprocessing and integration
05	EDA and statistical analysis
06	Clustering, classification, association rules, anomaly detection
07	Spark SQL, optimization and scalability
08	FastAPI backend + interactive dashboard
09	Testing, debugging and validation
10	Final report, presentation, demonstration and submission

⸻

🎓 Academic Alignment

CityPulse directly supports the learning objectives of Big Data Analytics — CSE 3712.

Course Requirement	CityPulse Implementation
Heterogeneous data acquisition	Multiple urban data domains
Hadoop	Distributed ecosystem
HDFS	Distributed storage
MapReduce	Distributed computation
PySpark	Large-scale processing
Spark SQL	Analytical querying
Statistics	Urban statistical analysis
Visualization	Interactive dashboard
Classification	Urban condition analytics
Clustering	Geographic/behavioral grouping
Association Rules	Frequent condition discovery
Industry Application	Real-world urban analytics

⸻

🌟 What Makes CityPulse Different?

❌ Not just a dashboard

CityPulse focuses on the analytical pipeline behind the visualization.

❌ Not just a machine-learning model

Multiple analytical approaches are combined.

❌ Not just one dataset

The project integrates heterogeneous urban domains.

❌ Not just prediction

The primary goal is discovering relationships, patterns, anomalies, and urban behavior.

✅ It is an end-to-end Big Data system

DATA
 ↓
STORAGE
 ↓
DISTRIBUTED PROCESSING
 ↓
INTEGRATION
 ↓
STATISTICS
 ↓
DATA MINING
 ↓
MACHINE LEARNING
 ↓
API
 ↓
VISUALIZATION
 ↓
URBAN INSIGHTS

⸻

🔮 Future Scope

Future versions could extend CityPulse with:

* 📡 Real-time streaming
* 🔄 Apache Kafka integration
* 🧠 More advanced ML models
* 🌐 Larger geographic coverage
* 🛰️ Satellite / remote-sensing data
* 📱 Mobile interface
* 🏙️ Multi-city comparison
* 🤖 AI-assisted urban insights
* 📊 Real-time monitoring
* 🔔 Intelligent anomaly alerts

These are future possibilities and are not considered implemented unless explicitly added to the project.

⸻

📚 Learning Outcomes

Through CityPulse, the project aims to develop practical expertise in:

Python
   ↓
Data Engineering
   ↓
Hadoop
   ↓
HDFS
   ↓
MapReduce
   ↓
PySpark
   ↓
Spark SQL
   ↓
Statistics
   ↓
Machine Learning
   ↓
Data Mining
   ↓
FastAPI
   ↓
Next.js
   ↓
End-to-End System Engineering

⸻

📊 Project Status

<div align="center">

🟡 Active Development

CityPulse is currently under active development.

</div>

Current work is focused on building the complete data pipeline and progressively integrating:

Data Sources
     ↓
Hadoop / HDFS
     ↓
MapReduce
     ↓
PySpark
     ↓
Analytics
     ↓
FastAPI
     ↓
Next.js Dashboard

Features will be marked as completed only after they have been implemented and validated.

⸻

🧭 Project Vision

<div align="center">

🌆 From Urban Data to Urban Intelligence

CityPulse aims to demonstrate how distributed Big Data technologies can transform fragmented urban datasets into a unified analytical system capable of revealing meaningful patterns within a city’s environment.

<br>

Collect → Store → Process → Integrate → Analyze → Visualize → Understand

</div>

⸻

👨‍💻 Author

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=soft&color=0:0072FF,100:7F00FF&height=100&section=footer&text=Arpit%20Pandey&fontSize=35&fontColor=FFFFFF&animation=fadeIn" width="100%"/>

Arpit Pandey

B.Tech Computer Science & Engineering
BML Munjal University

Course: Big Data Analytics — CSE 3712
Academic Year: 2026–27

<br>
</div>

⸻

<div align="center">

⭐ CityPulse

Urban data is everywhere.

The challenge is turning it into understanding.

<br>
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7F00FF,50:0072FF,100:00C6FF&height=120&section=footer" width="100%"/>
</div>
