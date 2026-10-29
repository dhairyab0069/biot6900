# Portfolio Deliverable 1: Multi-omics target discovery package

Dhairya Bhatia · Alzheimer's disease (AD)

This package brings Labs 2 to 4 together into one 6-page report. It follows my AD targets from multi-omics evidence (Lab 2), through druggability triage with protein language models (Lab 3), to AlphaFold structure and pocket assessment (Lab 4), and ends with a ranked shortlist of five targets: APLNR, ITGAX, PECAM1, HLA-DRB1 and APOE. No new analysis was run; the figures are re-plotted from saved lab outputs.

| File | What it is |
|---|---|
| `REPORT.pdf` | The 6-page package submitted on Canvas |
| `make_figures.py` | Re-plots Figures 1, 2 and 4 from the Module 2 and 4 outputs (`python portfolio1/make_figures.py` from the repository root) |
| `figures/` | Figure 1 (integration), Figure 2 (Venn diagrams), Figure 3 (modality map, copied from Module 3), Figure 4 (structures with pLDDT and pockets) |

**Data sources (all public):**
- Lab 2: AMP-AD RNA-seq and TMT proteomics summaries from Agora, and AD associations from the GWAS Catalog (`module2/data/`, `module2/targets_ad_full.csv`).
- Lab 3: the course data pack (ESM C and ESM-2 embeddings, Open Targets tractability labels) and my re-ranked table `module3/targets_ad_w3.csv`.
- Lab 4: AlphaFold DB v6 models and fpocket output in `module4/structures/` (downloaded by the Module 4 notebook, not committed), and RCSB PDB entries 4NEH, 3K6S, 1N3Y, 7SUS and 1CQP.

**What did not work, or needs a caveat:**
- Structures are drawn as an alpha-carbon trace coloured by pLDDT, made with matplotlib, because PyMOL and ChimeraX are not installed on my laptop. The pockets are fpocket's alpha-sphere centres.
- Only ITGAX and APLNR were assessed structurally in Lab 4, so PECAM1, HLA-DRB1 and APOE have no structure evidence in the shortlist.
- ESMFold and Boltz-2 were optional in Lab 4 and were not run.
- `make_figures.py` needs `module4/structures/`, which is not in the repository; run the Module 4 notebook first to download it.
