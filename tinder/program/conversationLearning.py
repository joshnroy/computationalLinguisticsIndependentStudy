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

verbResponses = db['verbResponses']
pronounResponses = db['pronounResponses']

# Parsing through the messages in the database and identifying the correct response verbs and nouns to input verbs and nouns
messagesFromPerson = messages.find({"from": "+16179329398"})
messagesToPerson = messages.find({"to": "+16179329398"})
x = 1
while True:
    if messagesFromPerson[x]['time'] < messagesToPerson[x]['time']:
        print "From\t" + str(messagesFromPerson[x]['message']) + "\t" + messagesFromPerson[x]['time']
        print "To\t" + str(messagesToPerson[x]['message']) + "\t" + messagesToPerson[x]['time']

    x +=1
