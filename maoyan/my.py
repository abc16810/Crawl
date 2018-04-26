#coding :utf-8

from requests.exceptions import RequestException
import requests
import random
import time
import json
import re


# TOP 100
URL = 'http://maoyan.com/board/4'
H = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
}




def get_page(url):
    try:
        response = requests.get(url, headers=H)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as f:
        return None
    
def parse_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>'
                     + '.*?<img.*?>.*?src="(.*?)\@.*?name">'
                     + '<a.*?>(.*?)</a>'
                     + '.*?star">(.*?)</p>.*?releasetime">'
                     + '(.*?)</p>.*?integer">'
                     + '(.*?)</i>.*?fraction">'
                     + '(.*?)</i>.*?</dd>', re.S)
    items = pattern.findall(html)
    for item in items:
        yield {
           
          'index': item[0],
          'image': item[1],
          'title': item[2],
          'actor': item[3].strip()[3:],
          'time': item[4].strip()[5:],
          'score': item[5] + item[6]

        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\t\n')

def main(offset=0):
    url = URL + '?offset=' + str(offset)
    html = get_page(url)
    for item in parse_page(html):
        write_to_file(item)


if __name__ == '__main__':
    for x in range(0,100,10):
        time.sleep(round(random.uniform(1,1.5),2))
        print("抓取第 %d 页数据" % int(x/10)+1)
        main(offset=x)










