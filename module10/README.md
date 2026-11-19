# Module 10: Build it, then break it

*Name:* Dhairya Bhatia

*What this is:* a DenseNet121 classifier for colon tumour versus normal tissue (PathMNIST), a barcode tag I added to the tumour images as a confounder, and tests with a clean control to see if the model learned the tag.

*Files:*

- `BIOT6900_Module10_Assignment.ipynb`: the executed notebook (run top to bottom on a laptop CPU, seed 0).
- `Module 10 report.docx` and `Module 10 report.pdf`: the report (the last page is a glossary for reference).
- `BIOT6900_Module10_Toy_MedNIST.ipynb`: the worked toy notebook.
- `build_subset.py`: builds the data file from the PathMNIST download.

*How to run:* use the `biot6900` environment (MONAI, MedMNIST, scikit-learn) and run the notebook. It needs `data/pathmnist_tumour_vs_normal_subset.npz` (600 training, 400 validation and 600 test images). This repo ignores data folders, so the file is not committed. Put the course's Canvas file there, or run `python build_subset.py` to build it (it downloads about 1 GB from Zenodo).

*What did not work or is different:* the course's Canvas subset file was not available, so I rebuilt the subset from the original PathMNIST (64 px, resized to 128 px). Because of that my numbers may differ from the course file. The results come from one run with one seed.
