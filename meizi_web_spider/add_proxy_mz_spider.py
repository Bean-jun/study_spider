# -*- coding:UTF-8 -*-
import requests
import time
from lxml import etree
from tqdm import tqdm
import re
import threading
import random
from pool import GetProxiesPool

class MeiZiSpider(GetProxiesPool):
    '''妹子爬虫'''
    def __init__(self):
        super().__init__()
        self.url = 'https://www.mzitu.com/'
        self.page_url = []
        self.page_photo_link = [] # 主图链接
        self.photo_name = [] # 主图名称
        self.photo_url = [] # 图片链接
        self.user_agent = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"
            ]
        self.proxy = self.main()

    @property
    def _set_proxy(self):
        '''配置代理'''
        fake_proxy = {
            'https':random.choice(self.proxy)
         }     
        proxy = {

         }   
        return random.choice([fake_proxy, proxy])

    def _headers(self,word):
        '''配置请求头'''
        headers = {
            'accept-encoding':'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://www.mzitu.com/' + word,
            'user-agent': random.choice(self.user_agent),
        }
        return headers

    def _get_page(self,word):
        '''获取对应栏总页数'''
        r = requests.get(self.url + word,headers=self._headers(word), proxies=self._set_proxy)
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
            r = requests.get(url, headers=self._headers(word),proxies=self._set_proxy)
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
            r = requests.get(url, headers=self._headers(word),proxies=self._set_proxy)
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

    def save_photo(self,more_url):
        for url in tqdm(more_url):
            index = more_url.index(url) + 1
            pattern = re.compile(r'\d{6,10}')
            page_photo_id_s = re.findall(pattern, url)
            page_photo_id = page_photo_id_s[0]
            k_word =  page_photo_id + '/' + str(index)
            try:
                r = requests.get(url, headers=self._headers(k_word),proxies=self._set_proxy)
                html = etree.HTML(r.text)
                photo_link = html.xpath('//*[@class="main-image"]//img/@src')
                filename = photo_link[0][-9:]
                with open(filename,'wb') as f:
                    time.sleep(2)
                    r = requests.get(photo_link[0], headers=self._headers(k_word),proxies=self._set_proxy)
                    f.write(r.content)
            except:
                pass
        
    def mult_threading(self, word):
        full_url = self._get_photo_link(word)
        mid = len(full_url) // 2
        t1 = threading.Thread(target=self.save_photo, args=(full_url[0:mid],))
        t2 = threading.Thread(target=self.save_photo, args=(full_url[mid:-1],))
        new_list = [t1, t2]
        for i in new_list:
            i.start()
        for j in new_list:
            j.join()

    def start_run(self, num):
        if num == '1':
            self.mult_threading('xinggan/')
        elif num == '2':
            self.mult_threading('japan/')
        elif num == '3':
            self.mult_threading('taiwan/')
        elif num == '4':
            self.mult_threading('mm/')
        else:
            pass

if __name__ == '__main__':
    mz = MeiZiSpider()
    msg = input('输入你想抓取的类型：1.性感妹子；2.日本妹子；3.台湾妹子；4.清纯妹子，输入对应序号即可！\n')
    mz.start_run(msg)