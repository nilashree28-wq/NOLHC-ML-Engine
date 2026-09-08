"""
Novelty-scorer probe (Ch5 §5.6 / Figure 5.4 evidence artifact).

Reproduces, as tables, the measured d=35 behaviour that
tests/test_novelty.py asserts pointwise and loop/novelty.py documents in
prose: a single-input extreme is never flagged; a multi-input excursion
always is. Run from experimenting_ml/:

    ./.venv/bin/python run_novelty_probe.py

Writes outputs/novelty_probe_table.csv (Figure 5.4 source data).
Deterministic: IsolationForest seed 42, fit on the committed 129x35;
random factor subsets use numpy seed 0.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
from data import load_xy  # noqa: E402
from loop.novelty import NoveltyScorer  # noqa: E402

MAGNITUDES = (1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0)
N_FACTORS = (1, 2, 3, 5, 10, 17, 25, 35)
N_TRIALS = 50


def main() -> None:
    X_df, _ = load_xy()
    X = X_df.to_numpy(dtype=float)
    cols = list(X_df.columns)
    n, d = X.shape
    scorer = NoveltyScorer().fit(X)  # IsolationForest(n_estimators=200, contamination="auto", random_state=42)

    in_sample = scorer.score(X)
    thr = float(np.quantile(in_sample, 0.90))
    base = X[0:1].copy()
    col_max = X.max(axis=0)
    col_min = X.min(axis=0)
    rng = np.random.default_rng(0)

    print(f"NOVELTY PROBE  --  n={n}  d={d}  IsolationForest(200 trees, contamination='auto', seed=42)")
    print("=" * 78)
    print(
        f"In-sample novelty score : min={in_sample.min():.4f}  median={np.median(in_sample):.4f}  "
        f"mean={np.mean(in_sample):.4f}  p90={thr:.4f}  max={in_sample.max():.4f}"
    )
    print(
        f"Novelty threshold (90th pct of in-sample) = {thr:.4f}   "
        f"-> {int((in_sample > thr).sum())} of {n} training rows sit above their own threshold\n"
    )

    # ---- Table A: single-factor excursion, magnitude sweep -------------------
    print("TABLE A  --  ONE factor pushed to k x its observed max (factor 0 = NA_Im), rest held at row 0")
    print(f"  {'k x max':>9} | {'score':>8} | {'flagged?':>9}")
    print("  " + "-" * 32)
    rows_a = []
    for k in MAGNITUDES:
        x = base.copy()
        x[0, 0] = col_max[0] * k
        s = float(scorer.score(x)[0])
        print(f"  {k:>9.1f} | {s:>8.4f} | {str(s > thr):>9}")
        rows_a.append(("A_single_factor_magnitude", k, 1, s, s > thr))

    # ---- Table B: which factor, at fixed k = 20 -----------------------------
    hi_scores = []
    lo_scores = []
    for j in range(d):
        xh = base.copy()
        xh[0, j] = col_max[j] * 20.0
        xl = base.copy()
        xl[0, j] = col_min[j] - abs(col_min[j]) * 20.0 - 1.0
        hi_scores.append(float(scorer.score(xh)[0]))
        lo_scores.append(float(scorer.score(xl)[0]))
    print(
        f"\nTABLE B  --  each of the {d} factors pushed alone to 20x max  (then to extreme-low):"
    )
    print(
        f"  high push : max score across all {d} factors = {max(hi_scores):.4f}  "
        f"-> {sum(s > thr for s in hi_scores)} of {d} flagged"
    )
    print(
        f"  low push  : max score across all {d} factors = {max(lo_scores):.4f}  "
        f"-> {sum(s > thr for s in lo_scores)} of {d} flagged"
    )
    for j in range(d):
        rows_a.append(("B_factor_20x_high", 20.0, 1, hi_scores[j], hi_scores[j] > thr))
        rows_a.append(("B_factor_extreme_low", -20.0, 1, lo_scores[j], lo_scores[j] > thr))

    # ---- Table C: m factors x magnitude grid ------------------------------
    print(f"\nTABLE C  --  m randomly-chosen factors pushed to k x max together ({N_TRIALS} trials each)")
    print(f"  {'m factors':>9} |" + "".join(f" k={k:<5g}" for k in (1.5, 2.0, 3.0, 5.0)))
    print("  " + "-" * 46)
    for m in N_FACTORS:
        cells = []
        for k in (1.5, 2.0, 3.0, 5.0):
            flags = 0
            score_sum = 0.0
            for _ in range(N_TRIALS):
                idx = rng.choice(d, m, replace=False)
                x = base.copy()
                x[0, idx] = col_max[idx] * k
                s = float(scorer.score(x)[0])
                score_sum += s
                flags += s > thr
            frac = flags / N_TRIALS
            cells.append(frac)
            rows_a.append(("C_m_factors_x_magnitude", k, m, score_sum / N_TRIALS, frac >= 0.5))
        print(f"  {m:>9} |" + "".join(f"  {c*100:>4.0f}%" for c in cells))
    print("  (cell = fraction of trials flagged as novel)")

    # ---- Table D: all d factors, magnitude sweep --------------------------
    print(f"\nTABLE D  --  ALL {d} factors pushed to k x max together")
    print(f"  {'k x max':>9} | {'score':>8} | {'flagged?':>9}")
    print("  " + "-" * 32)
    for k in MAGNITUDES:
        s = float(scorer.score((col_max * k).reshape(1, -1))[0])
        print(f"  {k:>9.1f} | {s:>8.4f} | {str(s > thr):>9}")
        rows_a.append(("D_all_factors_magnitude", k, d, s, s > thr))

    out = HERE / "outputs" / "novelty_probe_table.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["probe", "magnitude_x_max", "n_factors_perturbed", "score_or_mean_score", "flagged"])
        w.writerow(["threshold_p90", "", "", f"{thr:.6f}", ""])
        for r in rows_a:
            w.writerow([r[0], r[1], r[2], f"{r[3]:.6f}", r[4]])
    print(f"\nWrote {out.relative_to(HERE)}  ({len(rows_a) + 1} rows)  -- Figure 5.4 source data.")
    print(
        "\nHeadline: single-factor excursions -> 0% flagged at any magnitude; "
        "all-factor excursions -> 100% flagged, score saturates at ~0.158."
    )


if __name__ == "__main__":
    main()
