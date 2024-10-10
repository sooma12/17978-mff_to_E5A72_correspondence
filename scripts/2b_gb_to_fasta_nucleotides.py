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
        genbank_to_fasta(input_gb=input_filepath, output_fasta=output_path)

def genbank_to_fasta(input_gb, output_fasta):
    with open(input_gb, "r") as gb_file, open(output_fasta, "w") as fa_file:
        SeqIO.convert(gb_file, "genbank", fa_file, "fasta")

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
