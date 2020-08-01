# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class BooksparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if item['source'] == 'labirint.ru':
            item['name'] = re.sub(r'^.*:\s', '', item['name'])

        item['pages'] = re.findall(r'\d+', item['pages'])[0]
        item['isbn'] = re.sub(r'^ISBN:\s', '', item['isbn'])
        item['publisher'] = item['publisher'].strip()
        item['price'] = item['price'].replace(' ', '')

        if type(item['description']) is list:
            item['description'] = self.get_string(item['description'])

        collection.insert_one(item)
        return item

    def get_string(self, arr):
        string = ''

        for a in arr:
            string += a.strip()

        return string
