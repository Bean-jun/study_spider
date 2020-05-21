# -*- coding:UTF-8 -*-
import requests
import time
from lxml import etree
from tqdm import tqdm
import re
import threading

class MeiZiSpider():
    '''妹子爬虫'''
    def __init__(self):
        self.url = 'https://www.mzitu.com/'
        self.page_url = []
        self.page_photo_link = [] # 主图链接
        self.photo_name = [] # 主图名称
        self.photo_url = [] # 图片链接

    def _headers(self,word):
        '''配置请求头'''
        headers = {
            'accept-encoding':'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://www.mzitu.com/' + word,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
        }
        return headers

    def _get_page(self,word):
        '''获取对应栏总页数'''
        r = requests.get(self.url + word,headers=self._headers(word))
        html = etree.HTML(r.text)
        page = html.xpath('//a[@class="page-numbers"][4]/text()')
        # page = html.xpath('//a[@class="page-numbers"][1]/text()')
        return page

    def _get_page_link(self,word):
        '''使用获取到的pages来构造页码'''
        pages = self._get_page(word)
        for page in range(1, int(pages[0])+1):
            temp = self.url + word + str(page)
            self.page_url.append(temp)
        return self.page_url

    def _get_page_photo_link(self,word):
        '''获取每页中妹纸图的链接地址'''
        self._get_page_link(word)
        for url in tqdm(self.page_url):
            time.sleep(1)
            r = requests.get(url, headers=self._headers(word))
            try:
                if r.status_code == 200:
                    html = etree.HTML(r.text)
                    page_photo_link = html.xpath('//*[@id="pins"]//span/a/@href')
                    photo_name = html.xpath('//*[@id="pins"]//span/a/text()')
                    self.page_photo_link.extend(page_photo_link)
                    self.photo_name.extend(photo_name)
            except:
                pass

    def _get_simple_group_photo_page(self,word):
        '''获取一组妹子图片的页数'''
        self._get_page_photo_link(word)
        pages = []
        for url in tqdm(self.page_photo_link):
            time.sleep(1)
            r = requests.get(url, headers=self._headers(word))
            try:
                if r.status_code == 200:
                    html = etree.HTML(r.text)
                    page = html.xpath('//div[@class="pagenavi"]/a[5]/span/text()')
                    pages.extend(page)
            except:
                pass
        return pages

    def _get_photo_link(self,word):
        '''构造每张图的请求地址'''
        pages = self._get_simple_group_photo_page(word)
        for url in self.page_photo_link:
            for page in tqdm(range(1, int(pages[self.page_photo_link.index(url)])+1)):
                temp = url + '/' +str(page)
                self.photo_url.append(temp)
        return self.photo_url

    def save_photo(self,word):
        self._get_photo_link(word)
        for url in tqdm(self.photo_url):
            index = self.photo_url.index(url) + 1
            pattern = re.compile(r'\d{6,10}')
            page_photo_id_s = re.findall(pattern, url)
            page_photo_id = page_photo_id_s[0]
            k_word =  page_photo_id + '/' + str(index)
            try:
                r = requests.get(url, headers=self._headers(k_word))
                html = etree.HTML(r.text)
                photo_link = html.xpath('//*[@class="main-image"]//img/@src')
                filename = photo_link[0][-9:]
                with open(filename,'wb') as f:
                    time.sleep(1)
                    r = requests.get(photo_link[0], headers=self._headers(k_word))
                    f.write(r.content)
            except:
                pass

    def run(self, num):
        if num == '1':
            self.save_photo('xinggan/')
        elif num == '2':
            self.save_photo('japan/')
        elif num == '3':
            self.save_photo('taiwan/')
        elif num == '4':
            self.save_photo('mm/')
        else:
            pass

if __name__ == '__main__':
    mz = MeiZiSpider()
    msg = input('输入你想抓取的类型：1.性感妹子；2.日本妹子；3.台湾妹子；4.清纯妹子，输入对应序号即可！\n')
    mz.run(msg)