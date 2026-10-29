#!/bin/bash
# Pull 1000 Genomes phase 3 (GRCh37) genotypes at the AD PGS variants, by remote tabix query.
set -euo pipefail
module load bcftools/1.21
cd /scratch/bhatia.dh/biot6900_m6
BASE=http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502
curl -s -O $BASE/integrated_call_samples_v3.20130502.ALL.panel
# regions: chr, pos from both scores (GRCh37 harmonized positions)
for id in PGS004227 PGS002280; do
  zcat ${id}_hmPOS_GRCh37.txt.gz | grep -v '^#' | awk -F'\t' 'NR==1{for(i=1;i<=NF;i++)h[$i]=i; next}{print $h["hm_chr"]"\t"$h["hm_pos"]}'
done | grep -v -P '^\t' | sort -u -k1,1V -k2,2n > regions.tsv
wc -l regions.tsv
: > geno_raw.tsv
for c in $(cut -f1 regions.tsv | sort -uV); do
  awk -v c=$c '$1==c' regions.tsv > r_$c.tsv
  bcftools view -R r_$c.tsv $BASE/ALL.chr$c.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz 2>/dev/null \
    | bcftools norm -m- 2>/dev/null \
    | bcftools query -f '%ID\t%CHROM\t%POS\t%REF\t%ALT[\t%GT]\n' >> geno_raw.tsv
  echo "chr$c: $(wc -l < geno_raw.tsv) rows so far"
  rm -f r_$c.tsv
done
bcftools query -l $BASE/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz > samples.txt
rm -f *.tbi
echo DONE
