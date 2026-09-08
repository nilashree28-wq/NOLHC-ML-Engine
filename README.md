# NOLHC ML Engine

A fast machine-learning surrogate for the AnyLogic post-Brexit Ireland–GB–EU
RoRo agri-food border-control simulation. From **35 inputs** it predicts
**20 operational KPIs** (transit times, waiting times, staff utilisations) in
milliseconds, in a browser, with SHAP explanations and an explicit trust
signal that tells you when to fall back to the real simulation.

This is **one system in two parts**:

| Folder | What it is | You touch it when… |
|---|---|---|
| **`nolhc_ml/`** — the engine | The frozen, versioned model. Trained per-KPI on the designed experiment; holds `models/v1/` (registry + 20 models + 20 stacking ensembles), the prediction API, and a simple parameter UI. | you want raw predictions, or you retrain to the next version |
| **`experimenting_ml/`** — the workbench | The working layer. The research pipeline that chose the models, the uncertainty / novelty / trust-score layer, the dataset-growth loop, and **the scenario UI you actually use day to day**. Reads the engine and grows its training data. | scenario screening, running a dataset-growth round, operating the console |
| `archive/brexit_ml/` | Superseded Phase-1 corridor surrogate. Kept for traceability only — not part of the live system. | — |

### How the two parts fit together

```
engine (frozen, v1)  ──read──▶  workbench: predict → trust-score → flag
                                        │
                                        ▼
                            run flagged points in AnyLogic, ingest results
                                        │  training data grows (129 → 179 → …)
                                        ▼
                     when enough new data:  retrain  ─▶  engine v2 (frozen)
```

The engine is the frozen model; the workbench uses it, grows its training
data, and **periodically produces the next frozen version**. `v1` is never
modified — new versions land as `models/v2/`, `v3/`, … and the API/UI switch
to them.

---

## Quick start

```bash
./SETUP.sh      # build both environments (Python 3.8.10, one-time)   ·  Windows: .\SETUP.ps1
./LAUNCH.sh     # start the scenario UI at http://localhost:8000/UI/  ·  Windows: .\LAUNCH.ps1
```

That's the whole thing. `LAUNCH` opens the **scenario Decision-Intelligence
UI** — the primary interface (predictions, uncertainty, SHAP, and the operator
console under *Settings*).

To serve the simpler raw-surrogate parameter UI instead:

```bash
cd nolhc_ml && ./.venv/bin/python -m uvicorn main:app --port 8001
```

---

## Going deeper

| Document | For |
|---|---|
| **`docs/NOLHC_ML_Engine_Technical_Report.md`** | The full handover manual — architecture, how the engine is built, how to reproduce every result, how to run a dataset-growth round, how to extend for new inputs / KPIs, a step-by-step guide for a new engineer. **Start here.** |
| `REPRODUCE.md` | The condensed "clean clone → running system" checklist. |
| `experimenting_ml/docs/spec.md` | The engineering spec + open-questions log for the uncertainty / self-extension work. |

## Environment

Python **3.8.10**, one interpreter for both parts. Each part has its own
virtual environment built from its own `requirements.lock.txt` (exact pins).
`SETUP` does this for you. No database, no cloud account needed to run the
engine, the pipeline, or either UI — only a live AnyLogic Cloud subscription
is needed to run a *new* dataset-growth round.
