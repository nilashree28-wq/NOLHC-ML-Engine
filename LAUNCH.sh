#!/usr/bin/env bash
# Start the NOLHC ML Engine's primary interface: the scenario
# Decision-Intelligence UI (predictions + uncertainty + SHAP + operator
# console). macOS / Linux. Run ./SETUP.sh first if you haven't.
set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-8000}"
VENV="experimenting_ml/.venv/bin/python"

if [ ! -x "$VENV" ]; then
  echo "ERROR: $VENV not found. Run ./SETUP.sh first."
  exit 1
fi

echo "Scenario UI:        http://localhost:${PORT}/UI/index.html"
echo "Settings / operator: http://localhost:${PORT}/UI/settings.html"
echo "(Ctrl-C to stop.)"
echo

cd experimenting_ml
exec ./.venv/bin/python run_ui_inference_api.py --port "${PORT}"
