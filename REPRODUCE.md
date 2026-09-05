# Reproducing this project

This repository holds the full body of work for the NOLHC ML surrogate of the
post-Brexit AnyLogic border-control simulation, February–September 2026. This
file is the operational entry point: how to stand the project up from a clean
clone, what regenerates deterministically, and what depends on external
services. A prose walkthrough for a new analyst is in
`docs/NOLHC_ML_Engine_Technical_Report.*` (once drafted).

---

## 0. Layout

| Path | What it is | Status |
|---|---|---|
| `nolhc_ml/` | Production-style surrogate engine: per-KPI model registry (`v1`), FastAPI inference API, parameter UI | **Authoritative engine** |
| `experimenting_ml/` | Research pipeline (CV, model selection, stats, SHAP, conformal) + the uncertainty / novelty / self-extension loop + scenario Decision-Intelligence UI | **Authoritative research + reliability layer** |
| `brexit_ml/` | Phase 1 IRE↔GB corridor surrogate, trained on the earlier *Post-Brexit Sector-Based Model* completed-runs export | **Superseded** — kept for context; not part of the reproducible deliverable (see §6) |
| `docs/` | Specs, figures, due-diligence report, paper scaffold | reference |

The uncertainty loop in `experimenting_ml/src/loop/` reads the trained engine
from `nolhc_ml/models/v1/` and the dataset from `nolhc_ml/data/` — this
cross-package dependency is intentional and resolved by path in code.

---

## 1. Prerequisites

* **Python 3.8.10** — one interpreter for all three packages. (Earlier docs said
  `nolhc_ml` needs 3.10+; this is not the case — it installs and tests clean on
  3.8.10.)
* macOS/Linux. On Apple Silicon, `brew install libomp` if XGBoost import fails.
* No database, no cloud account required for anything in §2–§5.
* Pinned dependency sets are committed as `requirements.lock.txt` in each
  package (captured 2026-09-05: scikit-learn 1.3.2, numpy 1.24.4, scipy 1.10.1,
  pandas 2.0.3, xgboost 2.1.4, lightgbm 4.6.0, catboost 1.2.10, shap 0.44.1,
  MAPIE 0.9.2). `requirements.txt` holds the looser human-readable ranges;
  **use the lock file for reproduction.**

```bash
# one package at a time
cd nolhc_ml           # then experimenting_ml, then (optionally) brexit_ml
python3.8 -m venv .venv
./.venv/bin/pip install -r requirements.lock.txt
```

---

## 2. Run the test suites (fastest proof the clone is sound)

```bash
cd nolhc_ml        && ./.venv/bin/python -m pytest -q     #   9 passed
cd experimenting_ml && ./.venv/bin/python -m pytest -q    # 146 passed  (pytest.ini scopes to tests/)
cd brexit_ml       && ./.venv/bin/python -m pytest -q     #  52 passed, 1 skipped
```

Last verified: 2026-09-05, Python 3.8.10, the committed lock files.

---

## 3. `nolhc_ml` — the engine

The trained artifacts **are committed** (`models/v1/`: `registry.json`, 20
per-KPI models + 20 stacking ensembles, `scaler_X.pkl`, benchmarks, residuals;
`data/processed/`: the 129×35 / 129×20 parquet). A fresh clone can serve
predictions immediately — no rebuild needed.

```bash
cd nolhc_ml
# serve the API + parameter UI
./.venv/bin/python -m uvicorn main:app --port 8000
#   http://127.0.0.1:8000/            parameter UI
#   POST /predict   GET /health  /outputs  /inputs

# (optional) regenerate the registry from the source workbook
./.venv/bin/python src/train.py            # data/raw/nolhc_runs.xlsx -> models/v1/
./.venv/bin/python src/evaluate.py
./.venv/bin/python src/evaluate_to_excel.py
```

`train.py` is deterministic (seed 42, 80/20 split 103/26). Re-running it
reproduces the same per-KPI winners and the linear/GP/tree metrics to within
floating point; **XGBoost / LightGBM / CatBoost metrics match only to
library-version tolerance** — pin via the lock file for the closest match.

---

## 4. `experimenting_ml` — research pipeline + uncertainty loop

### 4.1 Ordered benchmarking pipeline (regenerates `outputs/`)

Run from `experimenting_ml/`, in order. Each step consumes the previous step's
JSON/CSV. Full detail: `docs/ML_Pipeline_Specification.md`.

| Step | Command | Produces (gist) |
|---|---|---|
| Cross-validation / hyperparameter tuning | `python run_step1_cv.py` | per-KPI × per-model 5-fold CV, best params → `outputs/cv_results.json`, `cv_best_hyperparameters_long.csv` |
| Ranking + stats | `python run_mentor_step2.py` | paired t-tests, Friedman/Nemenyi, CD diagrams, learning curves, residuals → `outputs/step2/` |
| Selection + calibration | `python run_step3_pre_conformal.py` | composite-score model selection, calibration curves → `outputs/step3/` |
| SHAP | `python run_step4_shap.py` && `python run_step4_shap_master_excel.py` | per-KPI importances, beeswarm/bar/waterfall, `outputs/shap_master.xlsx` |
| Retrain + hold-out eval | `python run_step6_retrain.py` && `python run_test_set_evaluation_final.py` | fitted models, test metrics, split-conformal coverage |
| Master workbook | `python run_step10_report.py` | `outputs/pipeline_results.xlsx` |

`outputs/` is committed, so every result above is readable without re-running.
Re-running requires the `nolhc_ml` models (committed) and the lock-file env.

### 4.2 The uncertainty / self-extension loop

```bash
cd experimenting_ml/src

# synthetic round (fast, no AnyLogic): propose -> trust score -> flag -> "simulate" -> retrain -> recalibrate
python -m loop.cli_export_manual_round --kpi-scope demo4 --n-candidates 20 \
       --quantile 0.9 --max-batch-size 10 --n-replications 5 --seed 42
#   -> data/manual_rounds/round_<ts>/run.csv  + run.xlsx  + manifest entry

# --- MANUAL STEP: enter run.xlsx field-by-field into AnyLogic Cloud,
#     run each request's replications, export results CSV
#     (run_id, replication, seed, <one column per KPI>) ---

python -m loop.cli_ingest_manual_round --round-id round_<ts> --results <results.csv>
#   -> retrains DEMO_4 estimators on 129 + N rows, appends to
#      data/manual_rounds/extended_{X,Y}_train.parquet, flips manifest to "ingested"
```

`--kpi-scope proven6` runs the same loop against the PROVEN_6 benchmarked UQ
methods instead of the generic dispatch. `load_current_training_data()` always
returns 129 + every ingested round.

### 4.3 Scenario Decision-Intelligence UI

```bash
cd experimenting_ml
./.venv/bin/python run_ui_inference_api.py --port 8000
#   http://localhost:8000/UI/index.html
#   POST /api/infer   /api/predict   GET /api/health  /api/meta
#   /api/infer returns prediction + SHAP + conformal interval + coverage
```

The `UI/*.xlsx` files are **config data read by the server** (scenario mapping,
dynamic-parameter tables) — not scratch; leave them in `UI/`.

---

## 5. AnyLogic worksheet artifacts

`experimenting_ml/docs/anylogic/` holds the reference workbooks:

| File | Use |
|---|---|
| `NOLHC Designs - AL Students Recent 26.xlsx` | the 129-run designed experiment (`ExpValues` inputs / `SimResults` KPIs) |
| `Model List of input and output parameters - recent 26.xlsx` | the 35 inputs + 20 KPIs with descriptions and units |
| `AnyLogic_Constants_Worklist.xlsx` | the 89 confirmed-constant AnyLogic fields + the 35 varying ones + the 7 with no AnyLogic field |
| `AnyLogic_Run_Requests_DEMO.csv` / `AnyLogic_Manual_Worklist_DEMO.xlsx` / `NOLHC Designs - AL Students Manual Run.xlsx` | worked examples of a run worksheet |

**To run a real round you build your own worksheet in this shape** — one row per
requested run: the 35 NOLHC parameter values (headed by their AnyLogic field
name) + the 89 constants for reference + `n_replications` + `seed`. The
`cli_export_manual_round` step generates this for you (`run.xlsx`); the
workbooks above are the format reference and the field/constant mapping.

---

## 6. What is NOT reproducible from this repo (by nature)

| Item | Why | What exists instead |
|---|---|---|
| The AnyLogic *Post-Brexit Sector-Based Model* simulation | Proprietary AnyLogic; the `.alp` model file is not in the repo; AnyLogic Cloud API is a paid subscription | The 129-run export (`nolhc_runs.xlsx`) and every manual-round result CSV |
| `brexit_ml` end-to-end | Its exact training workbook is not verified in-repo; superseded by the NOLHC engine | Code + tests run; treat as archival |
| Live LLM narration (`experimenting_ml/src/llm_attribution/`) | Needs an LLM API key; responses are non-deterministic | The schema, personas, and a golden snapshot |
| `UQ_Method_Benchmark.xlsx` coverage numbers | The benchmark-selection script was never committed | The workbook is committed as evidence; the *chosen* per-family UQ methods are enforced and tested in `loop/proven6.py` + `tests/test_proven6.py`; the UQ estimators themselves are fully tested (`tests/test_uq_estimators.py`). See `experimenting_ml/reports/README.md`. |
| Exact XGBoost/LightGBM/CatBoost predictions | Boosting libraries are not bit-stable across builds/versions | Deterministic to library-version tolerance with the lock file |

---

## 7. One-line summary for the report

> All code, tests, and the full modelling methodology reproduce from a clean
> clone on the committed Python 3.8.10 lock files. Trained artifacts are
> committed for immediate use and regenerate deterministically under seed 42
> (boosting models to within library-version tolerance). The AnyLogic
> simulation and live-LLM narration require their external services.
