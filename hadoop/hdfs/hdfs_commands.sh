#!/usr/bin/env bash
# ==============================================================================
# UrbanSphere - HDFS Setup & Upload Commands
# ==============================================================================

echo "Starting UrbanSphere HDFS Setup..."

# Processed authoritative layers
hdfs dfs -mkdir -p /urbansphere/data/processed/mobility
hdfs dfs -mkdir -p /urbansphere/data/processed/weather
hdfs dfs -mkdir -p /urbansphere/data/processed/air_quality
hdfs dfs -mkdir -p /urbansphere/data/processed/geography
hdfs dfs -mkdir -p /urbansphere/data/processed/integrated

# Quarantined synthetic benchmark layer
hdfs dfs -mkdir -p /urbansphere/data/benchmark/synthetic

# Compute engine output layers
hdfs dfs -mkdir -p /urbansphere/output/mapreduce
hdfs dfs -mkdir -p /urbansphere/output/spark

echo "Uploading Datasets..."
hdfs dfs -put data/processed/mobility/* /urbansphere/data/processed/mobility/
hdfs dfs -put data/processed/weather/* /urbansphere/data/processed/weather/
hdfs dfs -put data/processed/air_quality/* /urbansphere/data/processed/air_quality/
hdfs dfs -put data/processed/geography/* /urbansphere/data/processed/geography/
hdfs dfs -put data/processed/integrated/* /urbansphere/data/processed/integrated/
hdfs dfs -put data/benchmark/synthetic/* /urbansphere/data/benchmark/synthetic/

echo "Verifying HDFS Uploads..."
hdfs dfs -ls -R /urbansphere/data/
echo "HDFS Upload Complete."
