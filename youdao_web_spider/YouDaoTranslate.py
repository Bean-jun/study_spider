import time
import requests
from lxml import etree


class YouDaoTranslate(object):
    def __init__(self, content):
        self.content = content
        self.url = 'http://m.youdao.com/translate'
        self.data = {
            'inputtext': self.content,
            'type': 'AUTO',
            }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

    def get_translate_content(self):
        '''获取结果并分析'''
        response = requests.post(
            url=self.url,
            headers=self.headers,
            data=self.data
        )
        html = etree.HTML(response.text)
        translate  = html.xpath('//*[@id="translateResult"]/li/text()')[0]
        return translate

    def run(self):
        '''运行程序'''
        t = self.get_translate_content()
        print(t+'\n')


if __name__ == '__main__':
    print('--结束运行请使用Ctrl+C')
    while  True:
        content = input("请输入您要翻译的内容(中英文皆可):\n")
        translater = YouDaoTranslate(content)
        translater.run()
        time.sleep(1.25)
