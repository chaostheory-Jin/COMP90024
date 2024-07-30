import requests
from bs4 import BeautifulSoup
from datetime import datetime
from elasticsearch8 import Elasticsearch

def main():
# 获取今天的日期
    today_date = datetime.now().strftime('%m/%d/%Y')

    # 目标网页 URL
    url = 'https://www.google.com/finance/quote/GCW00:COMEX'

    # 发送 HTTP 请求获取网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功

    # 使用 BeautifulSoup 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 根据 class 属性找到目标标签
    target_div = soup.find('div', class_='YMlKec fxKbKc')

    # 提取并处理目标内容
    if target_div:
        target_content = target_div.get_text(strip=True)
        target_content = target_content.replace('$', '').replace(',', '').strip()
        target_content = float(target_content)
        
        # 准备插入数据
        gold_data = {
            "Date": today_date,
            "Value": target_content
        }
        
        # Elasticsearch 客户端配置
        client = Elasticsearch('https://elasticsearch-master.elastic.svc.cluster.local:9200', 
                            verify_certs=False,
                            ssl_show_warn=False, 
                            basic_auth=("elastic", "elastic"))
        
        try:
            # 插入数据到 Elasticsearch
            res = client.index(
                index='goldprice',
                id=gold_data["Date"],  # 使用 Date 作为唯一标识
                body=gold_data
            )
            return {'status':"200"}
            # print(f"插入成功: {res}")
        except Exception as e:
            print(f"插入失败: {e}")
    else:
        print("未找到目标标签")


