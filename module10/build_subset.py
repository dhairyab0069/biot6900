import numpy as np, os
from medmnist import PathMNIST
NORMAL, TUMOR = 6, 8
def pool(split):
    ds = PathMNIST(split=split, download=True, size=64, root="./data/raw")
    x, y = ds.imgs, ds.labels.squeeze()
    k = np.isin(y, [NORMAL, TUMOR]); return x[k], (y[k] == TUMOR).astype(np.int64)
rng = np.random.default_rng(0)
def sub(x, y, n):
    idx = np.concatenate([rng.permutation(np.where(y == c)[0])[:n] for c in (0, 1)])
    idx = rng.permutation(idx); return x[idx], y[idx]
xtr, ytr = pool("train"); xva, yva = pool("val"); xte, yte = pool("test")
print("pools", len(ytr), len(yva), len(yte))
xtr, ytr = sub(xtr, ytr, 300)
xva, yva = sub(xva, yva, min(200, (yva == 0).sum(), (yva == 1).sum()))
xte, yte = sub(xte, yte, min(300, (yte == 0).sum(), (yte == 1).sum()))
np.savez_compressed("data/pathmnist_tumour_vs_normal_subset.npz", xtr=xtr, ytr=ytr, xva=xva, yva=yva, xte=xte, yte=yte)
print("saved", xtr.shape, xva.shape, xte.shape)
