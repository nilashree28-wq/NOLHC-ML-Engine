# Brexit ML Engine (Phase 1)

Surrogate ML service for the IRE ↔ GB East/West corridor per `docs/ml/spec/brexit_ml_engine_spec.md`.

## Prerequisites

- Python 3.10+ (spec). If your default `python3` is older, create the venv with a newer interpreter, e.g. `python3.12 -m venv .venv`.
- Source workbook: copy `Post-Brexit_Sector_Based_Model_-_PostBrexit_latest_model_-_Completed_runs__2_.xlsx` to `data/raw/completed_runs.xlsx` (see spec).

## Setup

From this directory (`brexit_ml/`):

```bash
python3.10 -m venv .venv   # or python3.11 / python3.12
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optional: `export PYTHONPATH=src` is not required when using `main.py` (it prepends `src/`) or when running pytest (see `pyproject.toml`).

## Data loading (Task 3)

With `data/raw/completed_runs.xlsx` in place:

```bash
python -c "from data_loader import load_xlsx, save_processed_parquet; from pathlib import Path; \
  X,Y = load_xlsx('data/raw/completed_runs.xlsx'); \
  save_processed_parquet(X, Y, Path('data/processed'))"
```

Or import `prepare_training_frames` for tests. Column names are defined in `src/training_columns.py` (generated from `docs/ml/spec/brexit_ml_engine_spec.md`).

## Train (after Task 5 exists)

```bash
python src/train.py
```

## Run API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Check: `GET http://localhost:8000/health`

## Tests

From `brexit_ml/`:

```bash
pytest tests -v
```

## Layout

- `src/` — Python modules (`data_loader`, `train`, `ml_engine`, APIs, …)
- `data/raw/` — input xlsx (not committed)
- `data/processed/` — parquet features/targets
- `models/v1/` — scaler, per-output models, `registry.json` (not committed)
