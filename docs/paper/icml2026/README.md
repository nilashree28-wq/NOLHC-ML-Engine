# ICML-Style Research Paper (Group 18)

Draft LaTeX for converting your final project report into an ICML-format paper.

## Files

| File | Purpose |
|------|---------|
| `main.tex` | Full paper (abstract, intro, setup, method, experiments, UI, limitations) |
| `references.bib` | Starter bibliography (Harvard/BibTeX; compile with `natbib`) |
| `Makefile` | Build PDF |

## 1. Get official ICML style (required for submission)

1. Open the ICML author instructions for your target year (e.g. ICML 2026).
2. Download the official style bundle (`icml2026.sty`, `icml2026.bst`, `fancyhdr.sty`, etc.).
3. Copy those files into **this folder** (`docs/paper/icml2026/`).

Until you add `icml2026.sty`, you can compile a **draft** using the fallback in `main.tex` (uncomment the `article` block and comment the ICML block).

## 2. Build PDF

```bash
cd docs/paper/icml2026
make
```

Or manually:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

## 3. Map from your Word report

Paste content from `Analytics Live - Group 18_Report.docx` into:

- **Abstract** — executive summary paragraph
- **Introduction** — motivation, Brexit context, stakeholder needs
- **Related work** — expand `references.bib` with your supervisor’s reading list
- **Experiments** — tables/figures from `pipeline_results.xlsx` and mentor report
- **Acknowledgements** — group members, supervisors (remove for anonymous ICML submission)

## 4. Anonymous submission

For blind review, in `main.tex`:

- Use `\usepackage[accepted]{icml2026}` only for camera-ready; use default (no `accepted`) for review.
- Remove author names or use `\author{Anonymous}`.
- Avoid URLs that reveal identity.

## 5. Page limit

Check the current ICML call for main-track page limits (often 8 pages + references + appendix). Trim `\appendix` material if needed.
