#!/usr/bin/env bash
# ==============================================================================
# UrbanSphere — Local MapReduce Execution Engine (Canonical Datasets)
# ==============================================================================
# Executes all 4 MapReduce jobs locally using POSIX streaming pipes:
# cat <input> | python3 mapper.py | sort -k1,1 | python3 reducer.py > <output>
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [ -f "${PROJECT_ROOT}/UrbanSphere_env/bin/python3" ]; then
    PYTHON="${PROJECT_ROOT}/UrbanSphere_env/bin/python3"
else
    PYTHON="python3"
fi

OUTPUT_DIR="${PROJECT_ROOT}/output/mapreduce"
mkdir -p "${OUTPUT_DIR}"

echo "============================================================"
echo "UrbanSphere — Local MapReduce Execution (Canonical 2022-2024 Datasets)"
echo "Project Root: ${PROJECT_ROOT}"
echo "Python:       $(${PYTHON} --version)"
echo "Output Dir:   ${OUTPUT_DIR}"
echo "============================================================"

# ------------------------------------------------------------------------------
# Job 1: Traffic Corridor Volume & Capacity Stress Analysis
# ------------------------------------------------------------------------------
echo ""
echo "[Job 1/4] Running Traffic Corridor Aggregation (Canonical 315,648 Hourly Traffic Records)..."
INPUT_J1="${PROJECT_ROOT}/data/dataset_traffic_gurugram.csv"
OUT_J1="${OUTPUT_DIR}/job1_traffic_corridors_canonical.txt"

cat "${INPUT_J1}" | "${PYTHON}" "${SCRIPT_DIR}/job1_traffic_corridors/mapper.py" | sort -k1,1 | "${PYTHON}" "${SCRIPT_DIR}/job1_traffic_corridors/reducer.py" > "${OUT_J1}"
echo "  -> Saved: ${OUT_J1} ($(wc -l < "${OUT_J1}") lines)"

# ------------------------------------------------------------------------------
# Job 2: Vehicle Modal Split & Fleet Distribution
# ------------------------------------------------------------------------------
echo ""
echo "[Job 2/4] Running Vehicle Modal Split & Classification Distribution..."
INPUT_J2="${PROJECT_ROOT}/data/dataset_traffic_gurugram.csv"
OUT_J2="${OUTPUT_DIR}/job2_vehicle_composition_modal_split.txt"

cat "${INPUT_J2}" | "${PYTHON}" "${SCRIPT_DIR}/job2_vehicle_composition/mapper.py" | sort -k1,1 | "${PYTHON}" "${SCRIPT_DIR}/job2_vehicle_composition/reducer.py" > "${OUT_J2}"
echo "  -> Saved: ${OUT_J2} ($(wc -l < "${OUT_J2}") lines)"

# ------------------------------------------------------------------------------
# Job 3: Meteorological Extremes & Diurnal Temperature Range
# ------------------------------------------------------------------------------
echo ""
echo "[Job 3/4] Running Meteorological Extremes & DTR (Canonical 315,648 Weather Records)..."
INPUT_J3="${PROJECT_ROOT}/data/dataset_weather_gurugram_with_aqi.csv"
OUT_J3="${OUTPUT_DIR}/job3_weather_extremes_monthly.txt"

cat "${INPUT_J3}" | "${PYTHON}" "${SCRIPT_DIR}/job3_weather_extremes/mapper.py" | sort -k1,1 | "${PYTHON}" "${SCRIPT_DIR}/job3_weather_extremes/reducer.py" > "${OUT_J3}"
echo "  -> Saved: ${OUT_J3} ($(wc -l < "${OUT_J3}") lines)"

# ------------------------------------------------------------------------------
# Job 4: Multi-Station Air Quality Profiling & NAAQS Threshold Exceedance Indicators
# ------------------------------------------------------------------------------
echo ""
echo "[Job 4/4] Running Air Quality Profiling & NAAQS Exceedance Tracking..."
INPUT_J4="${PROJECT_ROOT}/data/dataset_air_quality_gurugram.csv"
OUT_J4="${OUTPUT_DIR}/job4_air_quality_profiling_seasonal.txt"

cat "${INPUT_J4}" | "${PYTHON}" "${SCRIPT_DIR}/job4_air_quality_profiling/mapper.py" | sort -k1,3 | "${PYTHON}" "${SCRIPT_DIR}/job4_air_quality_profiling/reducer.py" > "${OUT_J4}"
echo "  -> Saved: ${OUT_J4} ($(wc -l < "${OUT_J4}") lines)"

echo ""
echo "============================================================"
echo "All 4 MapReduce jobs executed successfully!"
echo "Outputs stored in: ${OUTPUT_DIR}"
echo "============================================================"
