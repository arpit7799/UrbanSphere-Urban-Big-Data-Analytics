#!/usr/bin/env bash
# ==============================================================================
# UrbanSphere — Hadoop Streaming Cluster Execution Runner
# ==============================================================================
# Submits all 4 MapReduce jobs to an active Apache Hadoop YARN cluster
# using Hadoop Streaming JAR against HDFS paths.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo "============================================================"
echo "UrbanSphere — Hadoop Streaming Cluster Runner"
echo "============================================================"

# Check if Hadoop CLI is available
if ! command -v hadoop &> /dev/null; then
    echo "ERROR: 'hadoop' command not found in PATH."
    echo ""
    echo "This script is designed to execute against a live Apache Hadoop cluster."
    echo "To test MapReduce locally without Hadoop, use the local streaming runner:"
    echo "    bash hadoop/mapreduce/run_mapreduce_local.sh"
    echo ""
    echo "Cluster prerequisites:"
    echo "1. Hadoop 3.x cluster running (HDFS + YARN)"
    echo "2. Datasets uploaded to HDFS via: bash hadoop/hdfs/hdfs_commands.sh"
    echo "3. HADOOP_HOME and JAVA_HOME exported in environment"
    exit 1
fi

# Locate Hadoop Streaming JAR
HADOOP_STREAMING_JAR=$(find "${HADOOP_HOME}/share/hadoop/tools/lib" -name "hadoop-streaming*.jar" 2>/dev/null | head -n 1)

if [ -z "${HADOOP_STREAMING_JAR}" ]; then
    echo "ERROR: hadoop-streaming*.jar could not be located in ${HADOOP_HOME}."
    exit 1
fi

echo "Found Hadoop Streaming JAR: ${HADOOP_STREAMING_JAR}"

# HDFS base paths
HDFS_DATA="/urbansphere/data/processed"
HDFS_OUTPUT="/urbansphere/output/mapreduce"

# Remove existing output directories in HDFS if re-running
hdfs dfs -rm -r -f "${HDFS_OUTPUT}" 2>/dev/null || true
hdfs dfs -mkdir -p "${HDFS_OUTPUT}"

# ------------------------------------------------------------------------------
# Job 1: Traffic Corridors
# ------------------------------------------------------------------------------
echo ""
echo "[Cluster Job 1/4] Submitting Traffic Corridor Aggregation..."
hadoop jar "${HADOOP_STREAMING_JAR}" \
    -D mapreduce.job.name="UrbanSphere_Traffic_Corridors" \
    -files "${SCRIPT_DIR}/job1_traffic_corridors/mapper.py,${SCRIPT_DIR}/job1_traffic_corridors/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "${HDFS_DATA}/mobility/traffic_cleaned.csv" \
    -output "${HDFS_OUTPUT}/job1_traffic_corridors"

# ------------------------------------------------------------------------------
# Job 2: Vehicle Composition
# ------------------------------------------------------------------------------
echo ""
echo "[Cluster Job 2/4] Submitting Vehicle Modal Split..."
hadoop jar "${HADOOP_STREAMING_JAR}" \
    -D mapreduce.job.name="UrbanSphere_Vehicle_Composition" \
    -files "${SCRIPT_DIR}/job2_vehicle_composition/mapper.py,${SCRIPT_DIR}/job2_vehicle_composition/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "${HDFS_DATA}/mobility/vehicle_composition_cleaned.csv" \
    -output "${HDFS_OUTPUT}/job2_vehicle_composition"

# ------------------------------------------------------------------------------
# Job 3: Weather Extremes
# ------------------------------------------------------------------------------
echo ""
echo "[Cluster Job 3/4] Submitting Weather Extremes & DTR..."
hadoop jar "${HADOOP_STREAMING_JAR}" \
    -D mapreduce.job.name="UrbanSphere_Weather_Extremes" \
    -files "${SCRIPT_DIR}/job3_weather_extremes/mapper.py,${SCRIPT_DIR}/job3_weather_extremes/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "${HDFS_DATA}/weather/weather_cleaned.csv" \
    -output "${HDFS_OUTPUT}/job3_weather_extremes"

# ------------------------------------------------------------------------------
# Job 4: Air Quality Profiling & Exceedance Tracking
# ------------------------------------------------------------------------------
echo ""
echo "[Cluster Job 4/4] Submitting Air Quality Profiling..."
hadoop jar "${HADOOP_STREAMING_JAR}" \
    -D mapreduce.job.name="UrbanSphere_Air_Quality_Profiling" \
    -files "${SCRIPT_DIR}/job4_air_quality_profiling/mapper.py,${SCRIPT_DIR}/job4_air_quality_profiling/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "${HDFS_DATA}/air_quality/air_quality_cleaned.csv" \
    -output "${HDFS_OUTPUT}/job4_air_quality_profiling"

echo ""
echo "============================================================"
echo "Hadoop Cluster Jobs Finished!"
echo "Check outputs via: hdfs dfs -ls -R ${HDFS_OUTPUT}"
echo "============================================================"
