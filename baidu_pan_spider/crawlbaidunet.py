# -*- coding:utf-8 -*-
import requests
from lxml import etree
import time
import re

class CrawlBaiDu():
    def __init__(self,keyword):
        self.keyword = keyword
        self.url = 'https://www.luomapan.com/search?keyword=' + self.keyword
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

    def get_data(self):
        r = requests.get(self.url,headers=self.headers)
        if r.status_code == 200:
            html = etree.HTML(r.text)
            title = html.xpath('//h1/a/text()')
            link = html.xpath('//h1/a/@href')
            print(content)
            for i in title:
                index = title.index(i)
                url = 'https://www.luomapan.com'

                new_url = url + link[index]
                r = requests.get(new_url,headers=self.headers)
                time.sleep(2)
                if r.status_code == 200:
                    html = etree.HTML(r.text)
                    verify = html.xpath('//span[@class="meta-item copy-item"]//text()')
                    desc_link = html.xpath('//div[@class="button-inner"]/a/@href')
                    # print(verify)
                    print('-'*80)
                    if len(verify) == 0:
                        print('|' + i + '\n' +'|' + '链接：' + desc_link[0]) 
                    else:
                        ver = re.sub('\n|\s','',verify[1])
                        print('|' + i + '\n'+'|' + '验证码：' + ver + '\n' + '|' + '链接：' + desc_link[0]) 
                    print('-'*80)


if __name__ == '__main__':
    while True:
        content = input('输入：\n')
        if content == '@@':
            break
        else:
            crawl = CrawlBaiDu(content)
            crawl.get_data()
