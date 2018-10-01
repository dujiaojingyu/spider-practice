__author__ = "Narwhale"
import re
import os
import json
import requests
import pymongo
from .config import *
from hashlib import md5
from urllib.parse import urlencode
from multiprocessing import Pool
from requests.exceptions import RequestException

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
}


def get_page_index(offest,keyword):
    data = {

        'offset': offest,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1,
        'from': 'gallery',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错！')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('成功储存到MongoDB中',result)
            return True
        return False
    except Exception:
        pass


def get_page_detail(url):
    try:
        response = requests.get(url,headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错！')
        return None

def parse_page_detail(html,url):
    partern1 = re.compile('BASE_DATA.galleryInfo =.*?title.*? \'(.*?),.*?</script>',re.S)
    partern2 = re.compile('BASE_DATA.galleryInfo = (.*?)</script>',re.S)
    title= re.search(partern1,html).group(1)
    gg = re.search(partern2,html).group(1)
    gg = re.sub('\\\\', '', gg)
    images = re.findall('url":"(.*?)".*?width"',gg)

    for image in images:
        download_images(image)

    if title and images:
        return {
            'title':title,
            'url':url,
            'images':images
        }


def download_images(url):
    print('正在下载',url)
    try:
        response = requests.get(url,headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            save_images(response.content)
        return None
    except RequestException:
        print('请求图片出错！')
        return None


def save_images(content):
    file_path = "{0}/{1}.{2}".format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()




def main(offest):
    # for i in range(10):
    html = get_page_index(offest, KEYWORD)
    for url in parse_page_index(html):
        if url != None:
            html = get_page_detail(url)
            if html:
                result = parse_page_detail(html,url)
                if result:
                    save_to_mongo(result)
                # print(result)


if __name__ == '__main__':
    groups = [i*20 for i in range(GROUP_START,GROUP_END+1)]
    print(groups)
    pool = Pool()
    pool.map(main,groups)