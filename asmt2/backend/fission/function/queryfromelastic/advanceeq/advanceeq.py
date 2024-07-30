import json
from flask import request
from elasticsearch8 import Elasticsearch

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()


def main():
    try:
        # Access the index name from the header and append a wildcard
        index_name = request.headers.get('X-Fission-Params-Index')
        index_pattern = f"{index_name}*"  # Wildcard for similar indices

        # Setup Elasticsearch client
        client = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
        )

        # Construct the query dynamically based on input
        date = request.headers.get('X-Fission-Params-Date')
        location = request.headers.get('X-Fission-Params-Location')
        date_1 = f"{date}"
        location_1 = f"{location}"

        # Initialize the query parts
        must_queries = []

        if date_1 != 'false':
            must_queries.append({
                "match": {
                    "date": {
                        "query": date_1
                    }
                }
            })

        if location_1 != 'false':
            must_queries.append({
                "match": {
                    "location": {
                        "query": location_1
                    }
                }
            })

        # Formulate the main query
        query = {"bool": {"must": must_queries}} if must_queries else {"match_all": {}}

        # Determine fields to retrieve based on the index, formatted as required
        fields = []
        if "pollen" in index_pattern:
            fields = [{"field": "poaceae"}, {"field": "other"}, {"field": "location"}, {"field": "date"}]
        elif "crash" in index_pattern:
            fields = [{"field": "crash_count"}, {"field": "location"}, {"field": "date"}]

        # Execute the search query using the wildcard index pattern
        response = client.search(
            index=index_pattern,
            query=query,
            fields=fields,  # Correct parameter for specifying fields
            size=3000,  # Adjust the size as needed
           

        )

        return json.dumps(response['hits'])

    except Exception as e:
        # Handle exceptions and return error message
        return json.dumps({"error": str(e)})
