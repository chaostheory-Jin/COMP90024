import json
import requests
from flask import request, current_app
from datetime import datetime, timedelta
from elasticsearch8 import Elasticsearch

def list_months(date_range):
    start_str, end_str = date_range.split('-')

    start_date = datetime.strptime(start_str, "%Y%m")
    end_date = datetime.strptime(end_str, "%Y%m")
    
    current_date = start_date
    months = []
    while current_date <= end_date:
        months.append(current_date.strftime("%Y%m"))
        if current_date.month == 12:
            next_month = current_date.replace(year=current_date.year + 1, month=1)
        else:
            next_month = current_date.replace(month=current_date.month + 1)
        current_date = next_month

    return months

def main():
    try:
        index = request.headers['X-Fission-Params-Index']
        daterange = request.headers['X-Fission-Params-Daterange']
        insertindex = request.headers['X-Fission-Params-Insertindex']
        monthlist = []
        monthlist = list_months(daterange)
        print(monthlist)
        # locationList = ["WARWICK"]
        locationlisturl = f'http://router.fission.svc.cluster.local/qstation/{index}'
        # return locationlisturl
        locationlist = requests.get(locationlisturl)
        
        # try:
        #     client = Elasticsearch (
        #         'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        #         verify_certs= False,
        #         basic_auth=('elastic', 'elastic')
        #     )
        # except:
        #     return

        # try:
        #     res= client.search(
        #         index=f"{index}*",
        #         query={"match_all": {}}
        #     )
        # except:
        #     return
        
        # return res['hits']
        
        # current_app.logger.info(locationlist.text)
        locationlist = locationlist.json()
        # locationlist = res['hits']
        locationlist = locationlist['hits']
        # return locationlist
        stations = []
        res = {}
        for hit in locationlist:
            # hit = json.loads(hit)
            
            station_info = {
                'stationname': hit['_source']['stationname'],
                'statename': hit['_source']['statename']
            }
            stations.append(station_info)
        # res["data"] = stations
        # return res
        fetUrl = 'http://router.fission.svc.cluster.local/ftpfetchweather'
        insertUrl = f'http://router.fission.svc.cluster.local/weatherinsert/{insertindex}'
        weather_all=[]
        for i in stations:
            for date in monthlist:  
                # weather_all.append(fetUrl+'/'+i['statename']+'/'+i['stationname']+'/'+date)
                try:
                    print(fetUrl+'/'+i['statename']+'/'+i['stationname']+'/'+date)
                    response = requests.get(fetUrl+'/'+i['statename']+'/'+i['stationname']+'/'+date)
                # current_app.logger.info(response.json())
                    data = response.json()
                    insertdata = data['data']
                    
                    # for i in insertdata:
                    #     # print(type(i))
                    #     i = i
                    #     response = requests.post(insertUrl, json=insertdata)
                    # current_app.logger.info(f'get the data: {response.json()}')
                    try: 
                        response = requests.post(insertUrl, json=insertdata)
                        current_app.logger.info(f'get the data: {response.json()}')
                    except:
                    # weather_all.append(e)
                        return (f"INSERT An error occurred: {e}")
                        # pass
                # response = requests.post(insertUrl, json=data)
                    weather_all.append(insertdata)
                except:
                    # weather_all.append(e)
                    # return (f"In An error occurred: {e}")
                    pass
        # res['data'] = weather_all
        # return res
    except Exception as e:
        return (f"An error occurred: {e}")
    