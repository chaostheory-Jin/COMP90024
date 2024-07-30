import json, requests
from flask import current_app
import pandas as pd

def main():
    try:
        #year = request.headers.get('X-Fission-Params-Year')
        #locationc = request.headers.get('X-Fission-Params-Locationc')
        #locationw = request.headers.get('X-Fission-Params-Locationw')
        #month = request.headers.get('X-Fission-Params-Month')

        #month_1 = f"{month}"
        #day_1 = f"{day}"
        
        #start_date = '2016-09-13'
        #end_date = '2021-09-10'

        aud_url = f"http://router.fission.svc.cluster.local/esq/indexname/audrate"
        gini_url = f"http://router.fission.svc.cluster.local/esq/indexname/ginico"
        incomeinequality_url = f"http://router.fission.svc.cluster.local/esq/indexname/incomeinequality"

        res_aud = requests.get(aud_url)
        current_app.logger.info(f'get the data: res_aud')
        res_gini = requests.get(gini_url)
        current_app.logger.info(f'get the data: res_gini')
        res_incomeinequality = requests.get(incomeinequality_url)
        current_app.logger.info(f'get the data: res_incomeinequality')

        if res_aud.status_code == 200:
            aud_data = res_aud.json()['hits']
            gini_data = res_gini.json()['hits']
            incomeinequality_data = res_incomeinequality.json()['hits']
        else:
            print("Failed to retrieve data.") 

        aud_df = pd.DataFrame([item['_source'] for item in aud_data])
        gini_df = pd.DataFrame([item['_source'] for item in gini_data])
        incomeinequality_df = pd.DataFrame([item['_source'] for item in incomeinequality_data])

        merged_df = pd.merge(incomeinequality_df, gini_df, on='Year', how='inner')
        merged_df = merged_df.drop_duplicates().reset_index(drop = True)
        merged_df = merged_df.drop('Inequality', axis=1)

        new_aud_df = aud_df

        new_aud_df['Date'] = pd.to_datetime(new_aud_df['Date'])
        sorted_new_aud_df = new_aud_df.sort_values(by='Date')
        sorted_new_aud_df.reset_index(drop=True, inplace=True)
        sorted_new_aud_df.rename(columns={'Value': 'AUDtoUSD'}, inplace=True)
        sorted_new_aud_df['AUDtoUSD'] = sorted_new_aud_df['AUDtoUSD'].interpolate(method='time')
        
        df = sorted_new_aud_df
        df['Date'] = pd.to_datetime(df['Date'])
        df['AUDtoUSD'] = df['AUDtoUSD'].astype(float)
        df['TwoYearGroup'] = df['Date'].dt.year - (df['Date'].dt.year - 2001) % 2 
        grouped = df.groupby('TwoYearGroup')['AUDtoUSD'].mean().reset_index()
        grouped['TwoYearGroup'] = grouped['TwoYearGroup'].apply(
            lambda x: str(x) + str(x + 1)
        )
        grouped.rename(columns={'TwoYearGroup': 'Date', 'AUDtoUSD': 'AverageAUDtoUSD'}, inplace=True)
        grouped['Date'] = grouped['Date'].apply(lambda x: x[:4] + x[6:])
        grouped.rename(columns={'Date': 'Year'}, inplace=True)
        new_merged_df = pd.merge(grouped, merged_df, on='Year', how='inner')
    
        json_data = new_merged_df.to_json(orient='records')
        #return new_merged_df
        return json.dumps(json_data)

    except Exception as e:
        # Handle exceptions and return error message
        return json.dumps({"error": str(e)})
#main()

