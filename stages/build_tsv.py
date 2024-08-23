import pandas as pd
import sys
import pyarrow as pyarrow
import os

InFileName = sys.argv[1]
OutFileName = sys.argv[2]

print(f"tsv2parquet: Converting file {InFileName}")

column_names = ['id', 'type', 'concept_id', 'concept_value', 'source']
# If the InFileName has a basename of 'mutation2pubtator3' then remove the lines with double quotes
if os.path.basename(InFileName) == 'mutation2pubtator3':
    InFileName_cleaned = InFileName + '_cleaned.tsv'
    with open(InFileName, 'r') as input_file, open(InFileName_cleaned, 'w') as output_file:
        for line_number, line in enumerate(input_file, 1):
            line = line.replace('"', '')
            output_file.write(line)
    df = pd.read_csv(InFileName_cleaned, sep='\t', header=None, names=column_names, low_memory=False)
else:
    df = pd.read_csv(InFileName, sep='\t', header=None, names=column_names, low_memory=False)
df.to_parquet(OutFileName)
