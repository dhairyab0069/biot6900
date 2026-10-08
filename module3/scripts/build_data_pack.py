"""Build the Module 3 data pack in data/ from public sources.

Stages (run all with no arguments, or one stage by name):
  tables      UniProt + Open Targets + HGNC  ->  panel.tsv, proteome.tsv
  embed       ESM C 300M (main) and ESM-2 35M (baseline) mean-pooled embeddings
  variants    ESM-2 650M masked-marginal scores for TP53, APOE, TREM2 -> variant_scores_*.tsv, anchor_variants.tsv
  manifest    manifest.json

Inputs are cached in .cache/. The proteome table covers the training panel plus every gene in the
Module 2 full ranked list (../module2/targets_ad_full.csv) that has a reviewed UniProt entry.
"""
import glob
import json
import os
import sys
import time
import urllib.request

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data_student_built")   # kept separate from the official course pack in data/
CACHE = os.path.join(REPO, ".cache")
MODULE2 = os.path.join(os.path.dirname(REPO), "module2", "targets_ad_full.csv")
SEED = 6900
PANEL_POS, PANEL_NEG = 400, 800          # about 1,200 proteins, one third with clinical precedence
CLINICAL = {"Approved Drug", "Advanced Clinical", "Phase 1 Clinical"}
ANCHOR_GENES = ["TP53", "APOE", "TREM2"]

UNIPROT = ("https://rest.uniprot.org/uniprotkb/search?format=tsv&size=500"
           "&fields=accession,gene_primary,protein_name,length,protein_families,cc_subcellular_location,sequence"
           "&query=%28organism_id%3A9606%29%20AND%20%28reviewed%3Atrue%29")
OT = "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/target_tractability/"
HGNC = "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt"

# (gene, UniProt-numbered variant, note)
ANCHORS = [
    ("TP53", "R175H", "cancer hotspot (DNA-binding domain, structural)"),
    ("TP53", "Y220C", "cancer hotspot (creates a druggable surface pocket)"),
    ("TP53", "G245S", "cancer hotspot (L3 loop, structural)"),
    ("TP53", "R248Q", "cancer hotspot (DNA contact)"),
    ("TP53", "R249S", "cancer hotspot (aflatoxin signature, structural)"),
    ("TP53", "R273H", "cancer hotspot (DNA contact)"),
    ("TP53", "R282W", "cancer hotspot (structural)"),
    ("APOE", "R176C", "rs7412, defines APOE e2 (mature numbering R158C); protective for AD"),
    ("APOE", "C130R", "rs429358, defines APOE e4 (mature numbering C112R); strongest common AD risk allele"),
    ("TREM2", "R47H", "rs75932628, rare AD risk variant (about 2-4x risk); impairs ligand binding"),
]


def fetch(url, name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        print(f"  downloading {name} ...")
        urllib.request.urlretrieve(url, path + ".part")
        os.rename(path + ".part", path)
    return path


def fetch_uniprot():
    # The UniProt /stream endpoint stalled on this connection, so page through /search instead.
    import gzip
    import re
    import requests
    path = os.path.join(CACHE, "uniprot_human.tsv.gz")
    if os.path.exists(path):
        return path
    print("  downloading UniProt reviewed human proteome (paged) ...")
    url, header, lines = UNIPROT, None, []
    while url:
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        text = r.text.splitlines()
        header, lines = text[0], lines + text[1:]
        m = re.search(r'<([^>]+)>; rel="next"', r.headers.get("Link", ""))
        url = m.group(1) if m else None
    os.makedirs(CACHE, exist_ok=True)
    with gzip.open(path, "wt") as f:
        f.write("\n".join([header] + lines) + "\n")
    return path


def load_uniprot():
    up = pd.read_csv(fetch_uniprot(), sep="\t", compression="gzip")
    up.columns = ["uniprot", "gene", "protein_name", "length", "protein_families", "subcellular_location", "sequence"]
    up = up.dropna(subset=["gene"])
    up["gene"] = up["gene"].str.strip().str.upper()
    # One entry per gene symbol: keep the longest (canonical) entry.
    up = up.sort_values("length", ascending=False).drop_duplicates("gene").reset_index(drop=True)
    return up


def family_group(fams, gene):
    # Use the broadest level UniProt gives ("Protein kinase superfamily", "G-protein coupled receptor 1 family")
    # so that a family split also holds out close relatives in sibling subfamilies.
    if isinstance(fams, str) and fams.strip():
        return fams.split(";")[0].split(",")[0].strip()
    return f"singleton:{gene}"


def load_labels():
    files = []
    for part in sorted(set(__import__("re").findall(r'href="(part-[^"]+\.parquet)"',
                                                   urllib.request.urlopen(OT, timeout=120).read().decode()))):
        files.append(fetch(OT + part, "tract_" + part))
    tr = pd.concat(pd.read_parquet(f) for f in files)
    tr = tr[tr["category"].isin(CLINICAL) & tr["value"].astype(bool)]
    by_mod = tr.groupby("targetId")["modality"].agg(set)
    hgnc = pd.read_csv(fetch(HGNC, "hgnc.tsv"), sep="\t", usecols=["symbol", "ensembl_gene_id"], low_memory=False)
    ens2sym = dict(zip(hgnc.ensembl_gene_id, hgnc.symbol.str.upper()))
    lab = pd.DataFrame({"gene": [ens2sym.get(e) for e in by_mod.index],
                        "sm_clinical": ["SM" in m for m in by_mod],
                        "ab_clinical": ["AB" in m for m in by_mod],
                        "any_clinical": True}).dropna(subset=["gene"])
    return lab.groupby("gene").any().reset_index()


def stage_tables():
    os.makedirs(DATA, exist_ok=True)
    up = load_uniprot()
    up["family_group"] = [family_group(f, g) for f, g in zip(up.protein_families, up.gene)]
    lab = load_labels()
    up = up.merge(lab, on="gene", how="left")
    for c in ["sm_clinical", "ab_clinical", "any_clinical"]:
        up[c] = up[c].fillna(False).astype(bool)
    print(f"  UniProt reviewed human genes: {len(up):,}; with clinical precedence: {up.any_clinical.sum():,}")

    # Enriched, labelled training panel. Anchor genes are always included.
    rng = np.random.default_rng(SEED)
    anchors = up[up.gene.isin(ANCHOR_GENES)]
    rest = up[~up.gene.isin(ANCHOR_GENES)]
    pos = rest[rest.any_clinical]
    neg = rest[~rest.any_clinical]
    pos = pos.iloc[rng.choice(len(pos), PANEL_POS - anchors.any_clinical.sum(), replace=False)]
    neg = neg.iloc[rng.choice(len(neg), PANEL_NEG - (~anchors.any_clinical).sum(), replace=False)]
    panel = pd.concat([anchors, pos, neg]).sort_values("gene").reset_index(drop=True)

    # Proteome table: panel + every Module 2 gene with a reviewed protein.
    m2 = pd.read_csv(MODULE2)["gene"].astype(str).str.strip().str.upper()
    prot = up[up.gene.isin(set(m2) | set(panel.gene))].sort_values("gene").reset_index(drop=True)

    cols = ["gene", "uniprot", "protein_name", "length", "family_group", "subcellular_location",
            "sm_clinical", "ab_clinical", "any_clinical", "sequence"]
    panel[cols].to_csv(os.path.join(DATA, "panel.tsv"), sep="\t", index=False)
    prot[cols].to_csv(os.path.join(DATA, "proteome.tsv"), sep="\t", index=False)
    print(f"  panel.tsv: {len(panel):,} proteins ({panel.any_clinical.mean():.2f} positive, "
          f"{panel.family_group.nunique()} family groups)")
    print(f"  proteome.tsv: {len(prot):,} proteins ({len(set(m2))} Module 2 genes, "
          f"{len(set(m2) - set(up.gene))} without a reviewed protein)")


# ---------------- embeddings ----------------
def device():
    import torch
    return "mps" if torch.backends.mps.is_available() else "cpu"


def windows(seq, size=1000, step=500):
    # Long proteins are embedded in overlapping windows; residue embeddings are averaged.
    if len(seq) <= size:
        return [(0, seq)]
    starts = list(range(0, len(seq) - size, step)) + [len(seq) - size]
    return [(s, seq[s:s + size]) for s in starts]


def embed_all(seqs, residue_fn, dim):
    out = np.zeros((len(seqs), dim), dtype=np.float32)
    t0 = time.time()
    for i, seq in enumerate(seqs):
        total, count = np.zeros((len(seq), dim), np.float32), np.zeros((len(seq), 1), np.float32)
        for s, w in windows(seq):
            total[s:s + len(w)] += residue_fn(w)
            count[s:s + len(w)] += 1
        out[i] = (total / count).mean(0)
        if (i + 1) % 200 == 0:
            print(f"    {i + 1}/{len(seqs)} ({time.time() - t0:.0f}s)", flush=True)
    return out


def esmc_fn():
    import torch
    from esm.models.esmc import ESMC
    from esm.sdk.api import ESMProtein, LogitsConfig
    model = ESMC.from_pretrained("esmc_300m").to(device()).eval()

    @torch.no_grad()
    def fn(seq):
        t = model.encode(ESMProtein(sequence=seq))
        e = model.logits(t, LogitsConfig(sequence=True, return_embeddings=True)).embeddings
        return e[0, 1:-1].float().cpu().numpy()
    return fn, 960, "EvolutionaryScale/esmc-300m-2024-12"


def esm2_fn(name):
    import torch
    from transformers import AutoTokenizer, EsmModel
    tok = AutoTokenizer.from_pretrained(name)
    model = EsmModel.from_pretrained(name).to(device()).eval()

    @torch.no_grad()
    def fn(seq):
        x = tok(seq, return_tensors="pt").to(device())
        return model(**x).last_hidden_state[0, 1:-1].float().cpu().numpy()
    return fn, model.config.hidden_size, name


def stage_embed():
    panel = pd.read_csv(os.path.join(DATA, "panel.tsv"), sep="\t")
    prot = pd.read_csv(os.path.join(DATA, "proteome.tsv"), sep="\t")
    # Embed each unique gene once, then write rows in table order.
    genes = sorted(set(panel.gene) | set(prot.gene))
    seq = dict(zip(prot.gene, prot.sequence)) | dict(zip(panel.gene, panel.sequence))
    for tag, maker in [("baseline", lambda: esm2_fn("facebook/esm2_t12_35M_UR50D")), ("main", esmc_fn)]:
        if os.path.exists(os.path.join(DATA, f"proteome_emb_{tag}.npy")):
            print(f"  {tag} embeddings already built")
            continue
        print(f"  embedding {len(genes)} proteins ({tag}) ...")
        fn, dim, _ = maker()
        E = embed_all([seq[g] for g in genes], fn, dim)
        idx = {g: i for i, g in enumerate(genes)}
        np.save(os.path.join(DATA, f"panel_emb_{tag}.npy"), E[[idx[g] for g in panel.gene]].astype(np.float16))
        np.save(os.path.join(DATA, f"proteome_emb_{tag}.npy"), E[[idx[g] for g in prot.gene]].astype(np.float16))


# ---------------- variant scores ----------------
def stage_variants():
    import torch
    from transformers import AutoTokenizer, EsmForMaskedLM
    name = "facebook/esm2_t33_650M_UR50D"
    tok = AutoTokenizer.from_pretrained(name)
    # Half precision keeps the 650M model inside 8 GB of unified memory on an M2 laptop.
    model = EsmForMaskedLM.from_pretrained(name, torch_dtype=torch.float16).to(device()).eval()
    aas = list("ACDEFGHIKLMNPQRSTVWY")
    aa_ids = tok.convert_tokens_to_ids(aas)
    prot = pd.read_csv(os.path.join(DATA, "proteome.tsv"), sep="\t").set_index("gene")

    rows_all = []
    for gene in ANCHOR_GENES:
        seq = prot.loc[gene, "sequence"]
        ids = tok(seq, return_tensors="pt")["input_ids"][0]
        L = len(seq)
        logp = np.zeros((L, 20), np.float32)
        with torch.no_grad():
            for b in range(0, L, 8):        # masked marginals: mask each position in turn
                pos = list(range(b, min(L, b + 8)))
                batch = ids.repeat(len(pos), 1)
                for k, p in enumerate(pos):
                    batch[k, p + 1] = tok.mask_token_id
                out = model(input_ids=batch.to(device())).logits.float().log_softmax(-1).cpu()
                for k, p in enumerate(pos):
                    logp[p] = out[k, p + 1, aa_ids].numpy()
                if b % 80 == 0:
                    print(f"    {gene}: position {b}/{L}", flush=True)
        rows = []
        for p, wt in enumerate(seq):
            if wt not in aas:
                continue
            for j, mt in enumerate(aas):
                if mt != wt:
                    rows.append((gene, p + 1, wt, mt, f"{wt}{p + 1}{mt}", logp[p, j] - logp[p, aas.index(wt)]))
        v = pd.DataFrame(rows, columns=["gene", "position", "wt", "mut", "variant", "score"])
        v["percentile_in_protein"] = v["score"].rank(pct=True) * 100
        v.to_csv(os.path.join(DATA, f"variant_scores_{gene}.tsv"), sep="\t", index=False, float_format="%.4f")
        rows_all.append(v)
        print(f"  {gene}: {len(v):,} substitutions scored")

    allv = pd.concat(rows_all).set_index(["gene", "variant"])
    anchors = []
    for g, var, note in ANCHORS:
        wt, pos = var[0], int(var[1:-1])
        assert prot.loc[g, "sequence"][pos - 1] == wt, f"{g} {var}: wild-type residue mismatch"
        r = allv.loc[(g, var)]
        anchors.append((g, var, note, r.position, r.score, r.percentile_in_protein))
    pd.DataFrame(anchors, columns=["gene", "variant", "note", "position", "score", "percentile_in_protein"]) \
        .to_csv(os.path.join(DATA, "anchor_variants.tsv"), sep="\t", index=False, float_format="%.4f")


def stage_manifest():
    panel = pd.read_csv(os.path.join(DATA, "panel.tsv"), sep="\t")
    m = {
        "dry_run": False,
        "built": time.strftime("%Y-%m-%d"),
        "built_by": "scripts/build_data_pack.py (student-built; not the instructor data pack)",
        "embedding_models": {
            "main": {"model": "ESM C 300M (EvolutionaryScale/esmc-300m-2024-12)", "dim": 960,
                     "pooling": "mean over residues; proteins >1000 aa in 1000-residue windows, step 500"},
            "baseline": {"model": "ESM-2 35M (facebook/esm2_t12_35M_UR50D)", "dim": 480,
                         "pooling": "same as main"},
        },
        "variant_model": "ESM-2 650M (facebook/esm2_t33_650M_UR50D, float16), masked marginals, "
                         "score = log P(mut) - log P(wt); UniProt numbering (includes signal peptides)",
        "labels": "Open Targets Platform target_tractability (latest release); clinical precedence = "
                  "Approved Drug, Advanced Clinical or Phase 1 Clinical; any_clinical includes SM, AB, PR, OC",
        "family_group": "first (broadest) UniProt 'protein families' term; singleton:<gene> if none",
        "panel": {"n": int(len(panel)), "positive_fraction": round(float(panel.any_clinical.mean()), 3),
                  "seed": SEED},
        "proteome": "training panel + Module 2 AD candidate genes (targets_ad_full.csv) with reviewed UniProt entries",
        "sources": {"uniprot": UNIPROT, "open_targets": OT, "hgnc": HGNC},
    }
    json.dump(m, open(os.path.join(DATA, "manifest.json"), "w"), indent=2)


if __name__ == "__main__":
    stages = {"tables": stage_tables, "embed": stage_embed, "variants": stage_variants, "manifest": stage_manifest}
    for s in (sys.argv[1:] or stages):
        print(f"[{s}]")
        stages[s]()
