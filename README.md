# Correspondence table construction: ATCC 17978-mff -> E5A72 locus tags
For linking 17978-mff locus tags to the biocyc genome

Link to biocyc genome: https://www.ncbi.nlm.nih.gov/nuccore/1729865701

- Parse CP039025.2, CP039024.1, CP039026.1 genbank files with Biopython -> get locus tags and protein sequences -> join into one
- Make 17978-mff BLAST database
- BLAST protein sequences from biocyc genome vs. 17978-mff to get best hits; grab those locus tags
- Associate locus tags together

## Setup

Creating conda environment for fetching genbank files and BLAST:
```bash
srun --partition=express --nodes=1 --cpus-per-task=2 --pty --time=00:60:00 /bin/bash
module load anaconda3
conda create --prefix /work/geisingerlab/conda_env/blast_corr python=3.9
conda activate /work/geisingerlab/conda_env/blast_corr
conda install -p /work/geisingerlab/conda_env/blast_corr entrez-direct
conda install -p /work/geisingerlab/conda_env/blast_corr gffread
conda install -p /work/geisingerlab/conda_env/blast_corr samtools
conda install -p /work/geisingerlab/conda_env/blast_corr blast
conda install -p /work/geisingerlab/conda_env/blast_corr ncbi-datasets-cli
conda install -p /work/geisingerlab/conda_env/blast_corr biopython
```

python venv for biopython:
```bash
PROJECT_DIR=/work/geisingerlab/Mark/correspondence_tables_17978/correspondence_17978-17961
python3 -m venv $PROJECT_DIR/venv
source $PROJECT_DIR/venv/bin/activate
which python  # verify that this points to the venv python


python3 -m pip freeze
deactivate
```

##  Get sequences


## BLAST

To format:
- Wrote a "first_line.txt" file containing tab-separated info about blast outfmt6
- concatenated first_line.txt and the 3 blast output files