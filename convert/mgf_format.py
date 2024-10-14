from pyteomics import mgf
import pandas as pd
import os

# Path to the MGF file
mgf_path = "/Users/leej741/Desktop/validation_set/mgf_individual_files/01_ECTABPP_NP_1_9Jan17_Wally_17-12-02.mzML_0.001_qvaluecutoff.mgf"

# Read the MGF file
with mgf.MGF(mgf_path) as reader:
    spectra = list(reader)
print(f"Successfully read {len(spectra)} spectra from the input file.")

# Extract precursor information and create DataFrame
precursors = [spectrum['params'] for spectrum in spectra]
df = pd.DataFrame.from_records(precursors)

# Set 'title' column equal to 'seq' column
df['title'] = df['seq']

# Display the first few rows to verify the change
print(df[['title', 'seq']].head())

# Update the spectra with new titles
for spectrum, (index, row) in zip(spectra, df.iterrows()):
    spectrum['params']['title'] = row['seq']

# Write the updated spectra back to an MGF file
output_path = "/Users/leej741/Desktop/validation_set/mgf_individual_files/pepnet/pepnet_01_ECTABPP_NP_1_9Jan17_Wally_17-12-02.mzML_0.001_qvaluecutoff.mgf"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write the updated MGF file
mgf.write(spectra, output_path)
print(f"Updated MGF file has been saved to: {output_path}")

# Verify the content of the new file
with mgf.MGF(output_path) as reader:
    new_spectra = list(reader)

print(f"Number of spectra in the new file: {len(new_spectra)}")
if new_spectra:
    print("First spectrum title:", new_spectra[0]['params']['title'])

# Print file sizes for comparison
print(f"Input file size: {os.path.getsize(mgf_path)} bytes")
print(f"Output file size: {os.path.getsize(output_path)} bytes")