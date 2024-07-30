import requests
from flask import request, current_app

def transform_location(lat,long):
    url = f"https://api.dggs.ga.gov.au/auspix/dataDrill?lat84={lat}&long84={long}"
    # url = "https://api.dggs.ga.gov.au/auspix/dataDrill?lat84=
    r = requests.get(url)
    return r.json()

def main():
    current_app.logger.info(f'Received request: ${request.headers}')
    lat = request.args.get('lat', '-27.5351')
    long = request.args.get('long', '152.9933')

    return transform_location(lat,long)