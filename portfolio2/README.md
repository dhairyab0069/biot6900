# Portfolio 2: Genomics and precision medicine case study

*Name:* Dhairya Bhatia

*Disease and targets:* Alzheimer's disease; my Part I targets APLNR, ITGAX, PECAM1, HLA-DRB1 and APOE.

*Files:*

- `Portfolio 2 report.pdf` and `Portfolio 2 report.docx`: the case study (7 pages including references and a glossary).
- `figures/fig_cells.png`: my five Part I genes by cell type in the Lab 8 single-cell sample (a summary of the saved sample, not a new analysis).

*Sources:* `module5/` (CYP2C19 variants), `module6/` (risk score across ancestries), `module7/` (knowledge graph) and `module8/` (single-cell and spatial view).

*What is different or did not work:*

- CYP2C19 in Lab 5 was an assigned gene, not one of my Part I targets.
- Lab 8 used breast cancer data from the assignment, so the cell-type evidence for my Alzheimer's targets comes from a tumour sample, not from brain.
- Some Lab 8 results may have small issues: the cluster's GPU nodes failed, so scVI ran on a CPU for 60 epochs, and jobs failed several times before the final run.
- The risk score results use simulated case labels from the course.
