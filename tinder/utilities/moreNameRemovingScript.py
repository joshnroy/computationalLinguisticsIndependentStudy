import pymongo, nltk
from pymongo import MongoClient

client = MongoClient()

db = client['tinderBot']

names = db['names']

messages = db['messages']

for message in messages.find():
    for name in names.find():
        message['message'] = message['message'].replace(name['name'], "", 100)
    messages.save(message)
