# Module 8: One tumour, two views

*Name:* Dhairya Bhatia

*Target gene:* EPCAM (the starter's default)

*Disease:* breast cancer (single-cell data from the CELLxGENE Census and a 10x Visium breast cancer section)

*Files:*

- `BIOT6900_Module8_Assignment_Starter.ipynb`: the executed notebook, every TODO filled in, run top to bottom on the Explorer cluster.
- `Module 8 report.docx` and `Module 8 report.pdf`: the report.
- `BIOT6900_Module8_SingleCell_Toy_pbmc3k.ipynb` and `BIOT6900_Module8_Spatial_Toy_Visium.ipynb`: the worked toy notebooks (single-cell and spatial).

*Note on the results:* some results may have small issues. The cluster's GPU nodes failed partway through the work, because their driver was too old for the installed PyTorch, and time was limited. So scVI ran on the CPU for 60 epochs instead of on a GPU for 200. Jobs on the cluster also failed quite a few times in between, so I had to re-evaluate the work and run it again. Changes in the cluster's rules also meant it took me extra time to reconnect to the cluster while running jobs and checking the data. The scVI scores in particular may be weaker than a full GPU run would give.

*What did not run as in the starter, or is different:*

- The Census query could not be read from the cluster, so I ran the starter's own query and sampling (seed 0) on a laptop and saved the 20,000-cell sample. The notebook loads that saved file.
- Highly variable genes use `span=0.4`, because the default failed on two donors.
- `rng` is recreated with seed 0, so the silhouette subsample differs from the starter's generator state.
- Moran's I was run on the highly variable genes with 100 permutations.
