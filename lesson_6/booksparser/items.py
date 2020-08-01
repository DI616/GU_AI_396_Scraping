# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    interpreter = scrapy.Field()
    editor = scrapy.Field()
    source = scrapy.Field()
    publisher = scrapy.Field()
    series = scrapy.Field()
    isbn = scrapy.Field()
    pages = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
