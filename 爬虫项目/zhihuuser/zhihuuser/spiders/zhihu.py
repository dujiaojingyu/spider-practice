# -*- coding: utf-8 -*-
import json
import requests
import scrapy
from zhihuuser.settings import *
from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com','api.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'

    #开始用户url
    user_url = 'https://www.zhihu.com/api/v4/members/{user}/activities'

    #关注url
    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followees_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 粉丝url
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        #更改请求url，构造请求，设置回调函数
        yield scrapy.Request(url=self.user_url.format(user=self.start_user), callback=self.parse_user)
        # yield scrapy.Request(url=self.followees_url.format(user=self.start_user, include=self.followees_query, offset=0, limit=20), callback=self.parse_followees)
        # yield scrapy.Request(url=self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20), callback=self.parse_followers)

    def parse_user(self, response):
        #获取到当前用户返回的信息
        result = json.loads(response.text)
        item = UserItem()
        #获取用户个人信息，此处先获取url，再获取个人信息
        information_url = result['data'][0]['actor']['url']
        information_result = json.loads(requests.get(url=information_url, headers=DEFAULT_REQUEST_HEADERS).text)
        #循环将信息存入item
        for field in item.fields:
            if field in information_result.keys():
                item[field] = information_result.get(field)
        #返回item
        yield item

        #关注的人
        yield scrapy.Request(url=self.followees_url.format(user=result.get('url_token'), include=self.followees_query, offset=0, limit=20), callback=self.parse_followees)
        #粉丝
        yield scrapy.Request(url=self.followers_url.format(user=result.get('url_token'), include=self.followers_query, offset=0, limit=20), callback=self.parse_followers)



    def parse_followees(self, response):
        #获取关注对象以及对象个人信息
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token')), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(url=next_page, callback=self.parse_followees)


    def parse_followers(self, response):
        #获取粉丝，调用回调函数parse_user，获取个人信息
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token')), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(url=next_page, callback=self.parse_followers)

