import json
from flask import request
from elasticsearch8 import Elasticsearch

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()


def main():
    try:

        # Setup Elasticsearch client
        client = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
        )

        # Construct the query dynamically based on input
        year = request.headers.get('X-Fission-Params-Year')
        location = request.headers.get('X-Fission-Params-Location')
        month = request.headers.get('X-Fission-Params-Month')
        day = request.headers.get('X-Fission-Params-Day')
        year_1 = f"{year}"
        location_1 = f"{location}"
        month_1 = f"{month}"
        day_1 = f"{day}"
        index = request.headers.get('X-Fission-Params-Index')
        index_1 = f"{index}"

        # Initialize the query parts
        must_queries = []

        if year_1 != 'false':
            must_queries.append({
                "term": {
                    "year": {   # update
                        "value": year_1
                    }
                }
            })

        if month_1 != 'false':
            must_queries.append({
                "term": {
                    "month": {
                        "value": month_1
                    }
                }
            })
            
        if day_1 != 'false':
            must_queries.append({
                "term": {
                    "day": {   # update
                        "value": day_1
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


        weather_stat = request.headers.get('X-Fission-Params-Weather')
        weather_stat_1 = f"{weather_stat}"
        # Determine fields to retrieve based on the index, formatted as required
        fields = [{"field": weather_stat_1}, {"field": "location"}, {"field": "day"}, {"field": "month"}, {"field": "year"}]

        by_month = request.headers.get('X-Fission-Params-Bymonth')
        by_month_1 = f"{by_month}"
        if by_month_1 == 'false':
            response = client.search(
                index=index_1,
                query=query,
                fields=fields,  # Correct parameter for specifying fields
                size=5000, # Adjust the size as needed
                source = False
                
            )
            return json.dumps(response['hits'])
        else:
            response = client.search(
                index=index_1,
                query=query,
                fields=fields,  # Correct parameter for specifying fields
                size=5000, # Adjust the size as needed
                source = False,
                aggregations = {
                                    "groupby": {
                                        "composite": {
                                            "size": 5000,
                                            "sources": [
                                                {
                                                    "month": {
                                                        "terms": {
                                                            "field": "month",
                                                            "missing_bucket": True,
                                                            "order": "asc"
                                                        }
                                                    }               
                                                },
                                                {
                                                    "year": {
                                                        "terms": {
                                                            "field": "year", # update
                                                            "missing_bucket": True,
                                                            "order": "asc"
                                                        }
                                                    }
                                                }
                                            ]
                                        },
                                        "aggregations": {
                                            "weather_stats": {
                                                "stats": {
                                                    "field": weather_stat_1
                                                }
                                            }
                                        }
                                    }
                                }
                
            )

            return json.dumps(response['aggregations'])

    except Exception as e:
        # Handle exceptions and return error message
        return json.dumps({"error": str(e)})
