#!/usr/bin/env bash
# One-time environment setup for the NOLHC ML Engine (macOS / Linux).
# Builds a virtual environment for each part from its committed lock file.
# Requires Python 3.8.10 available as `python3.8` (or edit PY below).
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3.8}"

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "ERROR: '$PY' not found. Install Python 3.8.10, or run:  PYTHON=/path/to/python3.8 ./SETUP.sh"
  exit 1
fi

echo "Using $("$PY" --version) at $(command -v "$PY")"
echo

for pkg in nolhc_ml experimenting_ml; do
  echo "── $pkg ───────────────────────────────────────────"
  ( cd "$pkg"
    "$PY" -m venv .venv
    ./.venv/bin/pip install --quiet --upgrade pip
    ./.venv/bin/pip install --quiet -r requirements.lock.txt
    echo "  done: $pkg/.venv"
  )
  echo
done

echo "Setup complete."
echo "  Launch the scenario UI:   ./LAUNCH.sh"
echo "  Run the tests:            cd nolhc_ml && ./.venv/bin/python -m pytest -q"
echo "                            cd experimenting_ml && ./.venv/bin/python -m pytest -q"
echo
echo "(archive/brexit_ml is superseded and not set up here — see its own README if you need it.)"
