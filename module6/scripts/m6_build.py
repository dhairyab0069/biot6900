"""Turn the remote 1000 Genomes pull into the Part 2 data layout (genotypes, variants, score, meta)."""
import gzip, io, os
import pandas as pd

samples = open("samples.txt").read().split()
cols = ["vcf_id", "chr", "pos", "ref", "alt"] + samples
raw = pd.read_csv("geno_raw.tsv", sep="\t", header=None, names=cols, dtype=str)
raw["pos"] = raw.pos.astype(int)
gt = raw[samples]
dos = gt.apply(lambda s: s.str[0].astype(int) + s.str[2].astype(int))   # phased "a|b" -> ALT count

panel = pd.read_csv("integrated_call_samples_v3.20130502.ALL.panel", sep="\t", usecols=[0, 1, 2, 3])
panel.columns = ["sample", "pop", "ancestry", "sex"]
meta = panel.set_index("sample").loc[samples].reset_index()

def read_score(pgs):
    txt = "".join(l for l in gzip.open(f"{pgs}_hmPOS_GRCh37.txt.gz", "rt") if not l.startswith("#"))
    s = pd.read_csv(io.StringIO(txt), sep="\t", dtype=str)
    s = s[s.hm_pos.notna()].copy()
    s["pos"] = s.hm_pos.astype(int)
    return s

for pgs, out in [("PGS004227", "data"), ("PGS002280", "data_grs83")]:
    s = read_score(pgs)
    rows, report = [], []
    for _, v in s.iterrows():
        cand = raw[(raw.chr == v.hm_chr) & (raw.pos == v.pos)]
        alle = {v.effect_allele, v.other_allele}
        hit = cand[[{r, a} == alle for r, a in zip(cand.ref, cand.alt)]]
        if len(hit) == 1:
            rows.append((v.rsID, hit.index[0], v.effect_allele, v.other_allele, float(v.effect_weight)))
        else:
            report.append((v.rsID, v.hm_chr, v.pos, f"{v.effect_allele}/{v.other_allele}",
                           "not in 1000G phase 3" if cand.empty else "alleles differ: " + ",".join(cand.ref + ">" + cand.alt)))
    os.makedirs(out, exist_ok=True)
    names = [r[0] for r in rows]
    geno = pd.DataFrame(dos.loc[[r[1] for r in rows]].to_numpy().T, columns=names)
    variants = pd.DataFrame({"variant": names, "chr": raw.loc[[r[1] for r in rows], "chr"].values,
                             "pos_grch37": raw.loc[[r[1] for r in rows], "pos"].values,
                             "ref": raw.loc[[r[1] for r in rows], "ref"].values,
                             "alt": raw.loc[[r[1] for r in rows], "alt"].values})
    score = pd.DataFrame(rows, columns=["variant", "_i", "effect_allele", "other_allele", "weight"]).drop(columns="_i")
    geno.to_csv(f"{out}/genotypes.csv", index=False)
    variants.to_csv(f"{out}/variants.csv", index=False)
    score.to_csv(f"{out}/score.csv", index=False)
    meta.to_csv(f"{out}/meta.csv", index=False)
    pd.DataFrame(report, columns=["rsid", "chr", "pos_grch37", "alleles", "reason"]).to_csv(f"{out}/unmatched_variants.csv", index=False)
    print(f"{pgs}: score {len(s)} variants, matched {len(rows)}, unmatched {len(report)} -> {out}/")
    for r in report: print("   ", r)
print(meta.ancestry.value_counts().to_string())
