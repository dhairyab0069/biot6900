---
title: "BIOT 6900 · Module 5: Variant Interpretation on CYP2C19"
author: "Dhairya Bhatia"
geometry: margin=0.7in
fontsize: 10pt
mainfont: Arial
header-includes:
  - \usepackage{booktabs}
  - \usepackage{needspace}
  - \setlength{\parskip}{4pt}
---

**Gene:** CYP2C19, assigned on Canvas. It is a liver enzyme that breaks down, or in the case of clopidogrel activates, many common drugs, including clopidogrel, voriconazole, some antidepressants (SSRIs) and proton-pump inhibitors. **AlphaGenome Atlas:** skipped, because I had no API key (Section 2). All numbers below come from my notebook.

**What came back (Q1):**

- **Count:** 80 ClinVar variants (64 distinct rsIDs).
- **Anchors:** both are present. CYP2C19\*2 (rs4244285) has gnomAD AF 0.168, and \*17 (rs12248560) has AF 0.200.
- **Scores:** CADD covers 68 of 80 variants, REVEL 54, AlphaMissense 54 and gnomAD 55, so none of the columns came back empty.
- **Labels:** 37 "drug response", 33 VUS, 9 benign or likely benign, and **zero pathogenic or likely pathogenic**. That zero shapes everything below.

## 1. Thresholds and calibration

**My frequency threshold: MAX_AF = 0.5.** CYP2C19 is a drug-response gene, not a disease gene. Its reduced-function alleles don't make anyone ill on their own; they only matter when a person takes certain drugs. So nothing keeps them rare, and the most important ones are very common: \*2 at 16.8% and \*17 at 20.0% in my data. A frequency filter here should only remove sites where the "alternate" base is actually the majority base, so I set the cut-off at 0.5.

- **What 0.5 removed:** 2 variants, I331V (AF 0.95) and one synonymous change (AF 0.92). Both are benign, both are the majority allele, and neither is functional.
- **Missing frequencies:** 25 variants have no gnomAD frequency. I kept them as rare. A plain `gnomad_af <= MAX_AF` test would have dropped them silently, because comparisons with missing values come out False.

**The 0.001 contrast:** a rare-disease cut-off would remove 19 variants, **14 of them functional**. It would lose the five best-known star alleles: \*2, \*17, \*3 (W212X), \*4 (M1V) and \*8 (W120R). In other words, it would discard nearly every allele a clinical CYP2C19 test reports.

**Which predictor:** CADD, because it is the only tool that scores non-missense variants. It covered 85% of the gene, against 67.5% for REVEL and AlphaMissense. That matters for this gene because \*2 is synonymous and \*17 is upstream of the gene.

**Calibration was not possible on CYP2C19 alone.** With 0 pathogenic and 5 benign variants that have a CADD score, there is no pathogenic group to compare against. ClinVar files CYP2C19's broken alleles under "drug response" instead of "pathogenic", because they cause no disease. So I took the documented route and **pooled with DPYD**, a gene with many pathogenic variants.

| CADD band | Variants | Pathogenic / benign | LR+ | Evidence |
|---|---:|---:|---:|---|
| 0–10 | 65 | 0 / 65 | 0.00 | strong, benign |
| 10–20 | 24 | 0 / 24 | 0.00 | strong, benign |
| 20–25 | 11 | 5 / 6 | 2.05 | none either way |
| 25–30 | **4** | 3 / 1 | 7.38 | moderate, pathogenic |
| 30–50 | 31 | 31 / 0 | inf | strong, pathogenic |

**How much to trust these numbers:** not much.

- **Sample size:** the calibration rests on 135 labelled variants (39 pathogenic, 96 benign). One band, 25–30, has only 4 variants, so its LR of 7.38 is noise.
- **Empty cells:** the LRs of 0 and infinity come from bands where one group has no variants at all. They mean "none seen", not "perfect evidence".
- **Wrong gene:** all 39 pathogenic variants come from DPYD, so the table really describes how CADD behaves in DPYD.

**I tested whether it transfers to CYP2C19, and it does not.** I placed CYP2C19's own known no-function alleles into the pooled bands:

| Allele | Change | CADD | Pooled band says |
|---|---|---:|---|
| \*2 | synonymous (splicing) | 5.7 | **strong, benign** |
| \*4 | start lost (M1V) | 15.9 | **strong, benign** |
| \*6 | R132Q | 23.0 | no evidence |
| \*8 | W120R | 25.7 | moderate, pathogenic |
| \*5 | R433W | 32.0 | strong, pathogenic |
| \*3 | stop gained (W212X) | 35.0 | strong, pathogenic |
| \*7 | splice donor | none | unscored |

Two of the six scored no-function alleles, including \*2, the most important allele in the gene, sit in a band that calls them "strong, benign". A calibration that calls \*2 benign cannot be used to classify anything else in CYP2C19.

**Classifying the VUS (Q5):**

- **Taken at face value:** the pooled bands would move 16 of the 33 VUS towards benign and none towards pathogenic.
- **After the transfer test:** **I moved none, and all 33 stay VUS.** The 16 "benign" moves come from CADD scores below 20, which is exactly the range where \*2 and \*4 sit.
- **The other 17:** 8 fell in the 20–25 band, which gives no evidence either way. 3 fell in the 4-variant band, which is too small to use. 6 are large deletions that no tool scored.

The CSV keeps both columns: the pooled evidence, and my final call after the transfer test.

## 2. Coverage gaps and the regulatory genome

**Classes no missense tool could score:** REVEL scored zero variants in eight classes, covering 25 variants: large deletions (8), synonymous (7), upstream (5), intergenic, intronic, splice donor, stop gained and stop lost. AlphaMissense also skipped the start-lost variant. CADD scored 14 of these 25. It missed the other 11: the 8 large deletions, which are written as ranges rather than single bases, the splice-donor variant, one synonymous change and one upstream change.

**A specific unscored variant: CYP2C19\*7 (rs72558186, chr10:94781999 T>A).**

- **What it is:** a change at the start of an intron, the "+2" position of a splice donor site, labelled "drug response" in ClinVar.
- **Scores:** CADD, REVEL and AlphaMissense all returned nothing. That means **not scored**, not "benign". Leaving it blank as if harmless would hide one of the gene's no-function alleles.
- **What would classify it:** evidence that it breaks splicing.
  - **SpliceAI** would predict whether the splice site is lost.
  - **An RNA assay** would show it directly. Either an RT-PCR of CYP2C19 messenger RNA from liver tissue of a carrier, or a minigene splicing assay in cells, would reveal whether an exon is skipped or an intron kept.

**The Atlas (skipped, disclosed):** I did not have an AlphaGenome key, so I set `SKIP_ATLAS = True`. My gene has 25 non-missense variants, which is exactly what the Atlas is built for.

- **\*17 (rs12248560):** sits upstream of the gene and *increases* enzyme activity. A regulatory attribution such as DNase, TF ChIP or RNA-seq for \*17 would point to a liver-specific change in how much of the gene is made, the known mechanism.
- **\*2:** a splicing attribution would have confirmed that the Atlas sees its real mechanism, which CADD missed.
- **The 5 upstream and 1 intronic "drug response" variants:** the Atlas could say whether each has a regulatory signal or is just linked to \*2 or \*17.

No other tool in the course looks at regulatory DNA in specific tissues, so this is the one gap I could not fill.

## 3. A discordant variant, read mechanistically: CYP2C19\*2

**Rule it tripped:** "common but functional". gnomAD AF 0.168 is far above 1%, yet ClinVar labels it "drug response", a functional allele.

**What each tool said:**

- **snpEff:** labels it synonymous: the DNA change (c.681G>A) does not change the amino acid at that position.
- **REVEL and AlphaMissense:** no score, because it is not missense.
- **CADD:** 5.7, which is unremarkable.
- **ClinVar:** the most important no-function allele in the gene.

**What would have to be true for both to make sense:** the change must act on **RNA, not protein**. That is the explanation I argue for, and it is the established one. The G>A change creates a new, stronger splice site inside exon 5. The cell's splicing machinery uses it and cuts out the first 40 bases of the exon. That shifts the reading frame, so the protein hits an early stop codon and is never made. So every tool is right about what it measures:

- **snpEff** is right that the codon itself is unchanged.
- **The missense tools** are right that there is no amino-acid change to score.
- **CADD's low score** means its splicing features did not recognise this new site as strong.

The variant is common because it does no harm until someone takes a drug that depends on CYP2C19, so evolution never removed it.

I reject the other explanation, that \*2 is just a passenger linked to some other causal variant, because the 40-base splicing defect has been shown directly in liver RNA.

## 4. What I could not determine, and the one experiment

Two things my analysis cannot tell about \*2:

1. **Zygosity and phase:** I scored variants one at a time. A person's metabolizer status depends on *both* copies of the gene. One copy of \*2 gives an intermediate metabolizer, while two copies, or \*2 with \*3, give a poor metabolizer. Only genotyping both copies, and knowing which variants sit together on each copy, gives the diplotype that CPIC guidance uses.
2. **Modifiers, including phenoconversion:** the same genotype can behave differently in a patient taking a drug that blocks CYP2C19. Omeprazole, a common acid-reflux drug, does this, so a genetically normal person can act like a poor metabolizer. A DNA-only analysis cannot see this.

**My most interesting call:** keeping 16 VUS as VUS instead of moving them to benign. **The single experiment that would settle it:** a multiplexed assay of variant effect (deep mutational scanning) that measures the enzyme activity of every possible CYP2C19 missense change in cells. That would give me CYP2C19's *own* functional labels, so I could calibrate CADD on this gene instead of borrowing DPYD.

**What would change my mind:** if missense variants with CADD below 20 almost all show normal activity in that assay, the benign evidence is real for missense changes, and I would move those 16 VUS towards benign. If a meaningful share of them show reduced activity, keeping them as VUS was right.
