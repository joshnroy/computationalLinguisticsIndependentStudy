import pymongo, nltk
from pymongo import MongoClient
from nltk.tag import pos_tag
from nltk.tree import *
from nltk.draw import tree

client = MongoClient()
db = client['tinderBot']

messages = db['messages']

for message in messages.find():
    tagged = pos_tag(nltk.word_tokenize(message['message']))
    chunked = nltk.chunk.ne_chunk(tagged)
    chunked.draw()
    '''
    for subtree in chunked.subtrees():
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                if leaf[1] == 'NNP':
                    message['message'] = message['message'].replace(leaf[0], "", 1)
                    print message
                    messages.save(message)
    '''
