# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 大类标题和链接
    parent_title = scrapy.Field()
    parent_url = scrapy.Field()
    # 子类标题和链接
    sub_title = scrapy.Field()
    sub_url = scrapy.Field()
    # 小类存储路径
    sub_filepath = scrapy.Field()
    # 文章链接
    son_url = scrapy.Field()
    # 文章标题和内容
    title = scrapy.Field()
    content = scrapy.Field()
