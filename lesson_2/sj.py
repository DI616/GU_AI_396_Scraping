import main
import mongo
import json

profession = 'Python developer'

sj_url = f'https://russia.superjob.ru/vacancy/search/?keywords={profession}'

parse_params = {'salary': ['span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}],
                'name': ['div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}],
                'city': ['span', {'class': '_3mfro f-test-text-company-item-location _9fXTd _2JVkc _2VHxz'}],
                'description': ['span', {'class': '_3mfro _38T7m _9fXTd _2JVkc _2VHxz _15msI'}],
                'company': ['span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'}],
                'source': 'https://superjob.ru'}

get_params = {'next': ['a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'}],
              'item': ['div', {'class': '_3zucV _1fMKr undefined _1NAsu'}]}

vacancies = main.get_items(sj_url, 1, get_params, parse_params)

with open('sj_vacancies.json', 'w') as f:
    json.dump(vacancies, f, ensure_ascii=False)

mongo.add_to_md(vacancies)

mongo.find_salary()
