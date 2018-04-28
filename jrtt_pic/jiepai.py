# coding: utf-8


from multiprocessing.pool import Pool
from urllib.parse import urlencode
from hashlib import md5
import time
import requests
import os


URL = 'https://www.toutiao.com/search_content/?'
POOLS = 2
START_PAGE = 1
PAGE_COUNT = 6

H = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
 'x-requested-with':'XMLHttpRequest',
}



def get_params_url(offset=0):

    p = {

        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery',
    }
    return URL + urlencode(p)

def get_page(offset):
    """
    offset: 页数偏移量
    """
    print("获取第 %d 页" % int(offset/20))
    time.sleep(1)
    url = get_params_url(offset)
    try:
        response = requests.get(url, headers=H)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None



def get_img(json):
    data = json.get('data')
    if data:
        for item in data:
            image_list = item.get('image_list')
            title = item.get('title')
            for img in image_list:
                yield {
                    'image': img.get('url'),
                    'title': title
                }

def save_img(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        local_image_url = item.get('image')
        new_image_url = local_image_url.replace('list','origin')
        print("开始下载: %s 连接:%s" % (item.get('title'),new_image_url))
        response = requests.get('http:' + new_image_url, stream=True)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content[:1024]).hexdigest(), 'jpg') 
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to save image')


def main(offset):
    json_text = get_page(offset)
    for item in get_img(json_text):
        save_img(item)


if __name__ == '__main__':
    pool = Pool(POOLS)
    groups = ([x * 20 for x in range(START_PAGE-1, PAGE_COUNT)])
    pool.map(main, groups)
    pool.close()
    pool.join()
    # main(0)
