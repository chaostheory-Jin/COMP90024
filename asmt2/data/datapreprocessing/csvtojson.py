import csv
import json
import pandas as pd

def csv_to_json(csv_file_path, json_file_path):
    # Open the CSV file for reading
        
    with open(csv_file_path, 'r', newline='',encoding='ISO-8859-1') as csv_file:
        # Read the CSV file
        csv_reader = csv.DictReader(csv_file)
        
        # Convert each row to a dictionary and store in a list
        data = []
        for row in csv_reader:
            data.append(row)
    
    # Write the JSON data to a file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def convert_to_bulk_api(input_file, output_file, index_name):
    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(output_file, 'w') as f:
        for doc in data:
            # Create bulk API operation header
            operation = {
                "index": {
                    "_index": index_name,
                    "_id": doc.get('id')  # Assuming each document has an 'id' field
                }
            }
            f.write(json.dumps(operation) + '\n')  # Write header to file
            f.write(json.dumps(doc) + '\n')        # Write document data to file



output_file = 'output.json'


csv_to_json('/home/aston/comp90024/fission/functions/data/location_data.csv', 'output.json')
input_file = 'output.json'
output_file = 'locationdata.json'
index_name = 'location'
convert_to_bulk_api(input_file, output_file, index_name)


