import json
import requests
from flask import request, current_app
from datetime import datetime
from elasticsearch8 import Elasticsearch

def get_current_month():
    current_date = datetime.now()
    return current_date.strftime("%Y%m")

def process_index(index, insertindex, current_month):
    try:
        locationlisturl = f'http://router.fission.svc.cluster.local/qstation/{index}'
        locationlist = requests.get(locationlisturl)
        locationlist = locationlist.json()
        locationlist = locationlist['hits']
        
        stations = []
        for hit in locationlist:
            station_info = {
                'stationname': hit['_source']['stationname'],
                'statename': hit['_source']['statename']
            }
            stations.append(station_info)
        
        fetUrl = 'http://router.fission.svc.cluster.local/ftpfetchweather'
        insertUrl = f'http://router.fission.svc.cluster.local/weatherinsert/{insertindex}'
        weather_all = []
        
        for station in stations:
            try:
                request_url = f'{fetUrl}/{station["statename"]}/{station["stationname"]}/{current_month}'
                print(request_url)
                response = requests.get(request_url)
                data = response.json()
                insertdata = data['data']
                
                try:
                    response = requests.post(insertUrl, json=insertdata)
                    current_app.logger.info(f'Inserted data: {response.json()}')
                except Exception as e:
                    current_app.logger.error(f"INSERT An error occurred: {e}")
                    return (f"INSERT An error occurred: {e}")
                    
                weather_all.append(insertdata)
            except Exception as e:
                current_app.logger.error(f"In An error occurred: {e}")
                pass
    except Exception as e:
        return (f"An error occurred: {e}")

def main():
    try:
        current_month = get_current_month()
        print(current_month)
        
        indices = ['pollenstation', 'crashstation']
        insertindex = 'weatherstats'

        for index in indices:
            process_index(index, insertindex, current_month)
        
    except Exception as e:
        return (f"An error occurred: {e}")
