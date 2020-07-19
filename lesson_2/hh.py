import main
import json

profession = 'Python developer'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Ubuntu Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36'}

hh_url = f'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text={profession}&L_save_area=true&' \
         f'area=113&from=cluster_area&showClusters=true'

parse_params = {'salary': ['div', {'class': 'vacancy-serp-item__sidebar'}],
                'name': ['div', {'class': 'vacancy-serp-item__info'}],
                'city': ['span', {'class': 'vacancy-serp-item__meta-info'}],
                'description': ['div', {'class': 'g-user-content'}],
                'company': ['a', {'data-qa': 'vacancy-serp__vacancy-employer'}],
                'source': 'https://hh.ru'}

get_params = {'next': ['a', {'class': 'HH-Pager-Controls-Next'}],
              'container': ['div', {'class': 'vacancy-serp'}],
              'item': ['div', {'class': 'vacancy-serp-item'}]}

vacancies = main.get_items(hh_url, 0, get_params, parse_params, headers=headers)

with open('hh_vacancies.json', 'w') as f:
    json.dump(vacancies, f, ensure_ascii=False)
