# Module 3: Target Triage with Protein Language Models in Alzheimer's Disease

**BIOT 6900 · Module 3 Assignment (Computational Lab 3)**
Dhairya Bhatia · Northeastern University · Disease: **Alzheimer's disease (AD)**

This module adds a tractability check to my 15 AD targets from Module 2. It asks whether each
target looks like proteins we already know how to drug, and with which modality (small molecule or
antibody). It also scores the course anchor variants (APOE ε2 and ε4, TREM2 R47H, a p53 hotspot)
and re-ranks the targets for Week 4 (structure prediction).

## Contents

| Path | Description |
|---|---|
| `BIOT6900_Module3_Assignment.ipynb` | Assignment notebook (Steps 1 to 7), runs top to bottom with `Restart & Run All` |
| `targets_ad.csv` | Input: my Module 2 top 15 AD targets (copied from `../module2`) |
| `targets_ad_w3.csv` | **Deliverable:** re-ranked targets, the hand-off to Week 4 |
| `REPORT.pdf` / `REPORT.md` | Written report |
| `modality_map.png` | Report figure: small-molecule versus antibody prior for each target (`python scripts/make_modality_map.py`) |
| `BIOT6900_Module3_Part2_RealData.ipynb` | Lab Part 2 notebook (self-paced, not graded) |
| `data/` | The course data pack from Canvas (`BIOT6900_Module3_DataPack.zip`), not committed (see `.gitignore`) |
| `scripts/build_data_pack.py` | Extra: my own build of a data pack from public sources, written before the course pack was posted. Writes to `data_student_built/` (not committed) |

## Reproducing the analysis

Uses the `biot6900` conda environment with scikit-learn and matplotlib.

1. Download `BIOT6900_Module3_DataPack.zip` from the Module 3 Canvas page, unzip it, rename the
   folder to `data`, and put it in this folder (the 11 files sit directly inside `data/`).
2. Run:

```bash
conda activate biot6900
jupyter lab BIOT6900_Module3_Assignment.ipynb
# then: Kernel > Restart & Run All
```

## The data pack

The analysis uses the course data pack (`data/manifest.json`): a 1,201-protein training panel
(401 with clinical precedence, 821 family groups), 20,190 reviewed human proteins, ESM C 300M and
ESM-2 35M embeddings, Open Targets tractability labels, and ESM-2 650M variant scores. Variants use
UniProt precursor numbering, which includes APOE's 18-residue signal peptide (R176C is mature
R158C, ε2, and C130R is mature C112R, ε4).

### Extra: my own data pack build

Before the course pack was posted I built a pack myself with `scripts/build_data_pack.py`
(UniProt, Open Targets, HGNC; ESM C 300M, ESM-2 35M and ESM-2 650M run locally). It used its own
1,200-protein panel draw and only embedded the panel plus my Module 2 genes. The submitted results
use the course pack; the script is kept as extra work and now writes to `data_student_built/`.

## Issues encountered

- **Data pack posted late:** the course data pack was not on Canvas when I started, so I first built
  my own (see above), then re-ran everything on the course pack once it was posted. The issues
  below are from that build.
- **UniProt download stalled:** the UniProt `/stream` endpoint kept stalling, so the script pages
  through the `/search` endpoint 500 entries at a time instead
- **Out of memory:** on an 8 GB laptop, ESM-2 650M in full precision filled memory and swapped for
  over 30 minutes without finishing, so the variant stage loads the model in half precision
  (float16) and masks 8 positions per batch
- **Column names:** no renaming was needed, since `targets_ad.csv` already has `gene` and `score`
