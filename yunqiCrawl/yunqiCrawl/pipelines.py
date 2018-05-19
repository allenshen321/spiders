# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .settings import MONGO_URI, MONGO_DATEBASE
from .items import YunqiBookListItem
import pymongo


class YunqicrawlPipeline(object):
    def __init__(self):
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DATEBASE

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, YunqiBookListItem):
            self.db.bookinfo.insert(dict(item))
        return item
