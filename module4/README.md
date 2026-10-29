# Module 4: Structure-based druggability

Dhairya Bhatia · Alzheimer's disease (AD)

This module takes my two Module 3 targets, ITGAX and APLNR, and asks whether their predicted 3D structures have a place where a drug could bind, and whether those structures can be trusted. I read AlphaFold confidence (pLDDT and PAE), compared each prediction with an experimental structure, found pockets with fpocket, and checked them against a real bound drug.

| File | What it is |
|---|---|
| `BIOT6900_Module4_Assignment.ipynb` | The assignment, run top to bottom (Kernel → Restart & Run All) |
| `structure_assessment_ad.csv` | Summary table from Step 7 |
| `REPORT.pdf` | The 5-page report |
| `figures/` | pLDDT, PAE and deviation plots taken from the notebook for the report |
| `BIOT6900_Module4_Part1_ToyModel.ipynb`, `..._Part2_RealData.ipynb`, `..._Demo_DrugPocket.ipynb` | Lab notebooks (not graded) |

**Targets:**
- **ITGAX** (P20702, Module 2 rank 6): compared with 4NEH chain A. Call: possible but uncertain, antibody as the realistic modality.
- **APLNR** (P35414, Module 2 rank 10): compared with 7SUS chain A, which has the small-molecule agonist 8EH bound. Call: structure supports a small-molecule pocket.

**Beyond the TODO cells:** I added three extra cells.
- **ITGAX per region:** per-region RMSD for ITGAX against 4NEH and 3K6S, plus block PAE. The domain finder merges ITGAX into one domain at PAE < 8 Å, even though the I domain and the legs have a mean PAE of 17–20 Å to the rest.
- **APLNR without the insert:** an APLNR RMSD that drops the three pairs the alignment made with the rubredoxin insert in 7SUS (2.83 Å before, 1.11 Å after). The CSV reports the insert-free value. I also placed the drug in the model to check for clashes.
- **Borrowed-ligand test for ITGAX:** lovastatin from the LFA-1 I domain (1CQP), with a positive control on LFA-1 itself.

**Data sources (all public):**
- AlphaFold Protein Structure Database v6: predicted structures and PAE for ITGAX (P20702) and APLNR (P35414).
- RCSB Protein Data Bank: 4NEH and 3K6S (ITGAX/β2 integrin), 1N3Y (ITGAX I domain), 7SUS (APLNR with agonist 8EH), 7W0L (APLNR with G protein), 1CQP (LFA-1 I domain with lovastatin), and 1TUP (p53, lab Part 2).
- UniProt: sequences and residue numbering.
- fpocket (conda-forge) for pocket detection.

**What didn't work, or needs a caveat:**
- **4NEH has no drug-like ligand.** The provided ligand-site check therefore reports only glycans (NAG, MAN, BMA) for ITGAX, which are not drug sites.
- **ESMFold:** not run; it was optional.

`structures/` is in `.gitignore`. The notebook downloads everything on first run (fpocket from conda-forge is required).
