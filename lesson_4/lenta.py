import requests
from lxml import html


def get_data():

    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36'}

    lenta_link = 'https://lenta.ru/'

    response = requests.get(lenta_link, headers=header)
    dom = html.fromstring(response.text)

    main_news = dom.xpath("//section[contains(@class, 'b-top7-for-main')]")[0]

    news = main_news.xpath(".//div[@class='first-item']")[0]

    data = []
    item = {}

    item['name'] = news.xpath(".//h2/a/text()")[0].replace('\xa0', ' ')
    item['link'] = news.xpath(".//h2/a/@href")[0]
    item['source'] = 'https://lenta.ru/'
    item['date'] = news.xpath(".//time/@title")[0]

    data.append(item)

    news = main_news.xpath(".//div[@class='item']")

    for i in news:

        item = {}

        item['name'] = i.xpath(".//a/text()")[0].replace('\xa0', ' ')
        item['link'] = i.xpath(".//a/@href")[0]
        item['source'] = 'https://lenta.ru/'
        item['date'] = i.xpath(".//time/@title")[0]

        data.append(item)

    # print('from lenta', data)
    return data
