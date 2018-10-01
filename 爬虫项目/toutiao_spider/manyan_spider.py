__author__ = "Narwhale"
import re
import json
import requests
from requests.exceptions import RequestException

def get_one_page(url):
    #要加请求头，不加会出错
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/\
        537.36(KHTML, likeGecko)Chrome/69.0.3497.92Safari/537.36'
    }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>'
                         '.*?title="(.*?)".*?star">(.*?)</p>'
                         '.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>'
                         '.*?fraction">(\d+)</i>',re.S)

    res = re.findall(pattern,html)
    # print(res)

    for item in res:
        #迭代器
        yield {
            'index': item[0],
            'title': item[1],
            'actor': item[2].strip(),
            'time': item[3],
            'score': item[4] + item[5]
        }


def write_to_file(content):
    with open('result.txt','a',encoding='utf8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in  range(10):
        main(i*10)



