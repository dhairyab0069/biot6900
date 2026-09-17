# BIOT 6900 Module 1

Dhairya Bhatia (bhatia.dh@northeastern.edu)

## Contents

| File | What it is |
|------|------------|
| `module1_setup.ipynb` | Module 1 starter notebook : environment check, BioPython intro, and four database API queries |

## What Module 1 does

The notebook is the course-provided Week 1 starter, filled in. It has four parts:

**Part A : Environment check.** Prints the Python version, the interpreter path, the OS, and the active conda environment, then prints versions for BioPython, pandas, numpy, and requests. This is just to confirm the `biot6900` environment is set up before starting real work.

**Part B : BioPython quickstart.** Builds a 24-base `Seq` object and calls `.translate()` on it to get the protein `MAIVMGR*`. One-line written answer explaining what translation did.

**Part C : Database API queries.** Four small requests, one per database, each followed by a short note:

- **PubMed** via `Bio.Entrez` : searched "AlphaFold protein structure", got 5 PMIDs back.
- **UniProt** REST : looked up accession `P04637`, which is "Cellular tumor antigen p53".
- **RCSB PDB** REST : looked up entry `1TUP`, "Tumor suppressor p53 complexed with DNA".
- **GWAS Catalog** (EBI) REST : looked up variant `rs7412` (APOE), reported as a missense variant.

All four are plain HTTP GETs where you build a query, send it, and read a field or two out of the JSON. Nothing is saved to disk.


## Running it

```bash
conda activate biot6900
jupyter lab module1_setup.ipynb
```

Run cells top to bottom. Parts C needs an internet connection since every cell there hits a live API. The PubMed and GWAS results can change over time, so re-running may not reproduce the exact IDs above.

Environment used when the notebook was last run: Python 3.14.7 on macOS (arm64), BioPython 1.86, pandas 3.0.5, numpy 2.5.2, requests 2.34.2.

## Status

- [x] Part A : environment verified
- [x] Part B : BioPython translation + note
- [x] Part C : all four API queries + notes
- [X] Repo link posted on Canvas
