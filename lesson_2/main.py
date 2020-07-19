from bs4 import BeautifulSoup as bs
import requests


def get_salary(item):

    res = [None, None, None]

    if not item or item.find('договорённости') != -1:
        return res

    if str(item).find('\x20') == -1:
        item = item.split('\xa0')
        currency = item.pop()
        if item[0] in ['от', 'до']:
            direction = item.pop(0)
            item = [direction, ''.join(item)]
        else:
            item = ''.join(item)
        res[2] = currency
    else:
        item = item.replace('\xa0', '').split(' ')
        res[2] = item[-1]

    if item[0] == 'от':
        res[0] = int(item[1])
    elif item[0] == 'до':
        res[1] = int(item[1])
    else:
        if type(item) is str:
            s = item.split('—')
        else:
            s = item[0].split('-')

        res[0] = int(s[0])
        res[1] = int(s[1])

    return res


def get_city(city):

    if city.find('•') == -1:
        return city

    res = city.split('•')[-1]

    return res


def get_vacancy_data(item, params):
    res = {'salary': get_salary(item.find(params['salary'][0], params['salary'][1]).getText()),
           'name': item.find(params['name'][0], params['name'][1]).getText(),
           'city': get_city(item.find(params['city'][0], params['city'][1]).getText()),
           'description': item.find(params['description'][0], params['description'][1]).getText(),
           'source': params['source']}

    company = item.find(params['company'][0], params['company'][1])

    if company:
        res['company'] = company.getText()

    return res


def get_items(url, page, params, parse_params, headers=None):
    res = []

    while True:

        response = requests.get(url + '&page=' + str(page), headers=headers)
        soup = bs(response.text, 'lxml')

        is_next_page = soup.find(params['next'][0], params['next'][1])

        if not 'container' in params:
            vacancies_block = soup.find(params['item'][0], params['item'][1]).parent
        else:
            vacancies_block = soup.find(params['container'][0], params['container'][1])

        vacancies = vacancies_block.find_all(params['item'][0], params['item'][1])

        for vacancy in vacancies:
            if (str(vacancy.findChild()).find('f-test-vacancy-item')) != -1 or (
                    str(vacancy).find('vacancy-serp-item') != -1):
                res.append(get_vacancy_data(vacancy, parse_params))

        if not is_next_page:
            break

        page += 1

    return res
