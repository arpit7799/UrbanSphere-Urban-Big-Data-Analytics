#!/usr/bin/env bash
# ==============================================================================
# UrbanSphere - HDFS Setup & Upload Commands
# ==============================================================================

echo "Starting UrbanSphere HDFS Setup..."

hdfs dfs -mkdir -p /urbansphere/data/processed/mobility
hdfs dfs -mkdir -p /urbansphere/data/processed/weather
hdfs dfs -mkdir -p /urbansphere/data/processed/air_quality
hdfs dfs -mkdir -p /urbansphere/data/processed/geography
hdfs dfs -mkdir -p /urbansphere/data/processed/integrated
hdfs dfs -mkdir -p /urbansphere/output/mapreduce
hdfs dfs -mkdir -p /urbansphere/output/spark

echo "Uploading Datasets..."
hdfs dfs -put data/processed/mobility/* /urbansphere/data/processed/mobility/
hdfs dfs -put data/processed/weather/* /urbansphere/data/processed/weather/
hdfs dfs -put data/processed/air_quality/* /urbansphere/data/processed/air_quality/
hdfs dfs -put data/processed/geography/* /urbansphere/data/processed/geography/
hdfs dfs -put data/processed/integrated/* /urbansphere/data/processed/integrated/

echo "Verifying HDFS Uploads..."
hdfs dfs -ls -R /urbansphere/data/processed/
echo "HDFS Upload Complete."
