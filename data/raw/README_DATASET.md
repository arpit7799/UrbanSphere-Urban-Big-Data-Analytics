# UrbanSphere — Gurugram DPR-Derived Dataset v1

## Purpose
This package converts verified tables from the **Revised Final DPR – Metro Rail Connection from HUDA City Centre to Cyber City, Gurugram** into structured, analysis-ready CSV and Excel datasets for the CityPulse Big Data Analytics project.

## Source
- Document: `RevisedFINALDPR_GurgaonMetro_Oct19.pdf`
- Primary traffic survey: RITES Primary Surveys, 2018
- DPR: 2019
- Geographic scope: Gurugram / Gurugram-Manesar Urban Complex
- Key printed pages: 2-5, 2-6, 2-14, 3-4, 3-5, 3-6, 3-7

## Included datasets
1. `midblock_traffic.csv` — 8 Gurugram mid-block/screen-line locations.
2. `midblock_vehicle_composition_derived.csv` — composition percentages plus analytically reconstructed vehicle counts.
3. `intersection_traffic.csv` — 4 intersections with 16-hour daily traffic totals.
4. `intersection_vehicle_composition.csv` — intersection traffic composition percentages.
5. `outer_cordon_traffic.csv` — 3 outer-cordon locations.
6. `road_speed_distribution.csv` — peak journey/running speed distribution across 567.3 km of road network.
7. `air_quality_context.csv` — Jan–Sep 2019 monthly air-quality context reported in the DPR.
8. `citypulse_gurugram_master_long.csv` — normalized long-format analytical dataset.
9. `data_dictionary.csv` — field-level documentation.
10. `provenance.csv` — source and limitations.

## Important integrity rule
Do **not** describe the derived composition-count rows as raw observations. They are mathematical reconstructions from reported total traffic and percentage composition.

Do **not** claim this package is a continuous real-time traffic dataset. The DPR contains survey aggregates and specific traffic-count surveys. The intersection survey itself used 15-minute direction-wise counts continuously from 06:00 to 22:00 on a typical working day, but the detailed interval records are not reproduced in these tables.

## Recommended CityPulse use
- Hadoop/HDFS: store the raw CSVs under `data/raw/mobility/`.
- PySpark: clean, standardize and integrate the datasets.
- Spark SQL: aggregate by location/type/metric.
- Analytics: compare mid-block, intersection and outer-cordon traffic; analyze speed distributions; join the environmental context later.
- Future integration: add independent weather, events and geospatial datasets using documented temporal/spatial keys.

## Dataset status
**v1 — source-grounded and reproducible.**

## Synthetic benchmark dataset
`synthetic_spark_benchmark_100k.csv` contains 100,000 generated records for **Hadoop/Spark performance testing only**.

It is intentionally separated from source-grounded observations. The generated rows use source-derived location traffic magnitudes and PCU ratios as a basis, but the timestamps and individual traffic observations are synthetic.

Never use this file as evidence that a specific traffic volume occurred at a specific time.
