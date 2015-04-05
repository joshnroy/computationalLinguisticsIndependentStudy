import pymongo, nltk
from pymongo import MongoClient
from nltk.tag import pos_tag

client = MongoClient()
db = client['messages']

messages = db['messages']

for message in messages.find():
    tagged = pos_tag(nltk.word_tokenize(message['message']))
    message['message'] = ''
    for word, pos in tagged:
        if pos != 'NNP':
            message['message'] += word +  ' '
    print message['message']

