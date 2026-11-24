import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "fig_cells.png"

genes = ["APLNR", "ITGAX", "PECAM1", "HLA-DRB1", "APOE"]
types = ["T", "Other", "Endothelial", "Macrophage", "Fibroblast", "B",
         "Epithelial/Tumor", "Monocyte", "NK", "DC"]
n = [12121, 3125, 1466, 1260, 1118, 586, 152, 73, 61, 38]

# percent of cells with the gene detected, rows = genes, columns = types
pct = np.array([
    [0.2, 1.6, 37.9, 0.2, 3.6, 0.3, 0.7, 0.0, 0.0, 0.0],
    [0.3, 1.7, 1.3, 30.8, 1.3, 1.4, 2.0, 42.5, 4.9, 15.8],
    [2.4, 3.7, 88.7, 33.3, 5.5, 4.9, 3.3, 35.6, 0.0, 5.3],
    [10.2, 3.6, 29.1, 56.8, 6.8, 73.2, 15.8, 93.2, 29.5, 94.7],
    [4.8, 62.8, 7.0, 64.4, 33.5, 5.6, 21.7, 34.2, 3.3, 13.2],
])
# mean log-normalised expression, same layout
mean = np.array([
    [0.00, 0.02, 0.61, 0.00, 0.05, 0.00, 0.02, 0.00, 0.00, 0.00],
    [0.01, 0.02, 0.01, 0.60, 0.02, 0.02, 0.01, 0.69, 0.13, 0.26],
    [0.03, 0.05, 2.11, 0.58, 0.07, 0.07, 0.05, 0.57, 0.00, 0.07],
    [0.18, 0.11, 0.57, 1.73, 0.11, 2.40, 0.28, 3.31, 0.83, 3.88],
    [0.09, 1.25, 0.10, 2.33, 0.88, 0.12, 0.51, 0.65, 0.07, 0.24],
])
frac = pct / 100
vmax = mean.max()

fig, ax = plt.subplots(figsize=(6.6, 3.2))
for i, gene in enumerate(genes):
    for j in range(len(types)):
        ax.scatter(j, len(genes) - 1 - i, s=30 + 420 * frac[i, j], c=[mean[i, j]],
                   cmap="viridis", vmin=0, vmax=vmax, edgecolor="#444", linewidth=.4)
ax.set_xticks(range(len(types)))
ax.set_xticklabels([f"{t} (n={k:,})" for t, k in zip(types, n)],
                   fontsize=6.5, rotation=30, ha="right", rotation_mode="anchor")
ax.set_yticks(range(len(genes)))
ax.set_yticklabels(genes[::-1], fontsize=8)
ax.set_xlim(-.6, len(types) - .4)
ax.set_ylim(-.6, len(genes) - .4)
sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(0, vmax))
cb = fig.colorbar(sm, ax=ax, pad=.01)
cb.set_label("mean log-normalised expression", fontsize=7)
cb.ax.tick_params(labelsize=7)
ax.set_title("Part I shortlist genes by cell type (dot size = share of cells with the gene detected)", fontsize=8)
plt.tight_layout()
plt.savefig(OUT, dpi=200)
print("saved", OUT)
