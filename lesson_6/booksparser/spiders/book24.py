import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2'
                  '%D0%B0%D0%BD%D0%B8%D0%B5']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(text(), 'Далее')]/@href").extract_first()
        book_links = response.xpath("//a[@data-product-id]/@href").extract()

        for book in book_links:
            yield response.follow(book, callback=self.book_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        authors = response.xpath("//span[contains(text(), 'Автор:')]/..//a/text()").extract()
        interpreter = None
        editor = None
        publisher = response.xpath("//span[contains(text(), 'Издательство:')]/..//a/text()").extract_first()
        series = response.xpath("//span[contains(text(), 'Серия:')]/..//a/text()").extract_first()
        isbn = response.xpath("//input[contains(@class, 'isbn__code')]/@value").extract_first()
        pages = response.xpath("//span[contains(text(), 'Количество страниц:')]/..//span[2]/text()").extract_first()
        price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        description = response.xpath("//div[contains(@class, 'collapse-panel__panel')]/div[contains(@class, "
                                     "'collapse-panel__text')]//text()").extract()

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
