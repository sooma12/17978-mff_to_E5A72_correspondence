# 2_gb_to_fa.py
"""
Make a .fa file from genbank via biopython
Technique comes from https://warwick.ac.uk/fac/sci/moac/people/students/peter_cock/python/genbank2fasta/
NOTE: need to load biopython.  Use `conda activate /work/geisingerlab/conda_env/blast_corr`
"""


from Bio import SeqIO
import os
import sys
import pathlib


def main():
    genbank_dir = get_var_from_config(config_filename="./config.cfg", varname="GENBANK_DIR")
    fasta_dir = get_var_from_config(config_filename="./config.cfg", varname="FASTA_DIR")
    if not os.path.exists(fasta_dir):
        os.makedirs(fasta_dir)

    file_paths = []
    for folder, subs, files in os.walk(genbank_dir):
        for filename in files:
            file_paths.append(os.path.abspath(os.path.join(folder, filename)))

    for input_filepath in file_paths:
        file_base = pathlib.Path(input_filepath).stem
        output_path = os.path.join(fasta_dir, (file_base + '.fa'))
        write_genbank_to_fa(input_filename=input_filepath, output_filename=output_path)


def write_genbank_to_fa(input_filename: str, output_filename: str):
    """
    write the amino acid protein sequences from a genbank file to a fasta file, with locus tags as headers
    """
    input_handle = open(input_filename, 'r')
    output_handle = open(output_filename, 'w')

    for seq_record in SeqIO.parse(input_handle, "genbank"):
        print(f'converting GenBank record {seq_record.id}')
        for seq_feature in seq_record.features:
            if seq_feature.type == "CDS":
                if 'pseudo' not in seq_feature.qualifiers.keys():  # Skip pseudogenes which are typed "CDS" but lack a translation qualifier
                    assert len(seq_feature.qualifiers['translation']) == 1
                    output_handle.write(
                        f">{seq_feature.qualifiers['locus_tag'][0]} from {seq_record.name}\n{seq_feature.qualifiers['translation'][0]}\n")

    output_handle.close()
    input_handle.close()


def get_var_from_config(config_filename: str, varname: str):
    """Open config file and get specified variable.
    Assumes config file is formatted with one variable per line, e.g. `VARNAME=VARVALUE`
    """

    target_var = None

    with open(config_filename, 'r') as config_fh:
        for line in config_fh:
            if line.startswith(varname):
                line = line.strip()
                if target_var:
                    print("Error in config parsing: variable occurs more than once.")
                    sys.exit(1)
                split_line = line.split(sep='=')
                target_var = split_line[1]

    return target_var


if __name__ == "__main__":
    main()
