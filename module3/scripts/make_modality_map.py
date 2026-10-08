"""Report figure: small-molecule vs antibody prior for each target.

Reads targets_ad_w3.csv (the notebook's export) and writes modality_map.png.
Usage: python scripts/make_modality_map.py [csv] [out.png]
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "targets_ad_w3.csv")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "modality_map.png")
LOW = 0.1   # below this on both axes counts as "near zero for both"
# Label nudges (points) for genes whose labels collide; anything else goes up and right.
NUDGE = {"APOC1": (8, -9), "HLA-DRA": (8, -4), "HLA-DRB1": (6, 5), "MTSS2": (0, 12, "center"), "GMPR": (6, 7)}

df = pd.read_csv(csv)
low = df[(df.p_sm < LOW) & (df.p_ab < LOW)]
lab = df.drop(low.index)

fig, ax = plt.subplots(figsize=(8.5, 4.3), dpi=150)
ax.grid(color="#e6e6e6", lw=0.8, zorder=0)
ax.plot([0, 1], [0, 1], ls="--", color="#999999", lw=1, zorder=1)
ax.text(0.86, 0.81, "p_sm = p_ab", color="#777777", fontsize=8)
ax.scatter(df.p_sm, df.p_ab, s=45, color="#1f6f8b", edgecolor="white", lw=0.8, zorder=3)
for _, r in lab.iterrows():
    dx, dy, *ha = NUDGE.get(r.gene, (6, 6))
    ax.annotate(r.gene, (r.p_sm, r.p_ab), xytext=(dx, dy), textcoords="offset points",
                fontsize=9, color="#222222", ha=ha[0] if ha else "left")
if len(low):
    ax.text(0.42, 0.24, f"Unlabelled: {len(low)} targets below {LOW} for both\n" + ", ".join(low.gene),
            fontsize=8.5, color="#555555")
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.03, 1.02)
ax.set_xlabel("P(tractable), small molecule (p_sm)")
ax.set_ylabel("P(tractable), antibody (p_ab)")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(out)
print(f"Wrote {out}")
