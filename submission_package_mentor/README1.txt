NOLHC Brexit ML Simulator - Mentor Submission Package
=====================================================

This is the reduced package for mentor evaluation.
It includes only the core implementation needed to run the project.
Environment Requirements (Important)
This submission includes pre-trained model artefacts (.joblib / .pkl).
To run inference/UI successfully, install the same library versions used during training.

Recommended Python
Python 3.10 (3.9 also supported if dependencies are installed correctly)
Required package compatibility
scikit-learn==1.3.2 (mandatory for included trained models)
If a different scikit-learn version is used (e.g., 1.6.x), model loading may fail with errors such as: 'ExtraTreeRegressor' object has no attribute 'monotonic_cst'

Included folders
----------------
1) experimenting_ml  -> Main runnable app (UI + inference API + model outputs)
2) nolhc_ml          -> Core ML utilities used by the inference stack

Setup Steps (macOS/Linux)
--------------------------------
# 1) Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Upgrade pip
python3 -m pip install --upgrade pip

# 3) Install project dependencies
pip install -r experimenting_ml/requirements.txt
pip install -r nolhc_ml/requirements.txt
pip install -r brexit_ml/requirements.txt

# 4) Force compatible scikit-learn version for shipped models
pip uninstall -y scikit-learn
pip install scikit-learn==1.3.2


Setup Steps (Windows PowerShell)
--------------------------------
# 1) Create and activate virtual environment
py -3 -m venv .venv
.venv\Scripts\Activate.ps1

# 2) Upgrade pip
python -m pip install --upgrade pip

# 3) Install project dependencies
pip install -r experimenting_ml/requirements.txt
pip install -r nolhc_ml/requirements.txt
pip install -r brexit_ml/requirements.txt

# 4) Force compatible scikit-learn version for shipped models
pip uninstall -y scikit-learn
pip install scikit-learn==1.3.2

Launch UI + Inference
--------------------------------
From project root:

cd experimenting_ml
python run_ui_inference_api.py --port 8000
Open in browser:

http://127.0.0.1:8000/UI/index.html
(or) http://127.0.0.1:8000/UI/sample%20template%20for%20sim_ml_xai_llm_platform%20(1).html

Troubleshooting
--------------------------------
1) python: command not found
Use python3 instead of python.

2) ExtraTreeRegressor has no attribute monotonic_cst
Cause: scikit-learn version mismatch with pre-trained artifacts.
Fix:

pip uninstall -y scikit-learn
pip install scikit-learn==1.3.2
3) favicon.ico / apple-touch-icon 404
Harmless browser icon requests; ignore.

4) If you must use newer sklearn versions
Re-train/re-generate model artifacts on that environment before running inference.


Quick validation
----------------
[ ] Scenario Controls visible on left panel
[ ] Run simulation updates KPI cards
[ ] SHAP panel shows explanatory drivers
[ ] Focus KPI dropdown updates SHAP values/model text
[ ] API health returns JSON at /api/health

Troubleshooting
---------------
1) Blank page:
   - Hard refresh (Cmd/Ctrl + Shift + R)
   - Use HTTP URL above (not file://)

2) Package/module errors:
   - Re-activate venv
   - Re-run: pip install -r experimenting_ml/requirements.txt

3) Port conflict:
   python run_ui_inference_api.py --port 8010
   then open http://127.0.0.1:8010/UI/index.html

Zip command
-----------
From project root:

zip -r submission_package_mentor.zip submission_package_mentor -x "*/.venv/*" "*/__pycache__/*" "*.DS_Store"

