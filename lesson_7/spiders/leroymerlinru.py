import scrapy
from scrapy.http import HtmlResponse
from merlinru.items import MerlinruItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, cat: str):
        super().__init__()
        self.category = cat
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{self.category}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']")[0]
        product_links = response.xpath("//a[@slot='picture']")
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=MerlinruItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('specs_names', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('unit', "//span[@slot='unit']/text()")
        loader.add_xpath('specs_values', "//dd[@class='def-list__definition']/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        yield loader.load_item()
