# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaPipeline(object):
    def process_item(self, item, spider):
        file_path = item['sub_filepath']+'/'+item['title']
        file_path = file_path.strip() + '.txt'
        with open(file_path, 'w') as f:
            f.write(item['title'] + '\n' + item['content'])
        return item
