from pyteomics import mgf
import pandas as pd
import os

# Path to the MGF file
mgf_path = "/Users/leej741/Desktop/validation_set/mgf_individual_files/01_ECTABPP_NP_1_9Jan17_Wally_17-12-02.mzML_0.001_qvaluecutoff.mgf"

# Check if input file exists
if not os.path.exists(mgf_path):
    print(f"Error: Input file does not exist: {mgf_path}")
    exit(1)

# Read the MGF file without using index
try:
    with mgf.MGF(mgf_path) as reader:
        spectra = list(reader)
    print(f"Successfully read {len(spectra)} spectra from the input file.")
except Exception as e:
    print(f"Error reading input file: {e}")
    exit(1)

# Extract precursor information
precursors = [spectrum['params'] for spectrum in spectra]

# Create DataFrame
df = pd.DataFrame.from_records(precursors)

# Set 'title' column equal to 'seq' column
df['title'] = df['seq']

# Display the first few rows to verify the change
print(df[['title', 'seq']].head())

# Update the spectra with new titles
for spectrum, (index, row) in zip(spectra, df.iterrows()):
    spectrum['params']['title'] = row['seq']

# Write the updated spectra back to an MGF file
output_path = "/Users/leej741/Desktop/validation_set/mgf_individual_files/updated_01_ECTABPP_NP_1_9Jan17_Wally_17-12-02.mzML_0.001_qvaluecutoff.mgf"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

try:
    mgf.write(spectra, output_path)
    print(f"Updated MGF file has been saved to: {output_path}")
except Exception as e:
    print(f"Error writing output file: {e}")
    exit(1)

# Verify the content of the new file
try:
    with mgf.MGF(output_path) as reader:
        new_spectra = list(reader)

    print(f"Number of spectra in the new file: {len(new_spectra)}")
    if new_spectra:
        print("First spectrum title:", new_spectra[0]['params']['title'])
    else:
        print("The new file appears to be empty.")
except Exception as e:
    print(f"Error verifying output file: {e}")

# Print file sizes for comparison
print(f"Input file size: {os.path.getsize(mgf_path)} bytes")
print(f"Output file size: {os.path.getsize(output_path)} bytes")