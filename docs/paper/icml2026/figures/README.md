# Figures for `main.tex`

Copy PNGs from `experimenting_ml/outputs/` into this folder (paths relative to `docs/paper/icml2026/`).

Hold-out residual diagnostics and optional heatmap/SHAP figures are embedded in Appendix **Supplementary tables and figures** (`app:supp` in `main.tex`); Experiments/Results/Discussion cite them as `Figure~\ref{...} (Appendix)` in the main body.

## Copied in repo (hold-out residual diagnostics)

| File | Source |
|------|--------|
| `TT_OB_Agri_holdout_residual_diagnostics.png` | `outputs/test_evaluation_final/plots/TT_OB_Agri_holdout_residual_diagnostics.png` |
| `WT_IB_NA_Ross_holdout_residual_diagnostics.png` | `outputs/test_evaluation_final/plots/WT_IB_NA_Ross_holdout_residual_diagnostics.png` |
| `Uti_DAFM_D_holdout_residual_diagnostics.png` | `outputs/test_evaluation_final/plots/Uti_DAFM_D_holdout_residual_diagnostics.png` |

Each panel: predicted vs.\ actual, residual vs.\ predicted, residual histogram (hold-out $n{=}26$).

## Suggested additions (not copied; add before camera-ready)

| Suggested filename | Source |
|--------------------|--------|
| `shap_TT_OB_Agri_beeswarm.png` | Regenerate from `run_step4_shap.py` / `outputs/step4_shap/` (no PNG in tree by default) |
| `paired_ttest_pvalue_heatmap.png` | Export from `cv_fold_details.xlsx` paired-$t$ tab (Excel heatmap) |
| `friedman_cd_diagram.png` | Step~2 mentor diagnostics under `outputs/step2/` |
| `calibration_Uti_Cus_D.png` | `outputs/step3/calibration/calibration__Uti_Cus_D__GPR_Matern.png` |

Remaining residual plots: `outputs/test_evaluation_final/plots/*_holdout_residual_diagnostics.png` (20 targets).
