import json, logging
import requests
from flask import request, current_app


def main():
    try:
        locationList = ["WARWICK"]

        fetUrl = 'http://router.fission.svc.cluster.local/ftpfetchweather'
        insertUrl = 'http://router.fission.svc.cluster.local/weatherinsert'

        for i in locationList:
            response = requests.get(fetUrl)
            current_app.logger.info(f'Observations to add:')
            data = response.json()
            current_app.logger.info(f'get the data: {response.json()}')    
            response = requests.post(insertUrl, json=data)

            return response.text
    except Exception as e:
        return (f"An error occurred: {e}")
    