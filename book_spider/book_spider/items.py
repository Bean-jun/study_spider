# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookSpiderItem_MeiRiYiWen(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()

class BookSpiderItem_A69Novel(scrapy.Item):
    novel_name = scrapy.Field()
    novel_chapter = scrapy.Field()  
    novel_content = scrapy.Field() 
    _id = scrapy.Field()