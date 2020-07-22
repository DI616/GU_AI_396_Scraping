from pymongo import MongoClient


def add_to_md(data):

    def is_existed_vacancy(vac):

        a = vacancies.find_one(vac)

        if a:
            return True
        return False

    n, o = 0, 0
    for i in data:
        existed_vacancy = is_existed_vacancy(i)
        if not existed_vacancy:
            n += 1
            vacancies.insert_one(i)
        else:
            o += 1

    print(f'Got {len(data)} vacancies, {n} new, {o} are not written in db.')


def find_salary():
    salary = int(input('Input min salary: '))
    res = vacancies.find({'salary': {'$gte': salary}}, {'_id': 0, 'name': 1, 'company': 1, 'salary': 1})

    for i in res:
        print(i)


client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']

vacancies = db.vacancies
