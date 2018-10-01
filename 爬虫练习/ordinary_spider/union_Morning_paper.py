import scrapy

class StackOverFlowSpide(scrapy.Spider):
    """docstring for StackOverFlowSpide"""
    name = 'stackoverflow'
    start_urls = ['http://www.uzbzw.com/plus/list.php?tid=28']

    def parse(self,response):
        for href in response.css('w960 li a::attr(href)'):
            print('href>>>>>>',href)
            full_url = response.urljoin(href.extract())
            print('full_url>>>>>',full_url)
            yield scrapy.Request(full_url,callback=self.parse_question)
    
    def parse_question(self,response):
        yield {
        'title':response.css('h2::text').extract()[0],
        'time':response.css('.w960 .info::text').extract()[0],
        'body':response.css('.w960 .content::text').extract()[0],
        'link':response.url,
        }            
        