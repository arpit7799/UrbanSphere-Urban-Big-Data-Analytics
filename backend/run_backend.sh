#!/usr/bin/env bash
# UrbanSphere — Start FastAPI Analytics Server
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

PORT=${1:-8000}
HOST=${2:-"0.0.0.0"}

echo "============================================================"
echo "Starting UrbanSphere FastAPI Analytics Server"
echo "URL: http://$HOST:$PORT"
echo "Interactive Swagger Docs: http://$HOST:$PORT/docs"
echo "ReDoc Documentation:     http://$HOST:$PORT/redoc"
echo "============================================================"

exec "$PROJECT_ROOT/UrbanSphere_env/bin/uvicorn" backend.app.main:app --host "$HOST" --port "$PORT" --reload
