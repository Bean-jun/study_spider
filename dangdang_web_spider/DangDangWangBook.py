# -*- coding:utf-8 -*-

import re
import time
from random import randint
import pymongo
import requests
from lxml import etree
from tqdm import tqdm


class DangDangWangBook(object):
    '''当当网图书畅销榜抓取'''
    def __init__(self):
        self.page = 0
        self.book_name = []
        self.book_num = []
        self.hot = []
        self.author = []
        self.press = []
        self.price = []
        self.url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        }
    
    def remove_impurities(self,page):
        '''祛除杂质'''
        ret = re.search('\d+', str(page)).group()
        self.page = ret
    
    def add_value(self,book_name,book_num,hot,author,press,price):
        '''整合数据'''
        self.book_name.append(book_name)
        self.book_num.append(book_num)
        self.hot.append(hot)
        self.author.append(author)
        self.press.append(press)
        self.price.append(price)

    def get_page(self):
        '''获取页码'''
        Response = requests.get(self.url,headers=self.headers)
        r = etree.HTML(Response.text)
        page = r.xpath('//*[@class="data"]/span[2]/text()')
        self.remove_impurities(page)
     
    def get_more_content(self):
        '''获取内容'''
        print('抓取中，请稍后...')
        for i in tqdm(range(1, int(self.page)+1)):
            time.sleep(randint(1, 5))
            new_url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-'
            self.url = new_url + str(i)
            Response = requests.get(self.url,headers=self.headers)
            r = etree.HTML(Response.text)
            book_name = r.xpath('//*[@class="name"]/a/@title')
            book_num = r.xpath('//*[@class="bang_list clearfix bang_list_mode"]/li/div[1]/text()')
            hot = r.xpath('//*[@class="tuijian"]/text()')
            author = r.xpath('//*[@class="publisher_info"]/a[1]/@title')
            temp = r.xpath('//*[@class="publisher_info"]/a[1]/text()')
            press = []
            for i in temp:
                if temp.index(i) % 2 == 1:
                    press.append(i)
            price = r.xpath('//*[@class="price"]/p[1]/span[1]/text()')
            self.add_value(book_name,book_num,hot,author,press,price)

    def standardization(self):
        '''规格化数据'''
        print('规格化数据中...')
        book_name, book_num, hot, author,press, price = [], [], [], [], [], []
        for i in tqdm(range(len(self.book_name))):
            book_name += self.book_name[i]
            book_num += self.book_num[i]
            hot += self.hot[i]
            author += self.author[i]
            press += self.press[i]
            price += self.price[i]
        self.book_name, self.book_num, self.hot, self.author, self.press, self.price = book_name, book_num, hot, author, press, price
    
    def cleaning(self):
        '''清洗'''
        print('清洗数据中...')
        book_name, book_num, hot, author,press, price = [], [], [], [], [], []
        for i in tqdm(self.book_name):
            book_name_ret = re.sub('（.*）','', i)
            book_name.append(book_name_ret)
        book_num = re.findall('[0-9]+', str(self.book_num))
        hot = re.findall('[0-9\.]+%', str(self.hot))
        for i in tqdm(self.author):
            author_ret = re.sub('\u3000|�+|出品','', i)
            author.append(author_ret)
        for i in tqdm(self.price):
            price_ret = re.search('\d.+', i)
            price.append(price_ret.group())
        self.book_name, self.book_num, self.hot, self.author, self.price = book_name, book_num, hot, author, price

    def save_mongo(self):
        '''保存到MongoDB'''
        print('开始写入MongoDB...')
        cliect = pymongo.MongoClient('localhost', 27017)
        db = cliect['DDbook']
        collection = db['book']
        collection.delete_many({})
        for content in tqdm(self.book_name):
            index = self.book_name.index(content)
            try:
                collection.insert_one({'_id':self.book_num[index],'hot':self.hot[index],'book_name':content,'author':self.author[index],'press':self.press[index],'price':self.price[index]})
            except:
                pass
        print('完成！')

    def save_txt(self):
        '''保存到txt文件'''
        print('开始写入当当网图书销量排行榜...')
        big_list = []
        for content in tqdm(self.book_name):
            small_list = []
            index = self.book_name.index(content)
            small_list = self.book_num[index] + ' ' + '热度：'+  self.hot[index] + ' ' + content + ' ' + self.author[index] + ' ' + self.press[index] + ' ' + '售价：'+ self.price[index]
            big_list.append(small_list)
        with open('当当网图书销量排行榜.txt','w',encoding="utf-8") as f:
            for i in big_list:
                f.write(i + '\n')
        print('完成！')
                        
    def model(self,flat):
        '''保存数据模式'''
        if flat == '1':
            self.save_txt()
        else:
            self.save_mongo()
        
    def run(self,flat):
        self.get_page()
        self.get_more_content()
        self.standardization()
        self.cleaning()
        self.model(flat)


if __name__ == "__main__":
    print('获取当当网站图书销量排行榜！')
    flat = input('请输入你要保存的模式：1为txt文档，2为MongoDB数据库：\n')
    book = DangDangWangBook()
    book.run(flat)
