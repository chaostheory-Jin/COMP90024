import pandas as pd
import json
from io import StringIO
import argparse

def read_and_process_file(filename):
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
    
    del lines[0:10]
    del lines[2]
    columns_line_11 = lines[0].strip().split(',')
    columns_line_12 = lines[1].strip().split(',')

    merged_line = [a + b for a, b in zip(columns_line_11, columns_line_12)]
    lines[0] = ','.join(merged_line) + '\n'
    del lines[1]
    del lines[-1]
    processed_data = StringIO(''.join(lines))
    df = pd.read_csv(processed_data)

    df = df.iloc[:, [0, 1, 3, 5, 6]]
    df.columns = ['location', 'date', 'rain', 'maxTemp', 'minTemp']
    df = df.fillna(0)
    df.replace('', 0, inplace=True)
    df.replace(' ', 0, inplace=True)
    df.replace('  ', 0, inplace=True) 
    new_date = df['date'].str.split('/', expand=True)
    df["day"] = new_date[0].astype(int)
    df["month"] = new_date[1].astype(int)
    df["year"] = new_date[2].astype(int)

    return df

def csv_to_json(df):
    data = []
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        row_dict['id'] = row[df.columns[0]] + row[df.columns[1]]
        data.append(row_dict)
    
    return data

def convert_to_bulk_api(data, index_name):
    bulk_data = []
    for doc in data:
        # Create bulk API operation header
        operation = {
            "index": {
                "_index": index_name,
                "_id": doc.get('id')  # Assuming each document has an 'id' field
            }
        }
        bulk_data.append(operation)
        bulk_data.append(doc)
    
    return bulk_data

def main():
    parser = argparse.ArgumentParser(description="Process a CSV file and convert to Bulk API format")
    parser.add_argument('csv_file_path', help="Path to the input CSV file")

    args = parser.parse_args()

    df = read_and_process_file(args.csv_file_path)

    json_data = csv_to_json(df)

    index_name = 'weatherstats'
    bulk_data = convert_to_bulk_api(json_data, index_name)

    output_file = 'bulk_output.json'
    with open(output_file, 'w') as f:
        for entry in bulk_data:
            f.write(json.dumps(entry) + '\n')

    print(f"{args.csv_file_path}")

if __name__ == "__main__":
    main()

