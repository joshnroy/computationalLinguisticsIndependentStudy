import pymongo, nltk, sys, os, stat_parser
from pymongo import MongoClient
from stat_parser import Parser, display_tree

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

# Do the processing
#    parser = stanford.StanfordParser(model_path="/Users/josh/Documents/Workspace/computationalLinguisticsIndependentStudy/tinder/program/stanford/stanford-raw/stanford-parser-3.5.1-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#    parser = nltk.ChartParser(grammar)
    sentences = sent_detector.tokenize(learningCorpus.strip())
    parser = Parser()
    for sentence in sentences:
        try:
            tree = parser.parse(sentence)
            display_tree(tree) 
        except TypeError:
            pass
