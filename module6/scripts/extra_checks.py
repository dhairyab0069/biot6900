"""Extra checks for the Module 6 report: how much of each group's AUC comes from APOE e4.

Run from module6/:  python scripts/extra_checks.py
Uses the same harmonisation as the notebook, then scores people three ways:
the full score, the score without the two APOE SNPs, and e4 count alone.
Writes figures/fig_auc_apoe.png and prints the numbers used in the report.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

INK, MUTED, BLUE, ORANGE, GREY = "#0b0b0b", "#52514e", "#2a78d6", "#eb6834", "#8a8985"
plt.rcParams.update({"font.family": "Arial", "font.size": 9, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})
POPS = ["EUR", "SAS", "EAS", "AMR", "AFR"]
APOE = ["rs429358", "rs7412"]

geno = pd.read_csv("data/genotypes.csv")
meta = pd.read_csv("data/meta.csv")
score = pd.read_csv("data/score.csv")
vt = pd.read_csv("data/variants.csv").set_index("variant")

snps = list(score["variant"])
G = geno[snps].to_numpy(float)
flip = score["effect_allele"].to_numpy() == vt.loc[snps, "ref"].to_numpy()
G[:, flip] = 2 - G[:, flip]
w = score["weight"].to_numpy()
no_apoe = np.array([s not in APOE for s in snps])

prs = G @ w
meta["prs"] = (prs - prs.mean()) / prs.std()
meta["prs_no_apoe"] = G[:, no_apoe] @ w[no_apoe]
e4 = geno["rs429358"] if vt.loc["rs429358", "alt"] == "C" else 2 - geno["rs429358"]
meta["e4"] = e4

eur = (meta.ancestry == "EUR").to_numpy()
model = LogisticRegression().fit(meta.loc[eur, ["prs"]], meta.loc[eur, "phenotype"])
meta["p_hat"] = model.predict_proba(meta[["prs"]])[:, 1]

rows = []
for pop in POPS:
    m = meta[meta.ancestry == pop]
    rows.append({"ancestry": pop, "n": len(m),
                 "e4_allele_freq": m.e4.mean() / 2,
                 "case_rate": m.phenotype.mean(),
                 "mean_predicted_risk": m.p_hat.mean(),
                 "auc_full": roc_auc_score(m.phenotype, m.prs),
                 "auc_without_apoe": roc_auc_score(m.phenotype, m.prs_no_apoe),
                 "auc_e4_only": roc_auc_score(m.phenotype, m.e4)})
tab = pd.DataFrame(rows)
print(tab.round(3).to_string(index=False))
top = meta.prs > np.quantile(meta.prs, 0.90)
print(f"\nShare of the pooled top 10% who carry at least one e4: {(meta.e4[top] > 0).mean():.2f}")

fig, ax = plt.subplots(figsize=(6.2, 2.9))
x = np.arange(len(POPS)); bw = 0.27
for k, (col, lab, c) in enumerate([("auc_full", "Full score (22 SNPs)", INK),
                                   ("auc_without_apoe", "Without the 2 APOE SNPs", BLUE),
                                   ("auc_e4_only", "APOE e4 count alone", ORANGE)]):
    ax.bar(x + (k - 1) * bw, tab[col], bw, color=c, label=lab)
ax.axhline(0.5, color=GREY, lw=1, ls="--")
ax.text(-0.45, 0.503, "chance", color=GREY, ha="left", va="bottom", fontsize=8)
ax.set_xticks(x, POPS); ax.set_ylim(0.4, 0.7); ax.set_ylabel("AUC (simulated phenotype)")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12), fontsize=8)
fig.savefig("figures/fig_auc_apoe.png", dpi=200, bbox_inches="tight")

# Report figure: the notebook's two figures side by side (left: PRS by ancestry, right: calibration)
from PIL import Image
left, right = Image.open("figures/prs_by_ancestry.png"), Image.open("figures/calibration_by_ancestry.png")
h = max(left.height, right.height)
left = left.resize((round(left.width * h / left.height), h))
right = right.resize((round(right.width * h / right.height), h))
panel = Image.new("RGB", (left.width + right.width + 60, h), "white")
panel.paste(left, (0, 0)); panel.paste(right, (left.width + 60, 0))
panel.save("figures/fig_prs_calibration.png")
