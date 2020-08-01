import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0'
                  '%B2%D0%B0%D0%BD%D0%B8%D0%B5/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        book_links = response.css('a.cover::attr(href)').extract()

        for book in book_links:
            yield response.follow(book, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        authors = response.xpath("//div[contains(text(), 'Автор:')]/a/text()").extract()
        interpreter = response.xpath("//div[contains(text(), 'Переводчик:')]/a/text()").extract_first()
        editor = response.xpath("//div[contains(text(), 'Редактор:')]/a/text()").extract_first()
        publisher = response.xpath("//div[@class='publisher']/a/text()").extract_first()
        series = response.xpath("//div[@class='series']/a/text()").extract_first()
        isbn = response.xpath("//div[@class='isbn']/text()").extract_first()
        pages = response.xpath("//div[@class='pages2']/text()").extract_first()
        price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        description = response.xpath("//div[@id='fullannotation']/p//text()").extract_first()
        if description is None:
            description = response.xpath("//div[@id='product-about']/p//text()").extract_first()
            if description is None:
                description = response.xpath("//h2/..//*/p//text()").extract_first()

        yield BooksparserItem(source=self.allowed_domains[0],
                              name=name,
                              authors=authors,
                              interpreter=interpreter,
                              editor=editor,
                              publisher=publisher,
                              series=series,
                              isbn=isbn,
                              pages=pages,
                              price=price,
                              description=description)
