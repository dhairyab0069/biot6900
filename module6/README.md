# Module 6: Polygenic risk score portability

Dhairya Bhatia · Alzheimer's disease (AD)

This module applies a published Alzheimer's polygenic risk score to real genomes from five ancestry groups and asks whether it works equally well for all of them. It does not: the score works best in Europeans (AUC 0.672) and falls to chance in the African-ancestry group (0.493). An extra check shows most of that drop comes from how the course simulated APOE e4's effect, not from APOE biology.

| File | What it is |
|---|---|
| `BIOT6900_Module6_Part3_Graded.ipynb` | The graded Part 3 notebook, run top to bottom with `USE_DEMO = False` |
| `REPORT.pdf` | The report (4 pages) |
| `figures/` | `prs_by_ancestry.png` and `calibration_by_ancestry.png` (saved by the notebook), `fig_prs_calibration.png` (the two side by side) and `fig_auc_apoe.png` (extra check) |
| `scripts/extra_checks.py` | My extra check: each group's AUC without the two APOE SNPs and with e4 alone (`python scripts/extra_checks.py` from this folder) |

## Data sources

The course cohort `data.zip` from Canvas, unzipped to `data/` (not committed).

- *Score:* PGS Catalog PGS000334 (Zhang et al., 2020), 22 SNPs including APOE rs429358 (e4) and rs7412 (e2).
- *Genotypes:* 1000 Genomes phase 3, 2,336 people: EUR, AFR and EAS 500 each, SAS 489, AMR 347.
- *Phenotype and age:* simulated by the course, because 1000 Genomes has no disease labels.

The notebook's proof-of-data block (source REAL, checksums `9cf41a1f`, `f7a87d3f`, `7f80e8ff`, `6cc55b6e`) is in the report and matches the course data README.

## Results

| | EUR | SAS | EAS | AMR | AFR |
|---|---:|---:|---:|---:|---:|
| AUC | 0.672 | 0.611 | 0.575 | 0.555 | 0.493 |
| % above the pooled top-10% cutoff | 7.8 | 4.3 | 2.2 | 6.3 | 28.0 |
| AUC without the 2 APOE SNPs | 0.588 | 0.582 | 0.588 | 0.557 | 0.580 |

Harmonisation used all 22 SNPs (13 flipped, 0 dropped). Cross-validated AUC: age alone 0.562, age plus PRS 0.618.

## What didn't work, or needs a caveat

- *Simulated phenotype:* every AUC and calibration result illustrates the portability problem; none measures real AD risk.
- *APOE in AFR:* the simulation's proxy for e4 is almost unlinked to e4 in African-ancestry samples, so the near-chance AFR result is a property of the dataset, not evidence that e4 is unimportant there.
- *Own data first:* before the course data was posted I built a similar cohort from the PGS Catalog and 1000 Genomes on the Explorer cluster. It used different scores and had no phenotype, so the graded run uses the course data only.
- *Figures:* the notebook's plotting cells only showed the figures, so I added a `savefig` line to each to keep them for the report.
