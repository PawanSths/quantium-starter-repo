import pandas as pd
import glob
import os

data_folder = './data'
csv_files = glob.glob(os.path.join(data_folder, "*.csv"))

processed_dfs = []

for file in csv_files:
    df = pd.read_csv(file)

    df = df[df['product'].str.lower() == 'pink morsel'].copy()

    df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['quantity'] = df['quantity'].astype(float)

    df['sales'] = df['quantity'] * df['price']

    df_formatted = df[['sales', 'date', 'region']]

    processed_dfs.append(df_formatted)

final_df = pd.concat(processed_dfs, ignore_index=True)

output_path = './formatted_output.csv'
final_df.to_csv(output_path, index=False)

print(f"Data processing complete, Output saved to '{output_path}'.")