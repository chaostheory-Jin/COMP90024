import requests
from bs4 import BeautifulSoup
from datetime import datetime
from elasticsearch8 import Elasticsearch

def fetch_and_store_aud_rate():
    url = 'https://www.google.com/finance/quote/AUD-USD'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except:
        return {'status':'no response'}


    soup = BeautifulSoup(response.text, 'html.parser')
    target_div = soup.find('div', class_='YMlKec fxKbKc')

    if not target_div:
        return {'status':"Could not find the exchange rate on the page."}

    target_content = target_div.get_text(strip=True)
    target_content = target_content.replace(',', '').strip()

    try:
        value = float(target_content)
    except:
        return {'status':"Could not convert the exchange rate to a float."}

    today = datetime.today().strftime('%d/%m/%Y')
    doc = {
        'Date': today,
        'Value': value
    }

    client = Elasticsearch('https://elasticsearch-master.elastic.svc.cluster.local:9200', 
                            verify_certs=False,
                            ssl_show_warn=False, 
                            basic_auth=("elastic", "elastic"))

    try:
        res = client.index(
            index='audrate',
            id=today,
            body=doc
        )
        return {'status':"200"}
    except:
        return {'status':"insert failed"}

def main():
    fetch_and_store_aud_rate()