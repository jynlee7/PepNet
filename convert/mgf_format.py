import os
import glob
from pyteomics import mgf
import pandas as pd

def process_mgf_files(input_directory, output_directory):
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Get all MGF files in the input directory
    mgf_files = glob.glob(os.path.join(input_directory, "*.mgf"))
    
    for mgf_path in mgf_files:
        # Get the base filename
        base_filename = os.path.basename(mgf_path)
        output_path = os.path.join(output_directory, f"pepnet_{base_filename}")

        # Read the MGF file
        with mgf.MGF(mgf_path) as reader:
            spectra = list(reader)
        print(f"Processing {base_filename}: Read {len(spectra)} spectra.")

        # Extract precursor information and create DataFrame
        precursors = [spectrum['params'] for spectrum in spectra]
        df = pd.DataFrame.from_records(precursors)

        # Set 'title' column equal to 'seq' column
        df['title'] = df['seq']

        # Update the spectra with new titles
        for spectrum, (index, row) in zip(spectra, df.iterrows()):
            spectrum['params']['title'] = row['seq']

        # Write the updated spectra back to an MGF file
        mgf.write(spectra, output_path)
        print(f"Updated MGF file has been saved to: {output_path}")

        # Print file sizes for comparison
        print(f"Input file size: {os.path.getsize(mgf_path)} bytes")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
        print("---")

# Usage example
input_dir = "/Users/leej741/Desktop/validation_set/mgf_individual_files"
output_dir = "/Users/leej741/Desktop/validation_set/mgf_individual_files/pepnet"

process_mgf_files(input_dir, output_dir)