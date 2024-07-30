import json
from flask import request
from elasticsearch8 import Elasticsearch

def main():
    try:
        index_name= request.headers['X-Fission-Params-Index']
    except KeyError:
         index_name= None

    try:
        client = Elasticsearch (
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs= False,
            basic_auth=('elastic', 'elastic')
        )
    except:
        return

    try:
        res= client.search(
            index=f"{index_name}*",
            query={"match_all": {}}
        )
    except:
        return
    
    return json.dumps(res['hits'])
