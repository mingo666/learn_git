# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyScrapyPipeline:
    #    def process_item(self, item, spider):
    #        return item

    # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
    def process_item(self, item, spider):
        try:
            title = item['title']
            link = item['link']
            mv_type = item['mv_type']
            mv_time = item['mv_time']
            output = f'|{title}|\t|{link}|\t|{mv_type}|\t|{mv_time}|\n\n'
            with open('./doubanmovie.txt', 'a+', encoding='utf8') as article:
                article.write(output)
            return item
        except Exception as e:  # 抓取所有错误信息。
            print("-----------------------------------------process_item执行报错-----------------------------------------")
            print(e)

