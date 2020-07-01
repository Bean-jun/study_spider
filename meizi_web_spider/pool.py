import re
import time
import requests
from lxml import etree


class GetProxiesPool(object):
    '''获取免费代理IP'''
    def __init__(self):
        self.base_url = ['http://www.data5u.com/','http://www.66ip.cn/index.html',
                        'https://www.kuaidaili.com/free/inha/','https://www.kuaidaili.com/free/intr/',
                        'http://www.ip3366.net/',
                        ]
        self.ip = []
        self.port = []
        self.net_type = []
        self.key = []
        self.value = []
        self.new_dic = {}
        self.use_head = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        }
        self.full_ip = []
    
    def get_data5u_ip_port(self):
        '''获取http://www.data5u.com/网站中的免费IP'''
        r = requests.get(self.base_url[0],headers=self.headers)
        html = etree.HTML(r.text)
        ip = html.xpath('//*[@class="l2"]/span[1]/li/text()')
        port = html.xpath('//*[@class="l2"]/span[2]/li/text()')
        net_type = html.xpath('//*[@class="l2"]/span[4]/li/text()')
        self.ip.append(ip)
        self.port.append(port)
        self.net_type.append(net_type)
    
    def get_66ip_ip_port(self):
        '''获取http://www.66ip.cn/index.html网站中的免费IP'''
        r = requests.get(self.base_url[1],headers=self.headers)
        html = etree.HTML(r.text)
        ip = html.xpath('//*[@id="main"]//tr/td[1]/text()')[1:]
        port = html.xpath('//*[@id="main"]//tr/td[2]/text()')[1:]
        temp = len(ip)
        net_type = ['http'] * temp
        self.ip.append(ip)
        self.port.append(port)
        self.net_type.append(net_type)

    def get_kuaidaili_ip_port(self):
        '''获取https://www.kuaidaili.com/free网站中的免费IP'''
        r = requests.get(self.base_url[2],headers=self.headers)
        html = etree.HTML(r.text)
        ip_01 = html.xpath('//*[@class="table table-bordered table-striped"]//td[1]/text()')
        port_01 = html.xpath('//*[@class="table table-bordered table-striped"]//td[2]/text()')
        net_type_01 = html.xpath('//*[@class="table table-bordered table-striped"]//td[4]/text()')
        self.ip.append(ip_01)
        self.port.append(port_01)
        self.net_type.append(net_type_01)

        time.sleep(3)
        r = requests.get(self.base_url[3],headers=self.headers)
        html = etree.HTML(r.text)
        ip_02 = html.xpath('//*[@class="table table-bordered table-striped"]//td[1]/text()')
        port_02 = html.xpath('//*[@class="table table-bordered table-striped"]//td[2]/text()')
        net_type_02 = html.xpath('//*[@class="table table-bordered table-striped"]//td[4]/text()')
        self.ip.append(ip_02)
        self.port.append(port_02)
        self.net_type.append(net_type_02)

    def get_ipnet_ip_port(self):
        '''获取http://www.ip3366.net/网站中的免费IP'''
        r = requests.get(self.base_url[4],headers=self.headers)
        html = etree.HTML(r.text)
        ip = html.xpath('//*[@class="table table-bordered table-striped"]//td[1]/text()')
        port = html.xpath('//*[@class="table table-bordered table-striped"]//td[2]/text()')
        net_type = html.xpath('//*[@class="table table-bordered table-striped"]//td[4]/text()')
        self.ip.append(ip)
        self.port.append(port)
        self.net_type.append(net_type)
    
    def run(self):
        '''运行'''
        print('开始获取...')
        self.get_data5u_ip_port()
        self.get_66ip_ip_port()
        self.get_kuaidaili_ip_port()
        self.get_ipnet_ip_port()
        ip = []
        print("ok!")
        for j in range(5):
            for i in range(len(self.net_type[j])):
                new_str = self.net_type[j][i]  + '://' + self.ip[j][i] + ':' + self.port[j][i]
                # new_str = self.net_type[j][i] + ':' + self.net_type[j][i]  + '://' + self.ip[j][i] + ':' + self.port[j][i]
                ip.append(new_str)
        return ip

    def test_ip(self,ip, test_url='https://www.baidu.com/', time_out=2):
        proxies = {'https': ip} 
        j = 0
        while j < 2: 
            try:
                r = requests.get(test_url, proxies=proxies, timeout=time_out)
                if r.status_code == 200:
                    print('测试通过%s' % ip)
                    self.full_ip.append(ip) 
                    break
                else:
                    print('请求失败%s' % ip)
            except:
                print('请求过程错误%s' % ip)
            j += 1
        return self.full_ip

    def main(self):
        proxy= self.run()
        for i in proxy:
            print(i)
            self.test_ip(i)
        return self.full_ip

if __name__ == '__main__':
    pool = GetProxiesPool()
    ip = pool.main()
    print('可以使用的IP:')
    print(ip)