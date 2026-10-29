# Module 5: Variant interpretation on CYP2C19

Dhairya Bhatia · Gene: **CYP2C19** (assigned on Canvas)

This module interprets the ClinVar variants of CYP2C19, a liver enzyme that activates clopidogrel and breaks down several common drugs. I filtered variants by population frequency, calibrated CADD against known labels, tried to reclassify the 33 variants of uncertain significance (VUS), and examined one variant where the tools disagree (CYP2C19\*2).

| File | What it is |
|---|---|
| `BIOT6900_Module5_Part3_Assignment.ipynb` | The assignment, run top to bottom (Kernel → Restart & Run All) |
| `pgx_classified_CYP2C19.csv` | The 33 VUS with their CADD band, pooled evidence and my provisional call |
| `REPORT.pdf` | The report (3 pages) |
| `figures/`, `scripts/make_figures.py` | Report figure: CADD calibration bands with CYP2C19's own no-function alleles (`python module5/scripts/make_figures.py` from the repository root; needs the notebook's `data/` cache) |

**Data sources (all public):**
- MyVariant.info, which serves ClinVar (clinical labels), CADD, REVEL, AlphaMissense and gnomAD allele frequencies for each variant.
- DPYD variants from the same source, used to pool the CADD calibration.
- Star-allele names (\*2, \*3, \*17 and others) follow PharmVar and the CPIC guidelines.

**Atlas:** not run. I had no AlphaGenome API key, so `SKIP_ATLAS = True`. The report answers the Atlas question from reasoning.

**Fallbacks and notes:**
- **Calibration:** not possible on CYP2C19 alone, because ClinVar has 0 pathogenic or likely pathogenic variants for it; its functional alleles are labelled "drug response". I pooled with DPYD, the documented route. A transfer test then placed CYP2C19's own no-function alleles \*2 and \*4 in the pooled "strong, benign" band, so I did not let the pooled bands move any VUS. All 33 stay VUS.
- **Frequency filter:** variants with no gnomAD frequency are kept as rare rather than dropped.
- **Large deletions:** 8 ClinVar records are large deletions with no consequence annotation. They are labelled `none (large deletion, CNV)` so they appear in the coverage table instead of being dropped.
- **Notebook fix:** the course notebook used the cell type `md`, which Jupyter rejects. I changed those cells to `markdown`; nothing else in the provided cells was changed.

`data/` is in the repository's `.gitignore`. On a first run the notebook fetches CYP2C19 and DPYD from MyVariant.info and caches them there.
