from Bio import SeqIO
import os, pathlib, sys

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
        output_path = os.path.join(fasta_dir, (file_base + '.fna'))
        extract_gene_loci(genbank_file=input_filepath, output_fasta=output_path)


def extract_gene_loci(genbank_file, output_fasta, feature_type="CDS"):
    """
    Extract gene loci from a GenBank file and write them to a FASTA file.

    :param genbank_file: Input GenBank file path.
    :param output_fasta: Output FASTA file path.
    :param feature_type: Type of feature to extract (default is "CDS").
    """
    with open(genbank_file, "r") as gb_file, open(output_fasta, "w") as fasta_file:
        for record in SeqIO.parse(gb_file, "genbank"):
            for feature in record.features:
                if feature.type == feature_type:
                    # Extract the locus ID (if available) or use feature location
                    locus_id = feature.qualifiers.get('locus_tag', ['unknown_locus'])[0]
                    # Extract the sequence for the feature
                    locus_seq = feature.extract(record.seq)
                    # Write in FASTA format
                    fasta_file.write(f">{locus_id}\n{str(locus_seq)}\n")

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
