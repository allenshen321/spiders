# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem
from .settings import *


class CnblogspiderPipeline(object):
    def __init__(self):
        self.file = open('cnblogs_info.txt', 'w')

    def process_item(self, item, spider):
        if item['title']:
            self.file.write(str(dict(item))+'\n')
            return item
        else:
            raise DropItem('在%s中没有标题!!!' % item)


class MongoPipeline(object):
    collection_name = 'cnblogs'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item