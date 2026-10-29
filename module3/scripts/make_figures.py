"""Report figures for Module 3 (the modality map is made by make_modality_map.py).

Run from the repository root:  python module3/scripts/make_figures.py
Reads targets_ad_w3.csv and the course data pack in module3/data/ (not committed).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
M3 = ROOT / "module3"
OUT = M3 / "figures"
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 220, "font.size": 9, "font.family": "Arial",
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.titleweight": "bold",
                     "axes.titlesize": 10, "axes.titlelocation": "left"})


def fig_rerank():
    """Module 2 rank against final rank after adding the tractability prior (w = 0.6)."""
    w3 = pd.read_csv(M3 / "targets_ad_w3.csv")
    m2 = pd.read_csv(M3 / "targets_ad.csv")[["gene", "rank"]].rename(columns={"rank": "m2"})
    d = w3.merge(m2, on="gene")
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    for _, r in d.iterrows():
        move = r.m2 - r["rank"]
        color = BLUE if move > 0 else ORANGE if move < 0 else MUTED
        ax.plot([0, 1], [r.m2, r["rank"]], color=color, lw=2 if abs(move) >= 3 else 1.2,
                marker="o", markersize=4)
        ax.text(-0.04, r.m2, r.gene, ha="right", va="center", fontsize=7.5, color=INK)
        ax.text(1.04, r["rank"], f"{r.gene} ({move:+d})" if move else r.gene,
                ha="left", va="center", fontsize=7.5, color=INK)
    ax.set_ylim(15.7, 0.3); ax.set_xlim(-0.55, 1.6)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Module 2 rank", "Final rank (w = 0.6)"])
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_title("Re-ranking: blue moved up, orange moved down")
    fig.savefig(OUT / "fig_rerank.png", bbox_inches="tight"); plt.close(fig)


def fig_validation():
    """Random against family split (numbers from the assignment notebook, Section 3)."""
    vals = {"AUROC": (0.839, 0.745, 0.500), "Average precision": (0.717, 0.548, 0.333)}
    fig, ax = plt.subplots(figsize=(5.0, 2.8))
    x = np.arange(2)
    for i, (lab, color) in enumerate([("Random split", BLUE), ("Family split", ORANGE)]):
        v = [vals[k][i] for k in vals]
        ax.bar(x + (i - 0.5) * 0.36, v, width=0.34, color=color, edgecolor="white", linewidth=1.5, label=lab)
        for xi, vi in zip(x, v):
            ax.text(xi + (i - 0.5) * 0.36, vi + 0.015, f"{vi:.3f}", ha="center", fontsize=7.5, color=INK)
    for xi, k in zip(x, vals):
        ax.hlines(vals[k][2], xi - 0.4, xi + 0.4, color=MUTED, ls=":", lw=1.2)
        ax.text(xi + 0.41, vals[k][2], "chance", va="center", fontsize=7, color=MUTED)
    ax.set_xticks(x); ax.set_xticklabels(list(vals)); ax.set_ylim(0, 1)
    ax.set_title("The prior on held-out proteins: family split is the honest number")
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.savefig(OUT / "fig_validation.png", bbox_inches="tight"); plt.close(fig)


def fig_variants():
    """Every possible substitution in each protein, with the anchor variants marked."""
    anchors = pd.read_csv(M3 / "data/anchor_variants.tsv", sep="\t")
    show = {"APOE": ["R176C", "C130R"], "TREM2": ["R47H"], "TP53": ["R175H"]}
    names = {"R176C": "ε2 R176C", "C130R": "ε4 C130R", "R47H": "R47H", "R175H": "R175H"}
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.5), sharey=False)
    for ax, (gene, vs) in zip(axes, show.items()):
        v = pd.read_csv(M3 / f"data/variant_scores_{gene}.tsv", sep="\t")
        ax.hist(v.score, bins=50, color="#c9cfd6")
        top = ax.get_ylim()[1]
        for name in vs:
            a = anchors[(anchors.gene == gene) & (anchors.variant == name)].iloc[0]
            ax.axvline(a.score, color=ORANGE, lw=1.4)
            right = a.score > v.score.max() - 4          # near the right edge: label on the left side
            pad = "" if right else " "
            ax.text(a.score + (-0.3 if right else 0), top * 0.97,
                    f"{pad}{names[name]}\n{pad}{a.percentile_in_protein:.0f}th pct",
                    fontsize=7, color=INK, va="top", ha="right" if right else "left")
        ax.set_title(gene); ax.set_xlabel("ESM-2 score (mutant − wild type)")
    axes[0].set_ylabel("substitutions")
    fig.tight_layout()
    fig.savefig(OUT / "fig_variants.png", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_rerank(); fig_validation(); fig_variants()
    print("saved to", OUT)
