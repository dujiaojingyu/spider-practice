# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider


class Zhihu1Spider(CSVFeedSpider):
    name = 'zhihu1'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/feed.csv']
    # headers = ['id', 'name', 'description', 'image_link']
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        i = {}
        #i['url'] = row['url']
        #i['name'] = row['name']
        #i['description'] = row['description']
        return i
