"""Report figure for Module 5: why the pooled CADD calibration cannot be trusted for CYP2C19.

Run from the repository root:  python module5/scripts/make_figures.py
Reads the MyVariant.info caches in module5/data/ (written by the notebook on its first run) and
repeats the notebook's own labelling and frequency filter, so the counts match the report.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
M5 = ROOT / "module5"
OUT = M5 / "figures"
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED = "#0b0b0b", "#52514e"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8985"
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 220, "font.size": 9, "font.family": "Arial",
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.titleweight": "bold",
                     "axes.titlesize": 10, "axes.titlelocation": "left"})
MAX_AF = 0.5
BANDS = [(0, 20, "strong, benign", "#dcebf9"), (20, 25, "none", "#f2f1ee"),
         (25, 30, "moderate,\npathogenic", "#fbe3d6"), (30, 50, "strong, pathogenic", "#f7cdb5")]
NO_FUNCTION = {"rs4244285": "*2", "rs4986893": "*3", "rs28399504": "*4", "rs56337013": "*5",
               "rs72552267": "*6", "rs41291556": "*8"}


def clinvar_label(sig):          # same rules as the notebook
    if not isinstance(sig, str): return "none"
    s = sig.lower()
    if "conflict" in s: return "conflicting"
    if "pathogenic" in s and "non-pathogenic" not in s: return "P/LP"
    if "benign" in s: return "B/LB"
    if "uncertain" in s: return "VUS"
    return "other"


def load(gene):
    d = pd.read_csv(M5 / f"data/{gene}.tsv", sep="\t")
    for c in ("cadd_phred", "gnomad_af"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["label"] = d.clinvar_sig.map(clinvar_label)
    return d[d.gnomad_af.isna() | (d.gnomad_af <= MAX_AF)].assign(source=gene)


def fig_calibration():
    G, P2 = load("CYP2C19"), load("DPYD")
    pool = pd.concat([G, P2], ignore_index=True)
    lab = pool[pool.label.isin(["P/LP", "B/LB"]) & pool.cadd_phred.notna()]
    benign, path = lab[lab.label == "B/LB"].cadd_phred, lab[lab.label == "P/LP"].cadd_phred
    vus = G[(G.label == "VUS") & G.cadd_phred.notna()].cadd_phred
    nf = (G[G.rsid.isin(NO_FUNCTION) & G.cadd_phred.notna()].sort_values("cadd_phred")
            .drop_duplicates("rsid", keep="last"))

    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    for lo, hi, name, color in BANDS:
        ax.axvspan(lo, hi, color=color, zorder=0)
        ax.text((lo + hi) / 2, 3.42, name, ha="center", va="bottom", fontsize=7, color=MUTED)
    rng = np.random.default_rng(0)
    rows = [(f"Benign, both genes (n = {len(benign)})", benign, BLUE),
            (f"Pathogenic, all DPYD (n = {len(path)})", path, ORANGE),
            (f"CYP2C19 VUS with a CADD score (n = {len(vus)})", vus, GREY)]
    for y, (name, vals, color) in zip([3, 2, 1], rows):
        ax.scatter(vals, y + rng.uniform(-0.22, 0.22, len(vals)), s=14, color=color, alpha=0.75,
                   edgecolor="white", linewidth=0.5, zorder=3)
    ax.scatter(nf.cadd_phred, np.zeros(len(nf)), marker="D", s=34, color=INK, zorder=4)
    for i, (_, r) in enumerate(nf.iterrows()):
        ax.annotate(NO_FUNCTION[r.rsid], (r.cadd_phred, 0), xytext=(0, 7 if i % 2 == 0 else -12),
                    textcoords="offset points", ha="center", fontsize=7.5, color=INK)
    ax.set_yticks([3, 2, 1, 0])
    ax.set_yticklabels([r[0] for r in rows] + ["CYP2C19 no-function star alleles"], fontsize=8)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.6, 3.95); ax.set_xlim(0, 50)
    ax.set_xlabel("CADD phred score")
    ax.set_title("Pooled CADD bands put CYP2C19*2 and *4 in the benign zone")
    fig.savefig(OUT / "fig_cadd_calibration.png", bbox_inches="tight"); plt.close(fig)
    print(f"labelled: P/LP {len(path)}, B/LB {len(benign)}; VUS scored {len(vus)}; star alleles {len(nf)}")


if __name__ == "__main__":
    fig_calibration()
    print("saved to", OUT)
