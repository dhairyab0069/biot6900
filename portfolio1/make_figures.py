"""Figures for Portfolio Deliverable 1, made from Module 2-4 outputs (no new analysis).

Run from the repository root:  python portfolio1/make_figures.py
Needs module4/structures/ (downloaded by the Module 4 notebook) for the structure figure.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "portfolio1" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 220, "font.size": 9, "font.family": "Arial",
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.titleweight": "bold",
                     "axes.titlesize": 10, "axes.titlelocation": "left"})

rna = pd.read_csv(ROOT / "module2/data/ad_transcriptomics.tsv", sep="\t")
prot = pd.read_csv(ROOT / "module2/data/ad_proteomics.tsv", sep="\t")
gwas = pd.read_csv(ROOT / "module2/data/ad_gwas.tsv", sep="\t")
full = pd.read_csv(ROOT / "module2/targets_ad_full.csv")
top = pd.read_csv(ROOT / "module2/targets_ad.csv")


# ---------- Figure 1: multi-omics integration (RNA vs protein, sized by GWAS) ----------
def fig_integration():
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    size = 6 + 4 * np.clip(full.neglog10p, 0, 60) ** 0.8
    for conc, color, lab in [(True, BLUE, "Concordant (same direction)"), (False, ORANGE, "Discordant")]:
        d = full[full.concordant == conc]
        ax.scatter(d.rna_lfc, d.prot_lfc, s=size[d.index], color=color, alpha=0.35, edgecolor="none",
                   label=f"{lab}: {len(d):,} genes")
    t = top.set_index("gene")
    ax.scatter(t.rna_lfc, t.prot_lfc, s=40, facecolor="none", edgecolor=INK, linewidth=1.1, zorder=3)
    # label positions in data units, with leader lines, so crowded labels do not overlap
    place = {"APOE": (0.10, 0.26), "APOB": (0.28, 0.33), "PLEC": (0.48, 0.40), "HLA-DRB1": (0.60, 0.33),
             "ITGAX": (0.78, 0.40), "HLA-DRA": (0.95, 0.35), "GMPR": (1.12, 0.29), "APLNR": (1.30, 0.17),
             "PECAM1": (1.02, 0.02), "MOG": (0.26, -0.20), "MTSS2": (0.80, -0.20), "APOC1": (0.62, -0.28),
             "NRXN3": (-0.55, 0.16), "SHANK2": (-0.45, -0.16), "RPH3A": (-1.05, -0.24)}
    for g, r in t.iterrows():
        ax.annotate(g, (r.rna_lfc, r.prot_lfc), xytext=place[g], textcoords="data", fontsize=7, color=INK,
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6, shrinkA=0, shrinkB=3))
    ax.set_ylim(-0.32, 0.46)
    n_out = int(((full.prot_lfc > 0.46) | (full.prot_lfc < -0.32)).sum())
    ax.axhline(0, color=GRID, lw=1, zorder=0); ax.axvline(0, color=GRID, lw=1, zorder=0)
    ax.set_xlabel("RNA log2 fold change, AD vs control (AMP-AD, strongest region)")
    ax.set_ylabel("Protein log2 fold change (DLPFC, TMT)")
    ax.set_title("Multi-omics integration of 1,115 genes measured in all three layers")
    leg = ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax.text(0, -0.17, f"Dot size: GWAS strength (−log10 p). Circled: the 15 top-ranked targets. "
            f"{n_out} genes with larger protein changes lie outside the axis.",
            transform=ax.transAxes, fontsize=7, color=MUTED)
    fig.savefig(OUT / "fig1_integration.png", bbox_inches="tight"); plt.close(fig)


# ---------- Figure 2: Venn diagrams (coverage and evidence) ----------
def venn3(ax, sets, names, colors, title):
    A, B, C = sets
    regions = {"100": len(A - B - C), "010": len(B - A - C), "001": len(C - A - B),
               "110": len(A & B - C), "101": len(A & C - B), "011": len(B & C - A), "111": len(A & B & C)}
    centers = [(-0.55, 0.32), (0.55, 0.32), (0, -0.62)]
    for (x, y), c in zip(centers, colors):
        ax.add_patch(Circle((x, y), 1.0, facecolor=c, alpha=0.18, edgecolor=c, linewidth=1.5))
    pos = {"100": (-1.0, 0.6), "010": (1.0, 0.6), "001": (0, -1.15), "110": (0, 0.78),
           "101": (-0.62, -0.38), "011": (0.62, -0.38), "111": (0, 0.0)}
    for k, (x, y) in pos.items():
        ax.text(x, y, f"{regions[k]:,}", ha="center", va="center", fontsize=8.5,
                fontweight="bold" if k == "111" else "normal", color=INK)
    for (x, y), n, c, s in zip([(-1.25, 1.45), (1.25, 1.45), (0, -1.85)], names, colors, sets):
        ax.text(x, y, f"{n}\n({len(s):,})", ha="center", va="center", fontsize=8, color=INK)
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-2.15, 1.85); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=9)
    return regions["111"]


def fig_venn():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.7))
    cov = [set(rna.gene), set(prot.gene), set(gwas.gene)]
    n1 = venn3(axes[0], cov, ["RNA measured", "Protein measured", "GWAS association"],
               [BLUE, ORANGE, AQUA], "A. Coverage: genes present in each layer")
    sig = [set(rna.gene[rna.pval < 0.05]), set(prot.gene[prot.pval < 0.05]),
           set(gwas.gene[gwas.neglog10p >= -np.log10(5e-8)])]
    n2 = venn3(axes[1], sig, ["RNA adj. p < 0.05", "Protein adj. p < 0.05", "GWAS p < 5e-8"],
               [BLUE, ORANGE, AQUA], "B. Evidence: genes significant in each layer")
    fig.text(0.01, 0.01, f"A: the inner join keeps the {n1:,} genes in the centre. B: {n2} genes pass all three "
             "significance thresholds at once.", fontsize=7, color=MUTED)
    fig.savefig(OUT / "fig2_venn.png", bbox_inches="tight"); plt.close(fig)
    return n1, n2


# ---------- Figure 4: predicted structures coloured by pLDDT, with pockets ----------
PLDDT_BINS = [(90, "#0053d6", "> 90 very high"), (70, "#65cbf3", "70–90 confident"),
              (50, "#ffdb13", "50–70 low"), (0, "#ff7d45", "< 50 very low")]


def read_ca(pdb):
    xyz, b, res = [], [], []
    for line in open(pdb):
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            xyz.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            b.append(float(line[60:66])); res.append(int(line[22:26]))
    return np.array(xyz), np.array(b), np.array(res)


def read_pockets(out_pdb, ids):
    pts = {i: [] for i in ids}
    for line in open(out_pdb):
        if line.startswith("HETATM") and line[17:20] == "STP":
            pid = int(line[22:26])
            if pid in pts:
                pts[pid].append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return {k: np.array(v) for k, v in pts.items() if v}


def color_of(p):
    return next(c for t, c, _ in PLDDT_BINS if p > t or t == 0)


def draw_structure(ax, uni, pockets, title):
    """pockets: list of (fpocket id, label, colour, label offset in points)."""
    s = ROOT / "module4/structures"
    xyz, plddt, _ = read_ca(s / f"AF-{uni}.pdb")
    centre = xyz.mean(0)
    _, _, vt = np.linalg.svd(xyz - centre, full_matrices=False)      # view along the two widest axes
    proj = lambda p: (p - centre) @ vt[:2].T
    p2 = proj(xyz)
    segs = np.stack([p2[:-1], p2[1:]], axis=1)
    ax.add_collection(LineCollection(segs, colors=[color_of(v) for v in plddt[:-1]], linewidths=1.3))
    pk = read_pockets(s / f"AF-{uni}_out" / f"AF-{uni}_out.pdb", [p[0] for p in pockets])
    for pid, label, col, off in pockets:
        if pid in pk:
            q = proj(pk[pid])
            ax.scatter(q[:, 0], q[:, 1], s=14, color=col, edgecolor="white", linewidth=0.3, zorder=3)
            cx, cy = q.mean(0)
            ax.annotate(label, (cx, cy), xytext=off, textcoords="offset points", fontsize=7.5, color=INK,
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.autoscale(); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=9)


def fig_structures():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.4), gridspec_kw={"width_ratios": [1.25, 1]})
    draw_structure(axes[0], "P20702",
                   [(4, "pocket 4 (score 0.49)", "#9a5fc0", (25, -38)), (79, "pocket 79 (score 0.47)", "#e34948", (-70, 45))],
                   "A. ITGAX (AF-P20702), mean pLDDT 88.0")
    draw_structure(axes[1], "P35414",
                   [(9, "pocket 9: top score (0.30)", "#e34948", (5, -45)), (2, "pocket 2: real drug site (8EH)", "#9a5fc0", (-95, -70))],
                   "B. APLNR (AF-P35414), mean pLDDT 81.7")
    handles = [plt.Line2D([], [], color=c, lw=3) for _, c, _ in PLDDT_BINS]
    fig.legend(handles, [l for _, _, l in PLDDT_BINS], loc="lower center", ncol=4, frameon=False, fontsize=7.5,
               title="pLDDT (AlphaFold confidence)", title_fontsize=7.5, bbox_to_anchor=(0.5, -0.04))
    fig.savefig(OUT / "fig4_structures.png", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_integration()
    print("venn centre counts:", fig_venn())
    fig_structures()
    print("saved to", OUT)
