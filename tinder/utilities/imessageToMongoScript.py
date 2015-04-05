import csv,  pymongo
from pymongo import MongoClient

client = MongoClient()
db = client['messages']


f = open('rawIMessages.csv')
csv_f = csv.reader(f)

messages = db['messages']

for row in csv_f:
    message = {"to": row[3],
            "from": row[5],
            "message": row[7]}
    message_id = messages.insert(message)
