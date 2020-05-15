# -*-encoding：UTF-8 -*-
from selenium import webdriver
import time

web = webdriver.Chrome()
web.get('https://mail.163.com/')
iframe = web.find_element_by_tag_name('iframe')

web.switch_to_frame(iframe)

# 模拟登陆
account = input('你的邮箱账号：')
password = input('你的密码：')
address = input('收件人地址：')
topic = input('邮件主题：')
content = input('邮件内容：\n')
web.find_element_by_name('email').send_keys(account)
web.find_element_by_name('password').send_keys(password)
time.sleep(3)
web.find_element_by_id('dologin').click()

web.switch_to.default_content()
time.sleep(5)
# 写信
xx_butten = web.find_elements_by_xpath('//li[@hidefocus="hidefocus"]')[1].click()
time.sleep(5)
web.find_element_by_class_name('nui-editableAddr-ipt').send_keys(address)
zt = web.find_elements_by_class_name('nui-ipt-input')[2].send_keys(topic)
iframe = web.find_elements_by_tag_name('iframe')[3]

web.switch_to_frame(iframe)
time.sleep(1)
web.find_element_by_class_name('nui-scroll').send_keys(content)
web.switch_to.default_content()
time.sleep(1)
web.find_element_by_class_name('nui-toolbar-item').click()
web.quit()