# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity


def process_photos_size(value: str):
    return value.replace('w_82,h_82', 'w_1000,h_1000')


def process_specs_value(value):
    return value.replace('\n', '').strip()


class MerlinruItem(scrapy.Item):
    _id = scrapy.Field()
    specs_values = scrapy.Field(input_processor=MapCompose(process_specs_value))
    specs_names = scrapy.Field(output_processor=Identity())
    specs = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photos_size))
