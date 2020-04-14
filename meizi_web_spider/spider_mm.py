import random
import re
import time
import requests
from lxml import etree
import os

headers = {
    'accept-encoding':'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.mzitu.com/',
    'cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1586682048,1586697823,1586749867; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1586749931',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
}

def fix_headers_page(number_page):
    '''修复referer，请求主页妹子时使用'''
    headers_01 = {
    'accept-encoding':'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.mzitu.com/xinggan/page/'+ number_page,
    'cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1586682048,1586697823,1586749867; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1586749931',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }
    return headers_01

def fix_headers_s(word):
    '''修复referer，请求一组妹子图时使用'''
    headers_01 = {
    'accept-encoding':'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.mzitu.com/'+ word,
    'cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1586682048,1586697823,1586749867; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1586749931',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }
    return headers_01

def fix_headers(word):
    '''修复referer，请求每张照片使用'''
    headers_01 = {
    'accept-encoding':'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.mzitu.com/'+ word,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }
    return headers_01

url = 'https://www.mzitu.com/xinggan/'

def create(addr):
    '''创建目录'''
    creat_dir = []
    page_link_s,count = get_main_link()
    page_link_s_two = get_page_link()
    for page in page_link_s:
        pattern = re.compile(r'\d{6,10}')
        number = re.findall(pattern, page)
        word = number[0]
        creat_dir.append(word)
    for page in page_link_s_two:
        pattern = re.compile(r'\d{6,10}')
        number = re.findall(pattern, page)
        word = number[0]
        creat_dir.append(word)
    for i in creat_dir: 
        os.makedirs(addr+'/'+str(i)) 

def get_main_link():
    '''获取性感妹子主页图的链接'''
    r = requests.get(url,headers=headers)
    html = etree.HTML(r.text)
    page_link = html.xpath('//*[@id="pins"]//span/a/@href')
    page_count_link = html.xpath('//*[@class="page-numbers"][4]/@href')
    pattern = re.compile(r'\d{1,4}')
    count = re.findall(pattern, page_count_link[0])[0]
    print(page_count_link,count)
    return page_link,count

def get_page_link():
    '''获取每一页的链接以便获取每页中妹子的组图的链接'''
    new_urls = []
    page_link, count = get_main_link()
    tag = 51
    if int(count) > int(tag):
        count = tag
    page_count_link = []
    url = 'https://www.mzitu.com/xinggan/page/' 
    for page in range(2,int(count)):
        temp = url + str(page)
        new_urls.append(temp)
    for new_url in new_urls:
        time.sleep(1)
        pattern = re.compile(r'\d{1,4}')
        number_page_temp = re.findall(pattern, new_url)
        number_page = number_page_temp[0]
        header = fix_headers_page(number_page)
        r = requests.get(new_url,headers=header)

        html = etree.HTML(r.text)
        page_link_count = html.xpath('//*[@id="pins"]//span/a/@href')
        if page_link_count:
            page_count_link.append(page_link_count[0])
    return page_count_link

def get_photo_one_link(page_link):
    '''获取单个妹子内部连接及页码'''
    create(os.getcwd())
    new_urls = []
    page = []
    for i in page_link:
        # 重做headers
        pattern = re.compile(r'\d{6,10}')
        number_num = re.findall(pattern, i)

        words_words = number_num[0]

        r = requests.get(i,headers=fix_headers_s(words_words))
        time.sleep(random.randint(1,5))
        html = etree.HTML(r.text)

        # 获取页码
        get_zong_page = html.xpath('//*[@class="pagenavi"]//a/@href')

        numberss = get_zong_page[-2][-2:]
        # print(numberss)

        int_num = int(numberss)
        for num in range(2,int_num):
            page.append(num)
            num_url = i+'/'+ str(num)
            new_urls.append(num_url)
        # print(new_urls) # 每个总图下每个妹子的图的总链接

        for new_url in new_urls:
            # 获取单张图片的链接
            # 重做headers
            index_s = new_urls.index(new_url) + 2
            pattern = re.compile(r'\d{6,10}')
            number = re.findall(pattern, new_url)
            word = '/' +number[0]+ '/' + str(index_s)

            # 启用新的头部文件
            header = fix_headers(word)
            
            rr = requests.get(new_url,headers=header)
            # time.sleep(random.randint(1,5))
            html_01 = etree.HTML(rr.text)
            # 提取每页中的图片下载link
            links = html_01.xpath('//*[@class="main-image"]//img/@src')
            
            # print(links)
            for link in links:
                filename = number[0]+ '/' +link[-9:]
                print(link[-9:])
                with open(filename,'wb') as f:
                    # time.sleep(random.randint(1,2))
                    time.sleep(1)
                    ret = requests.get(link,headers=header)
                    f.write(ret.content)
        new_urls = []

        
if __name__ =='__main__':
    print('开始下载...')
    page_link, count = get_main_link()   # 这个爬全部妹子的图  
    get_photo_one_link(page_link) # 获取第一页的妹子图

    page_link_ss = get_page_link()
    get_photo_one_link(page_link_ss) # 获取后续妹子的图
    print('下载结束！！！！')