#!/bin/bash
# Make blast database for reference genome
# Load conda environment with:
# `module load anaconda3`
# `conda activate /work/geisingerlab/conda_env/blast_corr`

module load anaconda3
source /shared/centos7/anaconda3/2021.05/etc/profile.d/conda.sh
conda activate /work/geisingerlab/conda_env/blast_corr

source ./config.cfg

echo 'Genome fasta files to make blast protein db:' "${REF_FASTAS[@]}"
echo "blast db output directory: $OUT_DIR"
echo "output database name: $OUTPUT_DATABASE"

mkdir -p $OUT_DIR

echo "Merging fastas" "${REF_FASTAS[@]}"
cat "${REF_FASTAS[@]}" > $MERGED_FASTA
echo "Merged fasta saved to $MERGED_FASTA"

makeblastdb -in $MERGED_FASTA -out $OUTPUT_DATABASE -parse_seqids -dbtype prot
