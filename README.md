# 学习基本的网络爬虫

1. [妹子图爬取](meizi_web_spider/spider_mm.py)  

    - 在get_page_link方法中有个限制，取消后可以直接爬取全站分页，否则只能爬取全站分页的52页。

    - Windows系统电脑可以直接运行这个[文件](meizi_web_spider/dist/spider_mm.exe)

    - 加入[每日一爬](meizi_web_spider/everyday_spider_mm.py)功能(只爬取每日更新图片)
  
2. [有道翻译](youdao_web_spider/YouDaoTranslate.py)

    - 抓取移动端的有道词典，实时进行翻译

    - 和第一个妹子图不同的请求方式，你可以看到使用post请求返回的结果

    - 开始尝试使用面向对象的思路写爬虫程序

## 待办事件

- 将妹子图使用面向对象的思路重构代码
- 加入更多的爬虫项目
- 适当加入一些爬虫项目中的经验