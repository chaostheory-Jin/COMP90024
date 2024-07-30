import json
from flask import request
from elasticsearch8 import Elasticsearch

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()


def main():
    try:
        index_name= request.headers['X-Fission-Params-Index']
    except KeyError:
         index_name= None

    try:
        client = Elasticsearch (
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs= False,
            basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
        )
    except:
        return

    try:
        res= client.search(
            index=f"{index_name}*",
            query={"match_all": {}},
            size=3000
        )
    except:
        return
    
    return json.dumps(res['hits'])
