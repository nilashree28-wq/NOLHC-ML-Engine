NOLHC Brexit ML Simulator - Submission Package
=============================================

This folder is a clean handover package for mentor evaluation and teammate validation.

Included folders
----------------
1) experimenting_ml  -> Main runnable mentor-facing app (UI + inference API)
2) nolhc_ml          -> Core ML training/inference support modules
3) brexit_ml         -> Baseline/reference implementation

Quick start (new machine)
-------------------------
1) Open terminal in this submission_package folder.
2) Create virtual environment:
   python -m venv .venv

3) Activate virtual environment:
   macOS/Linux:
   source .venv/bin/activate

   Windows PowerShell:
   .venv\Scripts\Activate.ps1

4) Install dependencies:
   pip install -r experimenting_ml/requirements.txt

5) Start app server:
   cd experimenting_ml
   python run_ui_inference_api.py

6) Open browser:
   http://127.0.0.1:8000/UI/index.html

Validation checklist for teammate
---------------------------------
[ ] UI page loads with Scenario Controls on left
[ ] Clicking "Run simulation" updates KPI cards
[ ] SHAP panel appears with Focus KPI dropdown
[ ] Changing Focus KPI updates bars/model/note
[ ] API health works: http://127.0.0.1:8000/api/health

Common issues
-------------
1) Blank page:
   - Hard refresh: Cmd/Ctrl + Shift + R
   - Ensure you run via http://127.0.0.1:8000, not file://

2) Missing module/package:
   - Re-activate .venv
   - Re-run pip install -r experimenting_ml/requirements.txt

3) Port already used:
   python run_ui_inference_api.py --port 8010
   Then open: http://127.0.0.1:8010/UI/index.html

Create zip for sharing
----------------------
From project root ("Final Brexit ML Design"):

zip -r submission_package.zip submission_package -x "*/.venv/*" "*/__pycache__/*" "*.DS_Store"

