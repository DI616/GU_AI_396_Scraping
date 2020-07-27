from pymongo import MongoClient
from hashlib import sha1
import lenta
import mail
import yandex

data = lenta.get_data()
data.extend(mail.get_data())
data.extend(yandex.get_data())

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news = db.news

for i in data:
    id_string = i['name'] + i['source'] + i['date']
    i['_id'] = sha1(id_string.encode()).hexdigest()

    news.insert_one(i)
