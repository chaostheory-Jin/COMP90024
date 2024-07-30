import json, requests
from flask import request, current_app
import pandas as pd

def main():
    try:
        year = request.headers.get('X-Fission-Params-Year')
        locationc = request.headers.get('X-Fission-Params-Locationc')
        locationw = request.headers.get('X-Fission-Params-Locationw')
        year_1 = f"{year}"
        location_1 = f"{locationw}"
        location_2 = f"{locationc}"
        #year_1 = 2015
        #location_1 = 'DUNALLEY%20(STROUD%20POINT)'
        #location_2 = 'dunalley_(stroud_point)'
        crash_url = f"http://router.fission.svc.cluster.local/advanceeq/indexname/crash/date/{year_1}/location/{location_2}"
        weather_url = f"http://router.fission.svc.cluster.local/weather/year/{year_1}/month/false/day/false/location/{location_1}/weatherstat/rain/bymonth/true/index/weatherstats"
        weather_day_url = f"http://router.fission.svc.cluster.local/weather/year/{year_1}/month/false/day/false/location/{location_1}/weatherstat/rain/bymonth/false/index/weatherstats"
        temp_url = f"http://router.fission.svc.cluster.local/weather/year/{year_1}/month/false/day/false/location/{location_1}/weatherstat/maxTemp/bymonth/true/index/weatherstats"
        res_crash = requests.get(crash_url)
        current_app.logger.info(f'get the data: res_crash')
        res_weather = requests.get(weather_url)
        current_app.logger.info(f'get the data: res_weather')
        res_weather_day = requests.get(weather_day_url)
        current_app.logger.info(f'get the data: res_weather_day')
        res_maxTemp = requests.get(temp_url)
        current_app.logger.info(f'get the data: res_maxTemp')
        if res_crash.status_code == 200:
            crash_data = res_crash.json()['hits']
            weather_data = res_weather.json()['groupby']['buckets']
            weather_data_day = res_weather_day.json()['hits']
            maxTemp_data = res_maxTemp.json()['groupby']['buckets']
            #print(crash_data)
            #print(weather_data)
            #print(weather_data_day)
        else:
            print("Failed to retrieve data.")
            
        crash_df = pd.DataFrame([item['_source'] for item in crash_data])
        #crash_df = crash_df.groupby(['date', 'location']).reset_index()
        #crash_df['date'] = crash_df['date'].astype(str)
        
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
        
        merged_df = pd.merge(crash_df, weather_df, on='date', how='inner')

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

    
        new_merged_df = pd.merge(merged_df, no_rain_df, on='date', how='inner')
        newest_merged_df = pd.merge(new_merged_df, maxTemp_df, on='date', how='inner')
        newest_merged_df['crash_count'] = newest_merged_df['crash_count'].astype(int)
        newest_merged_df['date'] = pd.to_datetime(newest_merged_df['date'], format='%Y-%m', errors='coerce')
        newest_merged_df.sort_values(by='date', inplace=True)
        newest_merged_df['date'] = newest_merged_df['date'].dt.to_period('M')
        newest_merged_df.reset_index(drop=True, inplace=True)
        json_data = newest_merged_df.to_json(orient='records')
    
        return json.dumps(json_data)

    except Exception as e:
        # Handle exceptions and return error message
        return json.dumps({"error": str(e)})

