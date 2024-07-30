import json, requests
from flask import request, current_app
import pandas as pd

def main():
    try:
        fillin = request.headers.get('X-Fission-Params-Fill')
        start_date_1 = request.headers.get('X-Fission-Params-Start')
        end_date_1 = request.headers.get('X-Fission-Params-End')
        #month = request.headers.get('X-Fission-Params-Month')

        fillin_1 = f"{fillin}"
        start_date = f"{start_date_1}"
        end_date = f"{end_date_1}"
        #day_1 = f"{day}"
        
        #start_date = '2016-09-13'
        #start_date = '2016-09-13'
        #end_date = '2016-10-20'
        #fillin = True
        #end_date = '2021-09-10'

        bit_url = f"http://router.fission.svc.cluster.local/esq/indexname/btcprice"
        gold_url = f"http://router.fission.svc.cluster.local/esq/indexname/goldprice"
        aud_url = f"http://router.fission.svc.cluster.local/esq/indexname/audrate"
        res_bit = requests.get(bit_url)
        current_app.logger.info(f'get the data: res_bit')
        res_gold = requests.get(gold_url)
        current_app.logger.info(f'get the data: res_gold')
        res_aud = requests.get(aud_url)
        current_app.logger.info(f'get the data: res_aud')
        if res_bit.status_code == 200:
            bit_data = res_bit.json()['hits']
            gold_data = res_gold.json()['hits']
            aud_data = res_aud.json()['hits']
        else:
            print("Failed to retrieve data.")
            
        bit_df = pd.DataFrame([item['_source'] for item in bit_data])
        gold_df = pd.DataFrame([item['_source'] for item in gold_data])
        aud_df = pd.DataFrame([item['_source'] for item in aud_data])

        new_bit_df = bit_df
        new_gold_df = gold_df
        new_aud_df = aud_df

        new_bit_df['Date'] = pd.to_datetime(new_bit_df['Date'])
        new_gold_df['Date'] = pd.to_datetime(new_gold_df['Date'])
        new_aud_df['Date'] = pd.to_datetime(new_aud_df['Date'])

        sorted_new_bit_df = new_bit_df.sort_values(by='Date')
        sorted_new_gold_df = new_gold_df.sort_values(by='Date')
        sorted_new_aud_df = new_aud_df.sort_values(by='Date')

        sorted_new_bit_df.reset_index(drop=True, inplace=True)
        sorted_new_gold_df.reset_index(drop=True, inplace=True)
        sorted_new_aud_df.reset_index(drop=True, inplace=True)

        sorted_new_bit_df.rename(columns={'Value': 'BitcoinPrice'}, inplace=True)
        sorted_new_gold_df.rename(columns={'Value': 'GoldPrice'}, inplace=True)
        sorted_new_aud_df.rename(columns={'Value': 'AUDtoUSD'}, inplace=True)

        merged_df = pd.merge(sorted_new_bit_df, sorted_new_gold_df, on='Date', how='outer')
        new_merged_df = pd.merge(merged_df, sorted_new_aud_df, on='Date', how='outer')
        
        if start_date != 'false' and end_date != 'false':
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            newest_merged_df = new_merged_df[(new_merged_df['Date'] >= start_date) & (new_merged_df['Date'] <= end_date)]
        else:
            newest_merged_df = new_merged_df
        
        newest_merged_df['BitcoinPrice'] = pd.to_numeric(newest_merged_df['BitcoinPrice'], errors='coerce')
        newest_merged_df['GoldPrice'] = pd.to_numeric(newest_merged_df['GoldPrice'], errors='coerce')
        newest_merged_df['AUDtoUSD'] = pd.to_numeric(newest_merged_df['AUDtoUSD'], errors='coerce')

        if fillin_1 != 'false':
            newest_merged_df.set_index('Date', inplace=True)
            newest_merged_df['GoldPrice'] = newest_merged_df['GoldPrice'].interpolate(method='time')
            newest_merged_df['AUDtoUSD'] = newest_merged_df['AUDtoUSD'].interpolate(method='time')
        else:
            newest_merged_df.set_index('Date', inplace=True)

        newest_merged_df['AUDtoUSD'] = newest_merged_df['AUDtoUSD'].astype(float)
        newest_merged_df['BitcoinPrice'] = newest_merged_df['BitcoinPrice'].astype(float)

        newest_merged_df['BitcoinPurchasingPower'] = (100000 * newest_merged_df['AUDtoUSD']) / newest_merged_df['BitcoinPrice']
        newest_merged_df['GoldPurchasingPower'] = (100000 * newest_merged_df['AUDtoUSD']) / newest_merged_df['GoldPrice']
        newest_merged_df = newest_merged_df.reset_index()
        newest_merged_df.rename(columns={'index': 'Date'}, inplace=True)
        newest_merged_df['Date'] = newest_merged_df['Date'].dt.strftime('%Y-%m-%d')
        #newest_merged_df.reset_index(drop=True, inplace=True)
        json_data = newest_merged_df.to_json(orient='records')
        return json.dumps(json_data)
        #return json.dumps(json_data)

    except Exception as e:
        # Handle exceptions and return error message
        return json.dumps({"error": str(e)})
#main()

