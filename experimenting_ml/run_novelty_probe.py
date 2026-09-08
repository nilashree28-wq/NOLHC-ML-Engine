"""
Novelty-scorer probe (Ch5 §5.6 / Figure 5.4 evidence artifact).

Reproduces, as a table, the measured d=35 behaviour that
tests/test_novelty.py asserts pointwise and loop/novelty.py documents in
prose: a single-input extreme is never flagged; a multi-input excursion
always is. Run from experimenting_ml/:

    ./.venv/bin/python run_novelty_probe.py

Deterministic (IsolationForest seed 42, fit on the committed 129x35).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from data import load_xy  # noqa: E402
from loop.novelty import NoveltyScorer  # noqa: E402


def main() -> None:
    X_df, _ = load_xy()
    X = X_df.to_numpy(dtype=float)
    cols = list(X_df.columns)
    scorer = NoveltyScorer().fit(X)  # IsolationForest(n_estimators=200, contamination="auto", random_state=42)

    in_sample = scorer.score(X)
    threshold = float(np.quantile(in_sample, 0.90))
    base = X[0:1].copy()
    col_max = X.max(axis=0)
    col_min = X.min(axis=0)

    print(f"n={X.shape[0]}  d={X.shape[1]}  IsolationForest(200, contamination='auto', seed=42)")
    print(
        f"in-sample novelty score : median={np.median(in_sample):.4f}  "
        f"mean={np.mean(in_sample):.4f}  max={in_sample.max():.4f}"
    )
    print(
        f"90th-percentile threshold = {threshold:.4f}  "
        f"({int((in_sample > threshold).sum())} of {len(X)} training rows sit above their own threshold by construction)\n"
    )

    print(f"SINGLE-DIMENSION excursion -- push one factor ({cols[0]}) to k x its observed max")
    print(f"  {'k':>5} {'score':>9} {'flagged':>9}")
    for k in (1, 2, 3, 5, 10, 20, 50, 100):
        x = base.copy()
        x[0, 0] = col_max[0] * k
        s = scorer.score(x)[0]
        print(f"  {k:>5} {s:>9.4f} {str(s > threshold):>9}")

    hi = sum(
        scorer.score(_perturb(base, j, col_max[j] * 20))[0] > threshold for j in range(X.shape[1])
    )
    lo = sum(
        scorer.score(_perturb(base, j, col_min[j] - abs(col_min[j]) * 20 - 1))[0] > threshold
        for j in range(X.shape[1])
    )
    print(f"\n  factors flagged by a 20x-max single push : {hi} / {X.shape[1]}")
    print(f"  factors flagged by an extreme-low single push : {lo} / {X.shape[1]}")

    print("\nMULTI-DIMENSION excursion -- push ALL 35 factors to k x their max together")
    print(f"  {'k':>5} {'score':>9} {'flagged':>9}")
    for k in (1.1, 1.25, 1.5, 2, 3, 5, 10):
        s = scorer.score((col_max * k).reshape(1, -1))[0]
        print(f"  {k:>5} {s:>9.4f} {str(s > threshold):>9}")

    rng = np.random.default_rng(0)
    n_trials = 50
    hits = 0
    for _ in range(n_trials):
        idx = rng.choice(X.shape[1], X.shape[1] // 2, replace=False)
        x = base.copy()
        x[0, idx] = col_max[idx] * 3
        hits += scorer.score(x)[0] > threshold
    print(f"\n  random {X.shape[1] // 2}-factor 3x-max excursions flagged : {hits} / {n_trials}")


def _perturb(base: np.ndarray, col: int, value: float) -> np.ndarray:
    x = base.copy()
    x[0, col] = value
    return x


if __name__ == "__main__":
    main()
