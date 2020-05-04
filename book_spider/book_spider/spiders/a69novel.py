# -*- coding: utf-8 -*-
import scrapy
import time
from random import randint
from book_spider.items import BookSpiderItem_A69Novel

class A69novelSpider(scrapy.Spider):
    name = 'a69novel'
    allowed_domains = ['69shu.com']
    start_urls = ['https://69shu.com/1464/']

    def parse(self, response):
        temp_link = response.xpath('//div[@class="mu_contain"][2]/ul/li/a/@href').extract()
        for url in temp_link[:-1]:
            yield scrapy.Request(
                str(url),
                callback=self.parse_content
            )

    def parse_content(self, response):
        item = BookSpiderItem_A69Novel()        
        time.sleep(randint(1,3))
        item['_id'] = response.xpath('//td[@valign="top"]/h1/text()').extract()
        item['novel_name'] = response.xpath('//div[@class="weizhi"]//a[3]/text()').extract_first()
        item['novel_chapter'] = response.xpath('//td[@valign="top"]/h1/text()').extract()
        item['novel_content'] = response.xpath('//div[@class="yd_text2"]/text()').extract()
        yield item
        