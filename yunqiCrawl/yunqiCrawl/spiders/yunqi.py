# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import YunqiBookListItem


class YunqiSpider(CrawlSpider):
    name = 'yunqi'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']

    rules = (
        Rule(LinkExtractor(allow=r'http://yunqi.qq.com/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        # 调出调试窗口
        from scrapy.shell import inspect_response
        inspect_response(response, self)

        books = response.xpath('//div[@class="book"]')
        for book in books:
            novel_image_url = book.xpath('./a/img/@src').extract_first()
            novel_id = book.xpath('./div[@class="book_info"]/h3/a/@id').extract_first()
            novel_link = book.xpath('./div[@class="book_info"]/h3/a/@href').extract_first()
            novel_name = book.xpath('./div[@class="book_info"]/h3/a/text()').extract_first()
            novel_author = book.xpath('./div[@class="book_info"]/dl[1]/dd[1]/a/text()').extract_first()
            novel_type = book.xpath('/div[@class="book_info"]/dl[1]/dd[2]/a/text()').extract_first()
            novel_status = book.xpath('./div[@class="book_info"]/dl[1]/dd[3]/a/text()').extract_first()
            novel_update_time = book.xpath('./div[@class="book_info"]/dl[2]/dd[1]/text()').extract_first()
            novel_words = book.xpath('./div[@class="book_info"]/dl[2]/dd[2]/text()').extract_first()
            novel_abstract = book.xpath('./div[@class="book_info"]/dl[3]/dd/text()').extract_first()

            item = YunqiBookListItem(novel_id=novel_id,
                                     novel_name=novel_name,
                                     novel_link=novel_link,
                                     novel_author=novel_author,
                                     novel_type=novel_type,
                                     novel_abstract=novel_abstract,
                                     novel_status=novel_status,
                                     novel_update_time=novel_update_time,
                                     novel_words=novel_words,
                                     novel_image_url=novel_image_url
                                     )
            yield item
