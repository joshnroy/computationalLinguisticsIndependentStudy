import pymongo, nltk, sys, os, stat_parser
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *

# Setting up the database stuff
client = MongoClient()

db = client['tinderBot']

names = db['names']

messages = db['messages']

pronounVerbPhrases = db['pronounVerbPhrases']
learningCorpusName = sys.argv[1]

# Opening the learning corpus
with open(learningCorpusName) as f:
    learningCorpus = f.read().replace('\n', ' ').decode('utf-8')

# Do the processing and the learning
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(learningCorpus.strip())
    parser = Parser()
    for sentence in sentences:
        try:
            tree = parser.parse(sentence)
            tree.draw()
            for i in tree.subtrees(filter=lambda x: x.label() == 'NP'):
                i.draw()
        except TypeError:
            pass
