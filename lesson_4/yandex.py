import requests
from datetime import datetime, timedelta
from lxml import html


def get_data():

    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36'}

    yandex_link = 'https://yandex.ru/news'

    response = requests.get(yandex_link, headers=header)
    dom = html.fromstring(response.text)

    news = dom.xpath("//div[@class='stories-set__main-item']")
    news.extend(dom.xpath("//table[@class='stories-set__items']"))

    data = []

    for i in news:

        item = {}

        item['name'] = i.xpath(".//h2[@class='story__title']//text()")[0].replace('\xa0', ' ')
        item['link'] = i.xpath(".//a[contains(@class, 'link_theme_black')]/@href")[0]
        item['source'] = i.xpath(".//div[@class='story__date']//text()")[0][:-6]

        if i.xpath(".//div[@class='story__date']//text()")[0].find('вчера') != -1:
            date = datetime.now() - timedelta(days=1)
            date = date.strftime("%Y-%m-%d")
        else:
            date = datetime.now().strftime("%Y-%m-%d")

        item['date'] = date

        data.append(item)

    # print('from yandex', data)
    return data
