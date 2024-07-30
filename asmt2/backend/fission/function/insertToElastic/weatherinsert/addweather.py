import json
from flask import request, current_app
from elasticsearch8 import Elasticsearch

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()



def main():
    try:
        index_name= request.headers['X-Fission-Params-Index']
    except KeyError:
         index_name= None

    current_app.logger.info(f'index name: {index_name}')

    if (index_name == None):
        return {"error": "index name is missing"}, 400
    elif (index_name != "weathertest" and index_name != "weatherstats"):
        return {"error": "index name is not valid"}, 400

    client = Elasticsearch('https://elasticsearch-master.elastic.svc.cluster.local:9200', 
                            verify_certs = False,
                            ssl_show_warn = False, 
                            basic_auth = (config('ES_USERNAME'), config('ES_PASSWORD')))
    
    for weather in request.get_json(force=True):
        try:
            current_app.logger.info(f'get the data: {weather}')
            res = client.index(
                index= f"{index_name}",
                id=f'{weather["location"]}{weather["date"]}',
                body=weather
            )
            current_app.logger.info(f'inserted data: {res}')
        except Exception as e:
            current_app.logger.error(f'An error occurred: {e}')
            return {"error": str(e)}, 400
    
    return f'inserted data: {res}', 200
