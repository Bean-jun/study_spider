# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re
cliect = MongoClient()
db = cliect['book_spider']

class BookSpiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'meiriyiwen':
            collection = db['meiriyiwen']
            temp = [re.sub('</*p>|\\.*|</*div>|\s|<div class="article_text">', '', i) for i in item['text']]
            item['text'] = temp[0]
            collection.insert(dict(item))
            print('ok')
        return item
