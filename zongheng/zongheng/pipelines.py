# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class ZonghengPipeline(object):
    def __init__(self):
        self.id = 0
    def process_item(self, item, spider):
        # print(item)

        # 把数据插入 novel 表
        with self.connection.cursor() as cursor:
            sql = "insert ignore into novel(novelName,author) value(%s,%s)"
            try:
                result = cursor.execute(sql,(item['book'],item['author']))
                if result != 0:     # 没有重复数据
                    self.id = self.connection.insert_id()
                    self.connection.commit()
            except Exception as e:
                print(e)
        # 把数据插入 chapter 表
        with self.connection.cursor() as cursor:
            sql = "insert into chapter(chapterName,content,novelId) value(%s,%s,%s)"
            try:
                cursor.execute(sql,(item['chapter'],item['content'],self.id))
                self.connection.commit()
            except Exception as e:
                print(e)
        return item
    def open_spider(self,spider):
        print("spider start")
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='123456',
                                          db='zongheng',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        
    def close_spider(self, spider):
        print("spider end")
        self.connection.close()
