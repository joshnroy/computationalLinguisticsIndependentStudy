import pymongo, nltk
from pymongo import MongoClient

client = MongoClient()

db = client['tinderBot']

names = db['names']

with open ('names.txt') as f:
    for line in f:
        name = {"name": line}
        names.insert(name)
