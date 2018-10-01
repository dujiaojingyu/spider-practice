__author__ = "Narwhale"

import requests
from pyquery import PyQuery as pq
import pymongo
from wexin.config import *
from urllib.parse import urlencode

proxy = None
proxy_url = PROXY_URL
base_url = BASE_URL
max_count = MAX_COUNT
headers = HEADERS

#连接MongoDB
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_html(url, count=1):
    """获取html文本"""
    print('Crawling:', url)
    print('tried count:',count)
    global proxy
    #递归结束条件
    if count >= max_count:
        print('Tried to many counts')
        return None

    try:
        if proxy:
            #代理设置
            proxies = {
                'http':'http://' + proxy,
                'https': 'https://' + proxy
            }
            print(proxies)
            response = requests.get(url=url,
                                    headers=headers,
                                    proxies=proxies,
                                    allow_redirects=False,
                                    )  #allow_redirects设置为不跳转

        else:
            response = requests.get(url = url,headers=headers,allow_redirects=False)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('320')
            #获取一个代理
            proxy = get_proxy()
            if proxy:
                print('Using proxy:', proxy)
                return get_html(url)
            else:
                print('Get proxy Failed')
        return None
    except ConnectionError as e:
        print('Error:', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        '_sug_type_': '',
        's_from': 'input',
        '_sug_': 'n',
        'type': '2',
        'page': page,
        'ie': 'utf8',
    }

    querys = urlencode(data)     # 转换成get请求数据的形式
    url = base_url + querys      # base_url与get请求数据相加为完整的url链接
    html = get_html(url)
    return html


def get_proxy():
    try:
        response = requests.get(proxy_url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_page(html):
    doc = pq(html)
    items = doc('.news-box .news-list h3 a').items()
    for item in items:
        yield item.attr('href')      #获取文章url


def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    doc = pq(html)
    title = doc('#activity-name').text()
    content = doc('#img-content').text()
    data = doc('.meta_content #publish_time').text()
    nickname = doc('#meta_content > span.rich_media_meta.rich_media_meta_text').text()
    wechat = doc('#js_name').text()

    return {
        'title': title,
        'content': content,
        'data': data,
        'nickname': nickname,
        'wechat': wechat,
    }


def save_to_mongo(data):
    if db[MONGO_TABLE].update({'title':data['title']},{'$set':data},True):
        print('Save to MongoDB:',data['title'])
    else:
        print('Save to MongoDB Failed')


def main():
    for i in range(1,100+1):
        html = get_index(keyword=KEYWORD,page=i)
        if html:
            article_urls = parse_page(html)
            # proxy = get_proxy(proxy_url)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                result = parse_detail(article_html)
                save_to_mongo(result)



if __name__ == '__main__':
    main()
