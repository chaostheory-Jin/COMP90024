import requests
from bs4 import BeautifulSoup
from elasticsearch8 import Elasticsearch
from datetime import datetime

def fetch_and_insert_btc_price():
    url = 'https://www.google.com/finance/quote/BTC-USD'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    target_div = soup.find('div', class_='YMlKec fxKbKc')

    if target_div:
        target_content = target_div.get_text(strip=True)
        target_content = target_content.replace(',', '').strip()
        btc_price = float(target_content)
    else:
        return {'status':"Could not convert the exchange rate to a float."}

    current_date = datetime.today().strftime('%d/%m/%Y')

    client = Elasticsearch('https://elasticsearch-master.elastic.svc.cluster.local:9200', 
                            verify_certs=False,
                            ssl_show_warn=False, 
                            basic_auth=("elastic", "elastic"))
    
    data = {
        'Date': current_date,
        'Value': btc_price
    }

    try:
        res = client.index(
            index='btcprice',
            id=current_date,
            body=data
        )
        return {'status':"200"}
    except:
        return {'status':"insert failed"}

def main():
    fetch_and_insert_btc_price()