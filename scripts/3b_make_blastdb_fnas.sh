#!/bin/bash
# Make blast database for reference genome
# Load conda environment with:
# `module load anaconda3`
# `conda activate /work/geisingerlab/conda_env/blast_corr`

module load anaconda3
source /shared/centos7/anaconda3/2021.05/etc/profile.d/conda.sh
conda activate /work/geisingerlab/conda_env/blast_corr

source ./config.cfg

echo 'Genome fasta files to make blast protein db:' "${REF_FNAS[@]}"
echo "blast db output directory: $OUT_DIR_fna"
echo "output database name: $OUTPUT_DATABASE_FNA"

mkdir -p $OUT_DIR_fna

echo "Merging fastas" "${REF_FNAS[@]}"
cat "${REF_FNAS[@]}" > $MERGED_FNA
echo "Merged fasta saved to $MERGED_FNA"

makeblastdb -in $MERGED_FNA -out $OUTPUT_DATABASE_FNA -parse_seqids -dbtype nucl
