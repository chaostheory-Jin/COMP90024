import json, requests
from flask import request, current_app
import pandas as pd

def main():
    try:
        year = request.headers.get('X-Fission-Params-Year')
        locationw = request.headers.get('X-Fission-Params-Locationw')
        locationp = request.headers.get('X-Fission-Params-Locationp')
        #year = 2017
        #location_1 = 'campbelltown'
        #location_2 = 'campbelltown_(mount_annan)'
        year_1 = f"{year}"
        location_1 = f"{locationw}"
        location_2 = f"{locationp}"

        
        pollen_url = f"http://router.fission.svc.cluster.local/advanceeq/indexname/pollen/date/{year_1}/location/{location_2}"
        weather_url = f"http://router.fission.svc.cluster.local/weather/year/{year_1}/month/false/day/false/location/{location_1}/weatherstat/rain/bymonth/true/index/weatherstats"
        weather_day_url = f"http://router.fission.svc.cluster.local/weather/year/{year_1}/month/false/day/false/location/{location_1}/weatherstat/rain/bymonth/false/index/weatherstats"
        temp_url = f"http://router.fission.svc.cluster.local/weather/year/{year_1}/month/false/day/false/location/{location_1}/weatherstat/maxTemp/bymonth/true/index/weatherstats"
        
        #pollen_url = f"http://localhost:9090/advanceeq/indexname/pollen/date/2018/location/viewbank"
        #weather_url = f"http://localhost:9090/weather/year/2018/month/false/day/false/location/viewbank/weatherstat/rain/bymonth/true/index/weatherstats"
        #weather_day_url = f"http://localhost:9090/weather/year/2018/month/false/day/false/location/viewbank/weatherstat/rain/bymonth/false/index/weatherstats"
        #temp_url = f"http://localhost:9090/weather/year/2018/month/false/day/false/location/viewbank/weatherstat/maxTemp/bymonth/true/index/weatherstats"
        #http://localhost:9090/weather/year/2020/month/false/day/false/location/campbelltown/weatherstat/rain/bymonth/true/index/weatherstats
        
        res_pollen = requests.get(pollen_url)
        current_app.logger.info(f'get the data: res_pollen')
        res_weather = requests.get(weather_url)
        current_app.logger.info(f'get the data: res_weather')
        res_weather_day = requests.get(weather_day_url)
        current_app.logger.info(f'get the data: res_weather_day')
        res_maxTemp = requests.get(temp_url)
        current_app.logger.info(f'get the data: res_maxTemp')
        
        if res_pollen.status_code == 200:
            pollen_data = res_pollen.json()['hits']
            weather_data = res_weather.json()['groupby']['buckets']
            weather_data_day = res_weather_day.json()['hits']
            maxTemp_data = res_maxTemp.json()['groupby']['buckets']
            #print(pollen_data)
            #print(weather_data)
            #print(weather_data_day)    
        else:
            print("Failed to retrieve data.")

        pollen_df = pd.DataFrame([item['_source'] for item in pollen_data])
        pollen_df['poaceae'] = pollen_df['poaceae'].astype(float)
        pollen_df['other'] = pollen_df['other'].astype(float)
        pollen_df['date'] = pd.to_datetime(pollen_df['date'])
        pollen_df['date'] = pollen_df['date'].dt.to_period('M')
        pollen_df = pollen_df.drop_duplicates()
        if location_2.lower() == 'brisbane':
            pollen_df = pollen_df[pollen_df['location'] == 'BRISBANE']

        grouped_pollen_df = pollen_df.groupby(['date', 'location']).agg({'poaceae':'sum', 'other':'sum'}).reset_index()
        grouped_pollen_df['date'] = grouped_pollen_df['date'].astype(str)
    
        for item in weather_data:
            year = item['key']['year']
            month = item['key']['month']
            max_value = round(item['weather_stats']['max'], 1)
            avg_value = round(item['weather_stats']['avg'], 1)
            sum_value = round(item['weather_stats']['sum'], 1)
            date_str = f'{year}-{month:02d}'
            item['key']['year_month'] = date_str
            item['weather_stats']['max'] = max_value
            item['weather_stats']['avg'] = avg_value
            item['weather_stats']['sum'] = sum_value
        extracted_weather = [{'date': item['key']['year_month'],
                    'maxRain': item['weather_stats']['max'],
                    'avgRain': item['weather_stats']['avg'],
                    'sumRain': item['weather_stats']['sum']} for item in weather_data]
        
        weather_df = pd.DataFrame(extracted_weather)

        for item in weather_data_day:
            year = item['fields']['year'][0]
            month = item['fields']['month'][0]
            day = item['fields']['day'][0]
            rain = item['fields']['rain'][0]
            date_str = f'{year}-{month:02d}'
            item['fields']['year_month'] = date_str
        extracted_weather_day = [{'date': item['fields']['year_month'],
                    'rain': item['fields']['rain'][0],
                    'day': item['fields']['year'][0]} for item in weather_data_day]
        
        df = pd.DataFrame(extracted_weather_day)
        no_rain_df = df.groupby('date')['rain'].apply(lambda x: (x == 0.0).mean()).reset_index()
        no_rain_df.columns = ['date', 'Zero_Rain_Percent']

        for item in maxTemp_data:
            year = item['key']['year']
            month = item['key']['month']
            max_value = round(item['weather_stats']['max'], 1)
            avg_value = round(item['weather_stats']['avg'], 1)
            sum_value = round(item['weather_stats']['sum'], 1)
            date_str = f'{year}-{month:02d}'
            item['key']['year_month'] = date_str
            item['weather_stats']['max'] = max_value
            item['weather_stats']['avg'] = avg_value
            item['weather_stats']['sum'] = sum_value
        extracted_weather_temp = [{'date': item['key']['year_month'],
                    'maxTemp': item['weather_stats']['max'],
                    'avgTemp': item['weather_stats']['avg'],
                    'sumTemp': item['weather_stats']['sum']} for item in maxTemp_data]
        
        maxTemp_df = pd.DataFrame(extracted_weather_temp)
        
        merged_df = pd.merge(weather_df, no_rain_df, on='date', how='inner')
        new_merged_df = pd.merge(merged_df, grouped_pollen_df, on='date', how='inner')
        newest_merged_df = pd.merge(new_merged_df, maxTemp_df, on='date', how='inner')
        json_data = newest_merged_df.to_json(orient='records')

        #return newest_merged_df
        return json.dumps(json_data)
    
    except Exception as e:
        # Handle exceptions and return error message
        return json.dumps({"error": str(e)})

