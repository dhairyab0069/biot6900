# BIOT 6900: Following Alzheimer's disease from genes to drug targets

Dhairya Bhatia (bhatia.dh@northeastern.edu) · Northeastern University

Alzheimer's disease is the most common cause of dementia, and there are still very few treatments. This repository holds my BIOT 6900 coursework, and most of it follows one thread: start from the genetics of Alzheimer's, find genes that look involved, ask which of them a drug could reach, and then ask how well genetic risk carries over to people of different ancestries.

| Folder | Module | Question |
|---|---|---|
| [`module1/`](module1/) | 1. Setup | Is the environment working, and what does a database say about APOE? |
| [`module2/`](module2/) | 2. Multi-omics | Which genes change in Alzheimer's at the RNA, protein and DNA level? |
| [`module3/`](module3/) | 3. Protein language models | Which of those genes look like proteins we already know how to drug? |
| [`module4/`](module4/) | 4. Structure | Do the best two have a place on their 3D structure where a drug could bind? |
| [`portfolio1/`](portfolio1/) | Portfolio 1 | Labs 2 to 4 brought together into one ranked target package |
| [`module5/`](module5/) | 5. Variant interpretation | How do a patient's variants in CYP2C19 change the drugs they can take? |
| [`module6/`](module6/) | 6. Polygenic risk | Does an Alzheimer's risk score work equally well across ancestries? |

Each folder has its own README with the data sources and what didn't work, and a `REPORT.pdf`.

## The story

### 1. A first look at APOE

[Module 1](module1/) sets up the environment and sends a first query to PubMed, UniProt, the PDB and the GWAS Catalog. The last query is rs7412, a variant in APOE, the gene with the largest single effect on Alzheimer's risk. APOE comes back in almost every module after this.

### 2. Which genes change in Alzheimer's?

[Module 2](module2/) combines three public layers: brain RNA and brain protein from AMP-AD (Agora), and every published Alzheimer's GWAS hit. 1,115 genes are measured in all three, and each gets one score. Known Alzheimer's genes rise to the top (HLA-DRB1 at 2, APOE at 11, CLU at 31), which suggests the method works, and the top 15 fall into immune, lipid, synapse and blood-vessel groups.

<img src="module2/figures/fig1_integration.png" width="560" alt="RNA against protein change for 1,115 genes; the top 15 are circled">

### 3. Which of them could a drug reach?

[Module 3](module3/) asks whether each of the 15 genes looks like proteins that already have drugs, using protein language model embeddings, and whether a small molecule or an antibody fits better. Most of the list are cell-surface proteins that suit antibodies; APLNR, a G-protein-coupled receptor, is the one clear small-molecule candidate.

<img src="module3/figures/modality_map.png" width="520" alt="Small-molecule against antibody prior for the 15 targets">

### 4. Is there a pocket on the structure?

[Module 4](module4/) takes the two lead targets, ITGAX and APLNR, reads their AlphaFold confidence, compares each with an experimental structure and searches for pockets. APLNR's structure supports a small-molecule pocket, matching a real bound drug. ITGAX is less certain, so an antibody is the realistic route.

<img src="portfolio1/figures/fig4_structures.png" width="620" alt="AlphaFold structures of ITGAX and APLNR coloured by confidence, with pockets">

### Portfolio 1: the target package

[Portfolio 1](portfolio1/) brings Labs 2 to 4 together into one report and ends with a ranked shortlist: APLNR, ITGAX, PECAM1, HLA-DRB1 and APOE.

### 5. From the drug to the patient

[Module 5](module5/) turns from finding targets to how patients respond to drugs. CYP2C19 is a liver enzyme that switches on clopidogrel and breaks down several common drugs. I calibrated variant-effect scores against known labels and tried to reclassify 33 variants of uncertain significance. The scores placed CYP2C19's own known no-function alleles in a "benign" band, so I left all 33 as uncertain rather than trust them.

<img src="module5/figures/fig_cadd_calibration.png" width="520" alt="CADD calibration bands with CYP2C19 star alleles marked">

### 6. Back to APOE: does genetic risk travel?

[Module 6](module6/) returns to APOE as part of a 22-SNP Alzheimer's risk score, applied to 2,336 genomes from five ancestry groups. The score works best in Europeans (AUC 0.672) and falls to chance in the African-ancestry group (0.493). Removing the two APOE SNPs brings every group to about 0.58, which shows the drop comes from how the course data simulated APOE's effect, not from APOE biology.

<img src="module6/figures/fig_auc_apoe.png" width="560" alt="AUC by ancestry with and without the APOE SNPs">

## Running the notebooks

```bash
conda activate biot6900
jupyter lab
```

Open a module's notebook and run Kernel → Restart & Run All. Course data packs from Canvas (Modules 3 and 6) go in that module's `data/` folder and are not committed; Module 2 downloads its own data with `scripts/get_data.py`, and Module 4 downloads structures on first run.
