# -*- coding: utf-8 -*-
import scrapy
from ..items import CnblogspiderItem


class CnblogsSpiderSpider(scrapy.Spider):
    name = 'cnblogs_spider'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://www.cnblogs.com/qiyeboy/default.html?page=1']

    def parse(self, response):
        articles = response.xpath('//div[@class="day"]')
        # 调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for article in articles:
            url = article.xpath('./div[@class="postTitle"]/a/@href').extract()[0]
            title = article.xpath('./div[@class="postTitle"]/a/text()').extract()[0]
            time = article.xpath('./div[@class="dayTitle"]/a/text()').extract()[0]
            abstract = article.xpath('./div[@class="postCon"]/div/text()').extract()[0]
            item = CnblogspiderItem(url=url, title=title, time=time, abstract=abstract)
            yield item
        next_page = scrapy.Selector(response).re(r'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)
