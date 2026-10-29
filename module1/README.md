# Module 1: Setup and first database queries

Dhairya Bhatia

This module checks the `biot6900` environment and makes a first query to four biology databases. The last query, the APOE variant rs7412, is where the Alzheimer's disease thread of this repository begins.

| File | What it is |
|---|---|
| `module1_setup.ipynb` | The course Week 1 starter, filled in and run top to bottom |

## What the notebook does

*Part A, environment check:* prints the Python version, interpreter path, OS and active conda environment, then the versions of BioPython, pandas, numpy and requests.

*Part B, BioPython:* builds a 24-base `Seq` and translates it to the protein `MAIVMGR*`, with a one-line note on what translation did.

*Part C, database queries:* one live request per database, each with a short note.

- PubMed via `Bio.Entrez`: searched "AlphaFold protein structure" and got 5 PMIDs.
- UniProt: accession P04637, "Cellular tumor antigen p53".
- RCSB PDB: entry 1TUP, "Tumor suppressor p53 complexed with DNA".
- GWAS Catalog: variant rs7412 (APOE), a missense variant.

Nothing is saved to disk.

## Data sources

All public, queried live: PubMed (NCBI Entrez), UniProt REST, RCSB PDB REST and the GWAS Catalog REST API.

## Running it

```bash
conda activate biot6900
jupyter lab module1_setup.ipynb
```

Part C needs an internet connection. PubMed and GWAS Catalog results change over time, so a re-run may not return the exact IDs above.

Last run with Python 3.14.7 on macOS (arm64), BioPython 1.86, pandas 3.0.5, numpy 2.5.2 and requests 2.34.2.

## What didn't work

Nothing needed a workaround in this module.
