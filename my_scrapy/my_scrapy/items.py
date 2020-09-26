# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 注释原有的pass
    # pass
    title = scrapy.Field()
    link = scrapy.Field()
    mv_type = scrapy.Field()
    mv_time = scrapy.Field()
