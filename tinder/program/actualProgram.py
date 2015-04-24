import pymongo, nltk, sys, os, stat_parser
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *
from pprint import pprint
from tinderAccess import authenticate, postForm, sendMessage
from time import sleep
from nltk.util import ngrams

# Variables
FBTOKEN="CAAGm0PX4ZCpsBAJQkND9pkYyntjZBOYdiVbz9TocR49mQ0xEBZCSMYLIzcMGy7sukyrliVg9GUUmllyx8mSNFkJMdHvlb9AHEk2RhNXZAr7qLjdzwRo7wH2Xns7W4TMQPcViZCJlSqTX5xBZBIsd7lboBb7t2jgOqsMxpftupIjenxBnGweK7OkD9uN2QJNBuufSc3JuusXtAEvARdj1Bes3REj2AysVoZD"
FBID="100009426311666"
LAT = "42.312449"
LON = "-71.035905"
data = {"lat": LAT, "lon": LON}
token = authenticate(FBTOKEN, FBID)['token']

# Setting up the database stuff
client = MongoClient()

db = client['tinderBot']

names = db['names']

pronounVerbPhrases = db['pronounVerbPhrases']

messagesAndResponses = db['messagesAndResponses']

openingMessages = db['openingMessages']

pronounResponses = db['pronounResponses']

# Setting up the processing stuff
parser = Parser()

# Defining Functions

def checkForNewMessages(token):
    matches = postForm("updates", "", token)['matches']
    recievedMessages = []
    for match in matches:
        messages = match['messages']
        for message in messages:
            if message['to'] == '552d6a6275a887851e60ab54':
                recievedMessage = {'from': message['from'],
                        'message': message['message']}
                recievedMessages.append(recievedMessage)
    return recievedMessages

def replyToMessages(messages, token):
    pass

def getMatches(token):
    update = postForm("updates", "", token)
    recievedMatches = []
    matches = update['matches']
    for match in matches:
        recievedMatches.append(match['_id'])
    return set(recievedMatches)

# THE ACTUAL PROGRAM

while False:
    newMatches = checkForNewMatches(token)
    startMessages(newMatches, token)
    newMessages = checkForNewMessages(token)
    replyToMessages(newMessages, token)
    sleep(60)


# THE sending messages to database program
if False:
    matches = postForm("updates", "", token)['matches']
    for match in matches:
        messages = match['messages']
        messagePair = {"Rating": 0}
        for message in messages:
            if message['to'] == '552d6a6275a887851e60ab54':
                messagePair['Recieved'] = message['message']
            else:
                messagePair['Sent'] = message['message']
                if "Recieved" in messagePair and "Sent" in messagePair:
                    messagesAndResponses.insert(messagePair)
                else:
                    openingMessages.insert(messagePair)
                messagePair = {}

# The learning part
if True:
    for messagePair in messagesAndResponses.find():
        recievedBigrams = ngrams(nltk.word_tokenize(messagePair['Recieved']), 2)
        sentBigrams = ngrams(nltk.word_tokenize(messagePair['Sent']), 2)
        for recievedBigram in recievedBigrams:
            for sentBigram in sentBigrams:
                print str(recievedBigram) + "\t" + str(sentBigram)
        print "################################################################"
        '''
        try:
            recievedTree = parser.parse(messagePair['Recieved'])
        except TypeError as e:
            print e
        try:
            sentTree = parser.parse(messagePair['Sent'])
        except TypeError as e:
            print e
        '''
