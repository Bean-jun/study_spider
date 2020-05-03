# -*- coding: utf-8 -*-
import scrapy
import time
from random import randint
from book_spider.items import BookSpiderItem

class MeiriyiwenSpider(scrapy.Spider):
    name = 'meiriyiwen'
    allowed_domains = ['meiriyiwen.com']
    start_urls = ['https://meiriyiwen.com/random']

    def parse(self, response):
        item = BookSpiderItem()
        item['name'] = response.xpath('//h1/text()').extract_first()
        item['author'] = response.xpath('//p[@class="article_author"]//span/text()').extract_first()
        item['text'] = response.xpath('//div[@class="article_text"]').extract()
        new_url = response.xpath('//div[@class="random_box"]/a/@href').extract_first()
        time.sleep(randint(1,3))
        yield scrapy.Request(
            new_url,
            callback=self.parse,
            dont_filter=True
        )
        yield item