import pandas as pd

# CONFIGURATION
id_column = 'sgId'
csv_location = './scripts/starting_files/read_counts.csv'

# SCRIPT
df = pd.read_csv(csv_location, header=None, low_memory=False)

# Combine the first two rows to form the header
header = df.iloc[:2].apply(lambda x: ', '.join(x.dropna()), axis=0)

# Skip the first two rows and set the combined header
df = df[2:]
df.columns = header
df.columns = df.columns.str.replace('sgRNA read counts, ', '')
df.columns = df.columns.str.replace('sgRNA growth phenotypes, ', '')
df = df.loc[:, ~df.columns.str.startswith('gamma')]
print(df.columns)

