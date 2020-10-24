import scrapy
from zongheng.items import ZonghengItem
import copy

class zongHeng(scrapy.Spider):
    name = "zongheng"

    start_urls = ["http://www.zongheng.com/"]
    
    def parse(self,response):
        books_info = response.xpath('//ul[@id="monthTicketRankList"]//a')
        
        for book in books_info:
            item = ZonghengItem()
            href = book.xpath('./@href').extract_first()         # 目录url 
            book = book.xpath('./text()').extract_first()        # 小说名
            # http://book.zongheng.com/book/1013348.html 替换为 http://book.zongheng.com/showchapter/1013348.html
            href = href[:25]+href[25:].replace("book","showchapter")    # 全部目录url
            print(href,book)
            item['book'] = book
            yield scrapy.Request(url=href,callback=self.parse_dir,meta={'item':item})
            
    def parse_dir(self,response):
        ''' 小说目录
        '''
        item = response.meta['item']
        chapter_info = response.xpath('//li[@class=" col-4"]/a')
        author = response.xpath('//div[@class="book-meta"]//a/text()').extract_first()
        print('作者：',author)
        item['author'] = author


        for chapter in chapter_info:
            href = chapter.xpath('./@href').extract_first()             # 小说内容url
            item['chapter'] = chapter.xpath('./text()').extract_first()    # 章节名

            yield scrapy.Request(url=href,callback=self.parse_content,meta={'item':copy.deepcopy(item)})    # 使用深复制
            # 使用Request函数传递item时，使用的是浅复制（对象的字段值被复制时，字段引用的对象不会被复制）

    def parse_content(self,response):
        ''' 小说内容
        '''
        item = response.meta['item']
        content = response.xpath('//div[@class="content"]/p/text()').extract()  # 小说 p 标签内容
        # 小说内容处理
        string = ""
        for s in content:
            string = string + s + '\n'
        item['content'] = string
        yield item