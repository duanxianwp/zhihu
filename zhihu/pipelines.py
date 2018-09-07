# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from zhihu import items


class MongoPipeline(object):
    collection_name = 'scrapy_items'
    url_token = None

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
        if self.url_token is not None:
            # 进行采集任务task 状态变更
            self.db['collect_task'].update({'token': self.url_token}, {'$set': {'status': "ANLAYZE_WAIT"}})
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, items.UserItem):
            self.db['user'].update({'url_token': item.get('url_token')}, {'$set': item}, True)
            return item
        elif isinstance(item, items.QuestionItem):
            self.db['question'].update({'url_token': item.get('url_token'), 'id': item.get('id')}, {'$set': item}, True)
            self.url_token = item['url_token']
            return item
        elif isinstance(item, items.AnswerItem):
            self.db['answer'].update({'url_token': item.get('url_token'), 'id': item.get('id')}, {'$set': item}, True)
            self.url_token = item['url_token']
            return item
        else:
            return None
