import requests
from lxml import html


def get_data():

    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36'}

    mail_link = 'https://news.mail.ru/'

    response = requests.get(mail_link, headers=header)
    dom = html.fromstring(response.text)

    main_news = dom.xpath("//div[contains(@class, 'js-topnews')]//tr//div[contains(@class, 'daynews__item')]")

    data = []

    for i in main_news:

        item = {}

        link = i.xpath(".//a/@href")[0]

        item['link'] = link

        news_response = requests.get(mail_link + link, headers=header)

        news_dom = html.fromstring(news_response.text)
        item['source'] = news_dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/@href")[0]
        item['date'] = news_dom.xpath("//span[@datetime]/@datetime")[0][:10]

        item['name'] = i.xpath(".//a//span[contains(@class, 'photo__title')]/text()")[0].replace('\xa0', ' ')

        data.append(item)

    # print('from mail', data)
    return data
