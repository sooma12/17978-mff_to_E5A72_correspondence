#!/bin/bash
# BLAST fasta-formatted proteins against reference genome blast database
# Load conda environment with:
# `module load anaconda3`
# `conda activate /work/geisingerlab/conda_env/blast_corr`

module load anaconda3
source /shared/centos7/anaconda3/2021.05/etc/profile.d/conda.sh
conda activate /work/geisingerlab/conda_env/blast_corr

source ./config.cfg

mkdir -p $BLAST_OUT_PATH

echo "Query fasta files" "${QUERY_FASTAS[@]}"
echo "Blastdb for reference genome: $OUTPUT_DATABASE"
echo "Saving BLAST output to: $BLAST_OUT_PATH"

# Define function.
# 3 arguments: blast_one_fa (ONE QUERY FA) (DATABASE) (OUTPUT)
blast_one_fa () {
  blastp -query $1 -db $2 -max_target_seqs 1 -outfmt 6 -evalue 1e-5 -num_threads 4 1>$3
}

for file in "${QUERY_FASTAS[@]}"; do
  file_base_name=$(basename $file)
  file_root_name=${file_base_name%%.fa}
  blast_one_fa $file $OUTPUT_DATABASE ${BLAST_OUT_PATH}/${file_root_name}.blastout6
done
