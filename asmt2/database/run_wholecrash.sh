#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base_directory_path>"
    exit 1
fi

BASE_DIRECTORY_PATH=$1

stationnames=(
	#place your own stationname here
)

for stationname in "${stationnames[@]}"; do
    DIRECTORY_PATH="${BASE_DIRECTORY_PATH}/${stationname}"
    find "$DIRECTORY_PATH" -type f -name "*.csv" | while read -r CSV_FILE_PATH; do
        echo "Processing file: $CSV_FILE_PATH"
        
        python3 wprocess.py "$CSV_FILE_PATH"
        
        curl -XPOST -k 'https://127.0.0.1:9200/weatherstats/_bulk' --header 'Content-Type: application/json' --data-binary '@bulk_output.json' --user 'elastic:elastic' | jq '.'
        
        echo "Finished processing file: $CSV_FILE_PATH"
    done
done
