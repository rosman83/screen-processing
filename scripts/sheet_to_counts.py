import pandas as pd
import os

# CONFIGURATION
id_column = 'sgId'
csv_location = './scripts/starting_files/read_counts.csv'
output_location = './scripts/resulting_files/'
double_header = True
lookup_table = './scripts/reference_files/library_tables/CRISPRi_v2_human_librarytable.txt'
demo = False

# STAGE 1: Grab Counts
df = pd.read_csv(csv_location, skiprows=1, low_memory=False)
if demo == True:
    df = df.head(5)
print(f'Columns in the file: {df.columns}')

if id_column not in df.columns:
    print(f'ID column {id_column} not found in the file')
    exit()

df = df.loc[:,~df.columns.str.contains('gamma', case=False)]
print(f'Columns with gamma removed: {df.columns}')

#TODO: Currently optimized only for CRISPRi_v2_human_librarytable.txt
lookup_df = pd.read_csv(lookup_table, sep='\t')

if not all(x in lookup_df.columns for x in ['sgId', 'sublibrary', 'gene']):
    print('Lookup table does not contain required columns')
    exit()

# Create a dictionary to store the mappings from genes to sublibraries
gene_sublibrary_dict = dict(zip(lookup_df['gene'], lookup_df['sublibrary']))

# Iterate through the DataFrame
for index, row in df.iterrows():
    temp_gene = row['sgId'].split('_')[0]
    # Retrieve the sublibrary from the dictionary
    temp_sublibrary = gene_sublibrary_dict.get(temp_gene, None)
    
    # Check if sublibrary exists for the gene
    if temp_sublibrary is not None:
        temp_sublibrary = temp_sublibrary.replace('_supp', '_Supp')
        temp_sublibrary = temp_sublibrary.replace('_top', '_Top')
        df.at[index, 'sgId'] = f'{temp_sublibrary}={row["sgId"]}'
    else:
        # Handle the case when sublibrary is not found for the gene
        df.at[index, 'sgId'] = f'Unassigned={row["sgId"]}'
    
    print(f'{index} / {len(df)}')


if not os.path.exists(output_location):
    os.makedirs(output_location)

for column in df.columns:
    formatted_column_name = column.replace(' ', '_').replace('/', '_').replace(',', '').lower()
    if column == id_column:
        continue
    print(f'Creating file for {column}')
    new_df = df[[id_column, column]]
    new_df.to_csv(f'{output_location}/{formatted_column_name}.counts', sep ='\t', header=False, index=False)

print('done here')