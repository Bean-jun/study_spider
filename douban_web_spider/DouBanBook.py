# -*- coding:utf-8 -*-
import re
import threading
import time
from random import randint
import pymongo
import requests
from lxml import etree
from tqdm import tqdm


class DouBanBook():
    '''豆瓣书评、摘录、读书笔记抓取'''
    def __init__(self, *args):
        self.book_id = args
        self.base_url = 'https://book.douban.com/subject/'
        self.book_content_url = [] # 获取图书主页url
        self.book_original_url = [] # 获取图书原文摘录url
        self.book_comments_url = [] # 获取图书评论url
        self.book_notes_url = [] # 获取图书笔记url
        self.book_name = [] # 获取书名
        self.proxy = {
            'http':'http://127.0.0.1:8080'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        }

    def config_url(self):
        '''配置起始抓取网页地址'''
        print('配置起始地址...')
        for book_id in tqdm(self.book_id):
            # 配置起始地址
            temp = self.base_url + str(book_id)
            self.book_content_url.append(temp)
            self.book_original_url.append(temp + '/blockquotes')
            self.book_comments_url.append(temp + '/reviews')
            self.book_notes_url.append(temp + '/annotation')

    def get_book_content(self):
        '''主页内容'''
        print("获取主页内容...")
        for url in tqdm(self.book_content_url):
            time.sleep(randint(1, 5))
            r = requests.get(url,headers=self.headers)
            if r.status_code == 200:
                html = etree.HTML(r.text)
                book_name = html.xpath('//*[@property="v:itemreviewed"]/text()')
                author = html.xpath('//*[@id="info"]//a[1]/text()')
                comment_num = html.xpath('//*[@property="v:average"]/text()')
                content_show = html.xpath('//*[@class="related_info"]//*[@class="intro"][1]//p[1]/text()')[0]
                self.book_name.append(book_name[0])
                temp = self.standardization_data(content_show)
                if self.get_mongo('book_content',book_name[0]):
                    self.save_mongo('book_content', book_name=book_name[0], author=author[0], commnet_num=comment_num[0], content_show=str(temp[0]))
                print('主页内容' + str(self.book_content_url.index(url) + 1) + '已保存...')
            else:
                print('error!!!')
        
    def get_book_original(self):
        '''原文摘录'''
        print('获取原文摘录...')
        for original_url in self.book_original_url:
            time.sleep(randint(1, 2))
            r = requests.get(original_url,headers=self.headers)
            if r.status_code == 200:
                html = etree.HTML(r.text)
                page = html.xpath('//*[@class="paginator"]/a[10]/text()')
                # 制作新的url
                url_list = []
                for i in range(0, int((int(page[0])-1)*20+1), 20):
                    url_list.append(original_url + '?sort=score&start=' + str(i))
                for url in tqdm(url_list):
                    time.sleep(randint(1,3))
                    r = requests.get(url, headers=self.headers)
                    if r.status_code == 200:
                        html = etree.HTML(r.text)
                        original = html.xpath('//*[@class="blockquote-list score bottom-line"]//li/figure/text()[1]')
                        for i in original:
                            temp = self.standardization_data(i)
                            if temp:
                                self.save_mongo('original', book_name=self.book_name[self.book_original_url.index(original_url)], original=str(temp[0]))
                        print('第' + str(url_list.index(url) + 1) + '页写入完成...')
                    else:
                        print('error!!!')
            else:
                print('error!!!')
    
    def get_book_comments(self):
        '''书评'''
        print('获取书评...')
        for comments_url in self.book_comments_url:
            time.sleep(randint(1, 2))
            r = requests.get(comments_url,headers=self.headers)
            if r.status_code == 200:
                html = etree.HTML(r.text)
                page = html.xpath('//*[@class="paginator"]/a[10]/text()')
                # 制作新的url
                url_list = []
                for i in range(0, int((int(page[0])-1)*20+1), 20):
                    url_list.append(comments_url + '?start=' + str(i))
                for url in tqdm(url_list):
                    time.sleep(randint(1,3))
                    r = requests.get(url, headers=self.headers)
                    if r.status_code == 200:
                        html = etree.HTML(r.text)
                        comments = html.xpath('//*[@class="review-list  "]//*[@class="short-content"]/text()')
                        for i in comments:
                            temp = self.standardization_data(i)
                            if temp[0]:
                                self.save_mongo('comments', book_name=self.book_name[self.book_comments_url.index(comments_url)], comments=str(temp[0]))
                        print('第' + str(url_list.index(url) + 1) + '页写入完成...')
                    else:
                        print('error!!!')
            else:
                print('error!!!')

    def get_book_notes(self):
        '''读书笔记'''
        print('获取笔记...')
        for notes_url in self.book_notes_url:
            time.sleep(randint(1, 2))
            r = requests.get(notes_url,headers=self.headers)
            if r.status_code == 200:
                html = etree.HTML(r.text)
                page = html.xpath('//*[@class="paginator"]/a[10]/text()')
                # 制作新的url
                url_list = []
                for i in range(0, int((int(page[0])-1)*20+1), 20):
                    url_list.append(notes_url + '?start=' + str(i))
                for url in tqdm(url_list):
                    time.sleep(randint(1,3))
                    r = requests.get(url, headers=self.headers)
                    if r.status_code == 200:
                        html = etree.HTML(r.text)
                        notes = html.xpath('//*[@class="comments by_rank"]//*[@class="short"]/span/text()')
                        for i in notes:
                            temp = self.standardization_data(i)
                            if temp:
                                self.save_mongo('notes', book_name=self.book_name[self.book_notes_url.index(notes_url)], notes=str(temp[0]))
                        print('第' + str(url_list.index(url) + 1) + '页写入完成...')
                    else:
                        print('error!!!')
            else:
                print('error!!!')

    def save_mongo(self, collection, **kwargs):
        '''保存到mongo数据库'''
        client = pymongo.MongoClient('localhost', 27017)
        db = client['DouBanBook']
        col = db[collection]
        col.insert_one(kwargs)

    def get_mongo(self, collection,book_name):
        '''获取mongo数据库数据'''
        client = pymongo.MongoClient('localhost', 27017)
        db = client['DouBanBook']
        col = db[collection]
        if not col.find_one({},{'book_name':book_name[0]}):
            return True
        else:
            return False

    def save_mysql(self):
        '''保存到mysql数据库'''
        pass
    
    def standardization_data(self, *args):
        '''清洗数据'''
        temp = []
        for i in args:
            ret = re.sub('◎|p\d|\s+|n|\(|xa0|\\\\|\……|（|）|\)', '', str(i))
            temp.append(ret)
        return temp
 
    def run(self):
        # 获取到url
        self.config_url()
        # 获取主页内容
        self.get_book_content()
        # 获取原文摘录
        t1 = threading.Thread(target=self.get_book_original)
        # 获取书评
        t2 = threading.Thread(target=self.get_book_comments)
        # 获取读书笔记
        t3 = threading.Thread(target=self.get_book_notes)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        print('-'*20 + '爬取结束' + '-'*20)
  

if __name__ == '__main__':
    douban = DouBanBook(33440205)
    douban.run()
