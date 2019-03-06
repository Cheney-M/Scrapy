# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from .items import MovieItem


class MoviespiderPipeline(object):
    config = {}

    def __init__(self):
        pass

    def process_item(self, item, spider):
        if(isinstance(item, MovieItem)):
            if item['link']:
                return item

class MongoPipline(object):
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        print(self.mongo_uri,mongo_db)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print(self.db)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].update({'link': item.get('link')}, {'$set': dict(item)}, True)
        return item