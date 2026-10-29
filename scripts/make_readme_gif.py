"""README animation: the two AlphaFold models from Module 4, rotating, coloured by pLDDT, with pockets.

Run from the repository root:  python scripts/make_readme_gif.py
Needs module4/structures/ (downloaded by the Module 4 notebook). Writes figures/anim_structures.gif.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d.art3d import Line3DCollection

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "module4/structures"
PLDDT = [(90, "#0053d6"), (70, "#65cbf3"), (50, "#ffdb13"), (0, "#ff7d45")]
plt.rcParams.update({"font.family": "Arial", "font.size": 9})


def color_of(p):
    return next(c for t, c in PLDDT if p > t or t == 0)


def read(uni, pockets):
    xyz, b = [], []
    for l in open(S / f"AF-{uni}.pdb"):
        if l.startswith("ATOM") and l[12:16].strip() == "CA":
            xyz.append([float(l[30:38]), float(l[38:46]), float(l[46:54])]); b.append(float(l[60:66]))
    pk = {i: [] for i in pockets}
    for l in open(S / f"AF-{uni}_out" / f"AF-{uni}_out.pdb"):
        if l.startswith("HETATM") and l[17:20] == "STP" and int(l[22:26]) in pk:
            pk[int(l[22:26])].append([float(l[30:38]), float(l[38:46]), float(l[46:54])])
    xyz = np.array(xyz); c = xyz.mean(0)
    return xyz - c, np.array(b), {k: np.array(v) - c for k, v in pk.items()}


MODELS = [("P20702", "ITGAX · mean pLDDT 88.0", {4: "#9a5fc0", 79: "#e34948"}),
          ("P35414", "APLNR · mean pLDDT 81.7", {2: "#9a5fc0", 9: "#e34948"})]
fig = plt.figure(figsize=(9, 4.2), dpi=100)
axes = []
for k, (uni, title, pockets) in enumerate(MODELS):
    ax = fig.add_subplot(1, 2, k + 1, projection="3d")
    xyz, b, pk = read(uni, pockets)
    segs = np.stack([xyz[:-1], xyz[1:]], axis=1)
    ax.add_collection3d(Line3DCollection(segs, colors=[color_of(v) for v in b[:-1]], linewidths=1.4))
    for pid, col in pockets.items():
        ax.scatter(*pk[pid].T, s=10, color=col, depthshade=False)
    r = np.abs(xyz).max() * 0.8
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-r, r)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("x (Å)", labelpad=-8); ax.set_ylabel("y (Å)", labelpad=-8); ax.set_zlabel("z (Å)", labelpad=-8)
    ax.tick_params(labelsize=6, pad=-3)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor((0.96, 0.97, 0.98)); a.pane.set_edgecolor("#d0d5db")
    ax.set_title(title, fontsize=10, fontweight="bold")
    axes.append(ax)
handles = [plt.Line2D([], [], color=c, lw=3) for _, c in PLDDT] + \
          [plt.Line2D([], [], marker="o", ls="", color=c) for c in ("#9a5fc0", "#e34948")]
fig.legend(handles, ["> 90", "70–90", "50–70", "< 50", "pocket A", "pocket B"], loc="lower center",
           ncol=6, frameon=False, fontsize=8, title="pLDDT (AlphaFold confidence) and fpocket pockets", title_fontsize=8)
fig.subplots_adjust(left=0, right=1, top=0.93, bottom=0.12, wspace=0)


def frame(i):
    for ax in axes:
        ax.view_init(elev=18, azim=-60 + i * 8)
    return axes


FuncAnimation(fig, frame, frames=45).save(ROOT / "figures/anim_structures.gif", writer=PillowWriter(fps=12))
print("wrote figures/anim_structures.gif")
