# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re
import json
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

        if spider.name == 'a69novel':
            collection = db['a69novel']
            # 去除多余字符和空字符
            temp = [re.sub('\r|\n|(\xa0\xa0\xa0\xa0)', '', str(i)) for i in item['novel_content']]
            t = [i for i in temp if i != '']
            content = ''
            for i in t[1:]:
                content += i
            id = re.findall('\d+', item['_id'][0])[0]
            novel_chapter = re.sub('\d+\.', '', item['novel_chapter'][0])
            item['_id'] = id
            item['novel_content'] = content
            item['novel_chapter'] = novel_chapter
            collection.insert(dict(item))
            print('ok')
        return item
