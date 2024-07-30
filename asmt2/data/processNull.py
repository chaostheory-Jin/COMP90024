import os
import pandas as pd

folder_path = '/home/aston/Downloads/pollen'

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        df = pd.read_csv(file_path)
        
        df.dropna(inplace=True)
        
        df.to_csv(file_path, index=False)
        print(f'Processed {file_path}')

print('All CSV files have been processed.')

