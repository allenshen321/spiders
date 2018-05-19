# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunqiBookListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 小说
    novel_id = scrapy.Field()
    # 小说名称
    novel_name = scrapy.Field()
    # 小说链接
    novel_link = scrapy.Field()
    # 小说作者
    novel_author = scrapy.Field()
    # 小说类型
    novel_type = scrapy.Field()
    # 小说简介
    novel_abstract = scrapy.Field()
    # 小说状态
    novel_status = scrapy.Field()
    # 小说更新时间
    novel_update_time = scrapy.Field()
    # 小说字数
    novel_words = scrapy.Field()
    # 小说封面
    novel_image_url = scrapy.Field()


class YunqiBookDetailItem(object):
    # 小说id
    novel_id = scrapy.Field()
    # 小说标签
    novel_label = scrapy.Field()
    # 总点击量
    novel_all_click = scrapy.Field()
    # 月点击量
    novel_month_click = scrapy.Field()
    # 周点击量
    novel_week_click = scrapy.Field()
    # 总人气
    novel_all_popular = scrapy.Field()
    # 月人气
    novel_month_popular = scrapy.Field()
    # 周人气
    novel_week_popular = scrapy.Field()
    # 评论数
    novel_comment_num = scrapy.Field()
    # 小说总推荐
    novel_all_comm = scrapy.Field()
    # 小说月推荐
    novel_month_comm = scrapy.Field()
    # 小说周推荐
    novel_week_comm = scrapy.Field()
