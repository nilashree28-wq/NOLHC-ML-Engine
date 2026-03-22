"""
Uvicorn entrypoint. Run from this directory:

    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

``src/`` is on ``sys.path`` so imports match the spec (``ml_api``, ``ml_engine``, …).
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from ml_api import app  # noqa: E402
