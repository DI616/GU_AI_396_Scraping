# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class MerlinruPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.merlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.category]
        collection.insert_one(item)
        return item


class MerlinruPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1]['path'] for itm in results if itm[0]]
        return item


class MerlinruSpecsPipeline:
    def process_item(self, item, spider):
        if item['specs_names'] and item['specs_values']:
            item['specs'] = {}

            for name, val in zip(item['specs_names'], item['specs_values']):
                item['specs'][name] = val

        item.pop('specs_names')
        item.pop('specs_values')

        item['price'] = int(item['price'])
        return item

