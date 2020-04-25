# 学习基本的网络爬虫

1. [妹子图爬取](meizi_web_spider/spider_mm.py)  

    - 在get_page_link方法中有个限制，取消后可以直接爬取全站分页，否则只能爬取全站分页的52页。

    - Windows系统电脑可以直接运行这个[文件](meizi_web_spider/dist/spider_mm.exe)

    - 加入[每日一爬](meizi_web_spider/everyday_spider_mm.py)功能(只爬取每日更新图片)
  
2. [有道翻译](youdao_web_spider/YouDaoTranslate.py)

    - 抓取移动端的有道词典，实时进行翻译

    - 和第一个妹子图不同的请求方式，你可以看到使用post请求返回的结果

    - 开始尝试使用面向对象的思路写爬虫程序

3. [当当书城畅销书排行](dangdang_web_spider/DangDangWangBook.py)
   
   - 抓取当当网站畅销书排行(ps:还是要多读书额)
     - 另外附赠4月25日抓取的[数据](dangdang_web_spider/当当网图书销量排行榜.txt)

   - 使用两种方式保存抓取到的数据

     - 使用txt格式时，什么都不需要做，只要运行就好

     - 使用MongoDB时，需要额外安装Mongo数据库和pymongo

   - 抓取时，使用的xpath如下：

        ```
        # 页码 //*[@class="data"]/span[2]/text()
        # 对应排行 //*[@class="bang_list clearfix bang_list_mode"]/li/div[1]/text()
        # 书名 //*[@class="name"]/a/@title
        # 推荐度 //*[@class="tuijian"]/text()
        # 作者 //*[@class="publisher_info"]/a[1]/@title
        # 出版社 //*[@class="publisher_info"]/a[1]/text()  ### 注意：偶数个才是出版社名
        # 价格 //*[@class="price"]/p[1]/span[1]/text()
        ```


## 待办事件

- 将妹子图使用面向对象的思路重构代码
- 加入更多的爬虫项目
- 适当加入一些爬虫项目中的经验