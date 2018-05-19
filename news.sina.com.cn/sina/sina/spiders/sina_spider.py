# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import SinaItem


class SinaSpiderSpider(scrapy.Spider):
    name = 'sina_spider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 提取大类的标题和url
        parent_title = response.xpath('//div[@id="tab01"]//h3/a/text()').extract()
        parent_url = response.xpath('//div[@id="tab01"]//h3/a/@href').extract()
        # 提取子类的标题和URL，子类以父类网址开头
        sub_title = response.xpath('//div[@id="tab01"]//ul/li/a/text()').extract()
        sub_url = response.xpath('//div[@id="tab01"]//ul/li/a/@href').extract()

        # 存储item的列表items
        items = []
        # 建立大类文件夹
        for i in range(len(parent_title)):
            # 判断是否存在目录，如有没有则创建
            parent_filepath = './data/' + parent_title[i]
            if not os.path.exists('./data/' + parent_title[i]):
                os.makedirs('./data/' + parent_title[i])
            for j in range(len(sub_title)):
                is_belong = sub_url[j].startswith(str(parent_url[i]))
                # 判断子类URL是否已父类URL开头
                if is_belong:
                    # 判断子类是否存在目录，如果没有则创建
                    sub_filepath = parent_filepath + '/' + sub_title[j]
                    if not os.path.exists(sub_filepath):
                        os.makedirs(sub_filepath)
                    # 存储变量到item里
                    item = SinaItem()
                    item['parent_title'] = parent_title[i]
                    item['parent_url'] = parent_url[i]
                    item['sub_title'] = sub_title[j]
                    item['sub_url'] = sub_url[j]
                    item['sub_filepath'] = sub_filepath
                    # 将item存放到items列表中
                    items.append(item)
        for item in items:
            yield scrapy.Request(url=item['sub_url'], meta={"meta_1": item}, callback=self.secend_parse)

    def secend_parse(self, response):
        # 创建存放item的空列表
        items = []
        meta_1 = response.meta['meta_1']
        son_urls = response.xpath('//a/@href').extract()
        i = 0
        for son_url in son_urls:
            # 判断son_url是否以父类网址开头，且以shtml结尾
            is_belong = son_url.endswith('.shtml') and son_url.startswith(meta_1['parent_url'])
            # 判断结果是真值，则将son_url放进item中，已进行下一次迭代
            if is_belong:
                i += 1
                print(meta_1['sub_title'] + '该类一共有' + str(i) + '个链接')

                item = SinaItem()
                item['parent_title'] = meta_1['parent_title']
                item['parent_url'] = meta_1['parent_url']
                item['sub_url'] = meta_1['sub_url']
                item['sub_title'] = meta_1['sub_title']
                item['sub_filepath'] = meta_1['sub_filepath']
                item['son_url'] = son_url
                items.append(item)
        for item in items:
            i += 1
            print(item['sub_title'] + '该类一共有' + str(i) + '个链接')
            yield scrapy.Request(url=item['son_url'], callback=self.detail_parse, meta={'meta_2': item})

    def detail_parse(self, response):
        item = response.meta['meta_2']
        # 定义一个空的字符串，用来存放多条返回文本
        result = ''
        result_title = ''
        title = response.xpath('//h1/text()').extract()
        content = response.xpath('//p/text()').extract()
        for each in content:
            result += each + '\n'
        for each in title:
            result_title += each.strip()
        item['title'] = result_title.strip()
        item['content'] = result
        yield item
