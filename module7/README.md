# Module 7: My Alzheimer's knowledge graph (Neo4j)

Dhairya Bhatia · Alzheimer's disease (AD)

This module connects my evidence from Modules 2–6 in one Neo4j knowledge graph. The 15 Alzheimer's genes from Module 2 carry my own results (RNA, protein, GWAS, druggability, structure), and around them I added public pathways, drugs, related diseases and symptoms from Open Targets, plus 200 patients from the Module 6 cohort. I then asked questions in Cypher, ranked the genes with PageRank fused with my scores, found communities, and stratified the patients by APOE genotype.

| File | What it is |
|---|---|
| `BIOT6900_Module7_Assignment.ipynb` | The assignment, run top to bottom against my AuraDB Free instance |
| `REPORT.pdf` | The report (4 pages) |
| `figures/kg_neo4j_view.png` | Part of the graph in Neo4j Explore (report Figure 1) |
| `figures/kg_overview.png` | The whole graph without patients, drawn by the notebook |
| `kg_data/` | The public data the graph uses, fetched from Open Targets |
| `scripts/build_kg_data.py` | Fetches `kg_data/` (`python scripts/build_kg_data.py` from this folder) |
| `BIOT6900_Module7_Toy_KnowledgeGraph.ipynb`, `BIOT6900_Module7_RealModel_Neo4j.ipynb` | Lab notebooks (not graded) |

## Results

- *Graph:* 415 nodes (15 genes, 50 pathways, 5 drugs, 3 diseases, 140 phenotypes, 2 APOE variants, 200 patients) and 329 relationships.
- *Drugs on my genes:* mipomersen (APOB, approved for high cholesterol), apelin (APLNR, phase 2), and three candidates on HLA-DRB1. None is indicated for Alzheimer's.
- *Repurposing walk:* the HLA-DRB1 candidates are reached through Parkinson disease, which shares depression and parkinsonism with Alzheimer's.
- *Top genes (PageRank fused with my scores):* PECAM1, APOC1, ITGAX, HLA-DRB1, APOE. APLNR, my lead small-molecule target, is 11th because public data barely links it to Alzheimer's.
- *Patients:* the risk-score percentile rises from 41 (e3/e3) to 99 (e4/e4), and e4 carriers have a higher simulated case rate in every ancestry group.

## Data sources

- *My outputs:* `../module2/targets_ad.csv`, `../module3/targets_ad_w3.csv`, `../module4/structure_assessment_ad.csv`.
- *Open Targets Platform (public API, no key):* Ensembl ids, Alzheimer's association scores, Reactome pathways, drugs and clinical candidates, related-disease scores, and HPO phenotypes. Saved in `kg_data/` so the graph rebuilds offline.
- *Module 6 cohort:* 200 people sampled from the course `data.zip` in `../module6/data/` (not committed). Their APOE genotypes are real 1000 Genomes data; their case labels are the course's simulation.

## Running it

The notebook uses the `biot6900` conda environment (with `neo4j` and `networkx`). The connection URI is in the first code cell. The Neo4j username and password are stored as variables of the `biot6900` environment (`conda env config vars`), never in the notebook or the repository; the cell reads them from there. `RESET = True` in Section 2 clears the instance before loading, so a re-run gives the same graph.

## What didn't work, or needs a caveat

- *Two candidate related diseases were not found* in Open Targets under the ids I tried (multiple sclerosis and coronary artery disease), so they were skipped; the script picked Parkinson disease and schizophrenia from the rest.
- *HPO has a phenotype named "Alzheimer disease",* which collided with the disease node and made a self-loop; the notebook skips phenotypes named after a disease.
- *Duplicate drug:* Open Targets lists mipomersen and its sodium salt separately; the notebook keeps one.
- *Patients left out of PageRank:* they only link to the two APOE variants, so including them would rank APOE by my sample size.
- *Text-to-Cypher (optional) and GDS Sessions (optional)* were not used.
