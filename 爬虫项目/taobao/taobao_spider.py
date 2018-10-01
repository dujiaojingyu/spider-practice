__author__ = "Narwhale"
import re
import pymongo
from .config import *  #导入当前目录的py文件加个点就不会出现红下划线
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]   #不能用引号括起来

#声明浏览器对象
browser = webdriver.Chrome()
#等待时间
wait = WebDriverWait(browser, 10)

def search():
    try:
        #打开淘宝主页
        browser.get('https://www.taobao.com/')
        #寻找输入框
        input_tb = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#q"))
        )
        #寻找提交按钮
        submit_tb = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        # 输入搜索字段
        input_tb.send_keys('美食')
        # 点击提交
        submit_tb.click()
        # 加载完成之后获取页数
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        input_page = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        # 寻找提交按钮
        submit_page = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input_page.clear()
        input_page.send_keys(page_number)
        submit_page.click()
        wait.until(
            EC.text_to_be_present_in_element(
                (
                By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),
                str(page_number)
            )
        )
        get_products()
    except TimeoutException:
        return next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-itemlist .items .item")))
    #获取源代码
    html = browser.page_source
    doc = pq(html)
    #获取全部的items
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text(),
            }
        # print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存MongoDB成功',result)
    except Exception:
        print('保存MongoDB失败',result)

def main():
    total = search()
    total = re.compile('(\d+)').search(total).group(1)
    for i in range(2,int(total)+1):
        next_page(i)


if __name__ == '__main__':
    main()