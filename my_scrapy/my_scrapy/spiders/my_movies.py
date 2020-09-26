import scrapy
# from bs4 import BeautifulSoup
from my_scrapy.items import MyScrapyItem
from scrapy.selector import Selector
from time import sleep
import random


class MyMoviesSpider(scrapy.Spider):
    name = 'my_scrapy'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3&offset=0']


    #   注释默认的parse函数
    #   def parse(self, response):
    #        pass

    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        print("--------------------------------------开始执行----------------------------------------------")
        i = 0
        url = f'https://maoyan.com/films?showType=3&offset={i + 0}'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
        # url 请求访问的网址
        # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
        # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数


    def parse(self, response):    # 解析函数
        try:
            print("--------------------------------------开始解析----------------------------------------------")
            print(response.url)
            # //表示只搜索div，/会真个网页搜索，性能不好。  //*[@id="app"]/div/div[2]/div[2]/dl/dd[1]/div[2]/a
            # movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
            movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
            i = 0
            for movie in movies:
                if i < 10:    # 限制只获取前十个电影。
                    # 路径使用 / .  .. 不同的含义　. 是从当前路径往下找，  .. 是找到统级别标签的下一个标签开始往下找。
                    title = movie.xpath('./a/text()')
                    link = movie.xpath('./a/@href')
                    print('-----------------------------------开始循环1 获取电影名---------------------------------------')
                    # print(title.extract())   # 返回的所有数据，存在一个list里。
                    # print(link.extract())
                    # print(title.extract_first())   # 返回第一个值。
                    # print(link.extract_first())
                    # print(title.extract_first().strip())   # 去掉空格。
                    # item = MyScrapyItem()
                    # item['title'] = title.extract_first().strip()
                    # item['link'] = "https://maoyan.com" + link.extract_first().strip()
                    i = i + 1
                    sleep(random.randint(3, 10))  # 防止被反扒
                    yield scrapy.Request(url=("https://maoyan.com" + link.extract_first().strip()), callback=self.get_details, meta={'title': title.extract_first().strip()}, dont_filter=False)


        except Exception as e:  # 抓取所有错误信息。
            print("-----------------------------------------执行报错-----------------------------------------")
            print(e)


    def get_details(self, response):  # 解析函数
        print(response.url)
        movies = Selector(response=response).xpath('//li[@class="ellipsis"]')
        i = 0
        item = MyScrapyItem()
        for movie in movies:
            print('-----------------------------------开始循环2 获取类型和上映时间---------------------------------------')
            item['title'] = response.meta['title']
            item['link'] = response.url
            print(response.meta['title'])
            print(response.url)
            if i == 0:
                mv_type = movie.xpath('./a/text()')
                print(mv_type.extract())
                item['mv_type'] = mv_type.extract()
            elif i == 2:
                mv_time = movie.xpath('./text()')
                print(mv_time.extract())
                item['mv_time'] = mv_time.extract()
            else:
                pass
            i = i + 1

        yield item
        sleep(random.randint(3, 10))  # 防止被反扒



