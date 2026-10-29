"""Report figures for Module 2, re-plotted from targets_ad_full.csv (no new analysis).

Run from the repository root:  python module2/scripts/make_figures.py
Figures 1 and 2 use the same plotting code as Portfolio Deliverable 1.
"""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "portfolio1"))
import make_figures as pf   # shared style, integration scatter and Venn diagrams

OUT = ROOT / "module2" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
pf.OUT = OUT


def fig_top15():
    """Each top-15 gene's score split into its three equal-weight layer ranks."""
    full = pd.read_csv(ROOT / "module2/targets_ad_full.csv")
    parts = pd.DataFrame({"RNA": full.rna_lfc.abs().rank(pct=True),
                          "Protein": full.prot_lfc.abs().rank(pct=True),
                          "GWAS": full.neglog10p.rank(pct=True)}) / 3
    parts["gene"] = full.gene
    t = parts.loc[full["rank"] <= 15].iloc[::-1]
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    left = 0
    for col, color in [("RNA", pf.BLUE), ("Protein", pf.ORANGE), ("GWAS", pf.AQUA)]:
        ax.barh(t.gene, t[col], left=left, color=color, edgecolor="white", linewidth=1.5, height=0.7, label=col)
        left = left + t[col]
    for y, total in enumerate(left):
        ax.text(total + 0.008, y, f"{total:.3f}", va="center", fontsize=7, color=pf.MUTED)
    ax.set_xlim(0, 1.08)
    ax.set_xlabel("Score = mean of the three layer ranks (each rank 0–1, weight 1/3)")
    ax.set_title("Top 15 genes: how much each layer contributes")
    ax.legend(frameon=False, fontsize=7.5, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.13))
    ax.tick_params(axis="y", length=0)
    fig.savefig(OUT / "fig3_top15.png", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    pf.fig_integration()
    pf.fig_venn()
    fig_top15()
    print("saved to", OUT)
