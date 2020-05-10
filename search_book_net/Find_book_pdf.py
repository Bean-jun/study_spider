import json
import re
import time
import requests


class CrawlBookPdf():
    def __init__(self,name):
        self.name = name
        self.time = int(1000*time.time())
        self.url = ['https://www5.jiumodiary.com/init_hubs.php','https://www.jiumodiary.com/ajax_fetch_hubs.php']
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }


    def __get_id(self):
        '''获取请求中的id'''
        data = {
            'q': self.name,
            'remote_ip':'',
            'time_int': self.time
        }
        r = requests.post(self.url[0],data=data,headers=self.headers)
        return r.content

    def __get_content(self):
        js = json.loads(self.__get_id())
        if js['status'] == 'succeed':
            data = {
                'id':js['id'],
                'set':0
            }
            r = requests.post(self.url[1],data=data,headers=self.headers)
            return r.content

    def __clear_data(self):
        '''获取json数据'''
        js = json.loads(self.__get_content())
        if js['status'] == 'succeed':
            while js['sources'] != None:
                try:
                    now = js['sources'].pop()
                    num = len(now['details']['data'])
                    for i in range(0, num):
                        link = now['details']['data'][i]['link']
                        title = now['details']['data'][i]['title']
                        desc = now['details']['data'][i]['des']
                        title = re.sub('</*.+>','',str(title))
                        desc = re.sub('</*.+>','',str(desc))
                        print(link + '      '+ title + '      '+ desc)
                        print('~'*60)
                except:
                    break

    @property
    def run(self):
        self.__clear_data()


if __name__ == '__main__':
    bookname = input('请输入书名：')
    book = CrawlBookPdf(bookname)
    book.run