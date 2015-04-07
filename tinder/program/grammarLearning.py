import pymongo, nltk
from pymongo import MongoClient
from collections import defaultdict

# Setting up the database stuff
client = MongoClient()

db = client['tinderBot']

names = db['names']

messages = db['messages']

# Getting name of the learning corpus
learningCorpusName = input("What is the name of the learning corpus? (make sure it is in the directory that you are running this program from): ")

# Opening the learning corpus
with open(learningCorpusName) as f:
    learningCorpus = f.read().replace('\n', '')

# Split into sentences
    counts = defaultdict(int)
    sentences = nltk.tokenize.sent_tokenize(learningCorpus.decode('utf-8'))
    for sentence in sentences:
        tagged = nltk.pos_tag(nltk.tokenize.word_tokenize(sentence))
        for word, tag in tagged:
            counts[tag] += 1
    print sorted(counts)
