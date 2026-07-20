# Word submission (Group 18 research paper)

## Regenerate `Group18_Research_Paper.docx`

From this directory:

```bash
pandoc main.tex -o Group18_Research_Paper.docx \
  --bibliography=example_paper.bib \
  --citeproc \
  --from=latex \
  --resource-path=.:figures
```

Requires [Pandoc](https://pandoc.org/) 3.x. Install on macOS: `brew install pandoc`.

## Contents

| File | Role |
|------|------|
| `main.tex` | Full paper (A4, 0.5 in margins, two-column, Times, numeric natbib) |
| `example_paper.bib` | Bibliography (`references.bib` plus keys cited in the Word draft) |
| `experiment_pipeline.tex` | Appendix workflow figure and CV algorithm (`\input` from `main.tex`) |
| `figures/` | Hold-out residual PNGs referenced by `\includegraphics` |

## After import into Word

Pandoc does not reproduce LaTeX layout exactly. Expect to touch up:

- **Equations** — display math and multi-line `align` blocks; check `\R`, fractions, and subscripts.
- **Tables** — colored `table*` and narrow two-column tables; column widths and wrapping.
- **Figures** — TikZ pipeline diagram and `algorithm` float may appear as raw text or simplified blocks; residual PNGs in `figures/` should embed if paths resolve.
- **Two-column layout** — set Word to two columns (Layout → Columns) to match submission guidelines.
- **Headers** — re-create running head / page numbers (LaTeX `fancyhdr` is not carried over).
- **Bibliography** — numbered list from citeproc; verify order and missing metadata notes in `.bib`.
- **Related Work** — pasted `\item` lists without `\begin{itemize}` may need manual bullet formatting.

## Figures

Copy additional PNGs into `figures/` before regenerating (see `../figures/README.md`). Placeholders remain for `paired_ttest_pvalue_heatmap.png` and `shap_TT_OB_Agri_beeswarm.png` if not present.
