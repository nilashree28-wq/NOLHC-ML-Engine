"""
Uvicorn entrypoint. Run from this directory:

    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

`src/` is added to sys.path so modules match the spec (e.g. `from ml_engine import MLEngine`).
"""

import sys
from pathlib import Path
from typing import Dict

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from fastapi import FastAPI

app = FastAPI(
    title="Brexit ML Engine",
    version="0.1.0",
    description="Phase 1 scaffold — routes move to ml_api.py in later tasks.",
)


@app.get("/health")
def health() -> Dict[str, str]:
    """Minimal liveness probe until Task 7 wires registry-backed health."""
    return {"status": "ok", "note": "scaffold"}

