"""Fetch the public evidence for my Module 7 knowledge graph from the Open Targets Platform API.

Run from module7/:  python scripts/build_kg_data.py
Starts from my own top 15 Alzheimer's genes (../module2/targets_ad.csv) and writes, to kg_data/:
  genes.csv        Ensembl id and Open Targets association score with Alzheimer's disease
  pathways.csv     Reactome pathways for each gene
  drugs.csv        drugs and clinical candidates acting on each gene, with their furthest stage
  related.csv      association scores of my genes with candidate related diseases (the two best are used)
  phenotypes.csv   HPO phenotypes of Alzheimer's and of the chosen related diseases
No key is needed. Everything here is public, gene- or disease-level data.
"""
import json
import time
from pathlib import Path

import pandas as pd
import requests

URL = "https://api.platform.opentargets.org/api/v4/graphql"
HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "kg_data"
OUT.mkdir(exist_ok=True)
AD = "MONDO_0004975"
# diseases that could share genes or symptoms with Alzheimer's; the two sharing most of my genes are kept
CANDIDATES = {"MONDO_0005180": "Parkinson disease", "MONDO_0017276": "frontotemporal dementia",
              "MONDO_0005301": "multiple sclerosis", "EFO_0001645": "coronary artery disease",
              "MONDO_0004976": "amyotrophic lateral sclerosis", "MONDO_0005090": "schizophrenia"}
STAGE_ORDER = ["APPROVAL", "PREAPPROVAL", "PHASE_4", "PHASE_3", "PHASE_2_3", "PHASE_2", "PHASE_1_2", "PHASE_1", "EARLY_PHASE_1", "UNKNOWN"]


def q(query, **variables):
    for attempt in range(4):
        r = requests.post(URL, json={"query": query, "variables": variables}, timeout=90)
        if r.status_code == 200 and "errors" not in r.json():
            return r.json()["data"]
        time.sleep(2 + attempt * 3)
    raise RuntimeError(f"Open Targets query failed: {r.status_code} {r.text[:300]}")


top = pd.read_csv(HERE.parent / "module2" / "targets_ad.csv")
genes = []
for sym in top["gene"]:
    hits = q('query($s:String!){ search(queryString:$s, entityNames:["target"], page:{index:0,size:5}){ hits{ id name } } }', s=sym)["search"]["hits"]
    hit = next((h for h in hits if h["name"] == sym), hits[0])
    genes.append({"gene": sym, "ensembl": hit["id"]})
genes = pd.DataFrame(genes)
ids = genes["ensembl"].tolist()

def scores(efo):
    d = q('query($e:String!,$b:[String!]){ disease(efoId:$e){ name associatedTargets(Bs:$b, page:{index:0,size:100}){ rows{ target{ id } score } } } }', e=efo, b=ids)["disease"]
    if d is None:
        print("  skipped, not found in Open Targets:", efo); return None, {}
    return d["name"], {r["target"]["id"]: r["score"] for r in d["associatedTargets"]["rows"]}

ad_name, ad = scores(AD)
genes["ot_ad_score"] = genes["ensembl"].map(ad).round(3)
genes.to_csv(OUT / "genes.csv", index=False)

rel = []
for efo in CANDIDATES:
    name, sc = scores(efo)
    if name is None: continue
    for gid, s in sc.items():
        rel.append({"disease_id": efo, "disease": name, "gene": genes.set_index("ensembl").loc[gid, "gene"], "score": round(s, 3)})
rel = pd.DataFrame(rel)
rel.to_csv(OUT / "related.csv", index=False)
shared = rel[rel.score >= 0.1].groupby(["disease_id", "disease"]).gene.nunique().sort_values(ascending=False)
chosen = shared[shared >= 2].head(2)
print("related diseases by shared genes (score >= 0.1):\n", shared.to_string())

paths, drugs = [], []
for g in genes.itertuples():
    t = q('query($id:String!){ target(ensemblId:$id){ pathways{ pathway pathwayId topLevelTerm } '
          'drugAndClinicalCandidates{ rows{ maxClinicalStage drug{ name drugType } diseases{ disease{ id name } } } } } }', id=g.ensembl)["target"]
    for p in t["pathways"] or []:
        paths.append({"gene": g.gene, "pathway": p["pathway"], "pathway_id": p["pathwayId"], "top_level": p["topLevelTerm"]})
    for row in (t["drugAndClinicalCandidates"] or {}).get("rows", []):
        inds = [d["disease"] for d in row["diseases"] if d.get("disease")]
        drugs.append({"gene": g.gene, "drug": row["drug"]["name"], "drug_type": row["drug"]["drugType"],
                      "stage": row["maxClinicalStage"], "indications": json.dumps(sorted({d["name"] for d in inds})),
                      "indication_ids": json.dumps(sorted({d["id"] for d in inds}))})
pd.DataFrame(paths).drop_duplicates().to_csv(OUT / "pathways.csv", index=False)
pd.DataFrame(drugs).drop_duplicates(["gene", "drug"]).to_csv(OUT / "drugs.csv", index=False)

phen = []
for efo, name in [(AD, ad_name)] + list(chosen.index):
    rows = q('query($e:String!){ disease(efoId:$e){ phenotypes(page:{index:0,size:200}){ rows{ phenotypeHPO{ id name } } } } }', e=efo)["disease"]["phenotypes"]["rows"]
    for r in rows:
        h = r["phenotypeHPO"]
        if h and not any(w in h["name"].lower() for w in ("inheritance", "onset", "heterogeneity", "penetrance")):
            phen.append({"disease_id": efo, "disease": name, "phenotype": h["name"], "hpo": h["id"]})
pd.DataFrame(phen).drop_duplicates().to_csv(OUT / "phenotypes.csv", index=False)
json.dump({"alzheimers": [AD, ad_name], "related": [list(i) for i in chosen.index]}, open(OUT / "diseases.json", "w"), indent=1)
print("written:", sorted(p.name for p in OUT.iterdir()))
