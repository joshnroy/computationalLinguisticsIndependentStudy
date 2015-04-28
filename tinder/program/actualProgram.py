import pymongo, nltk, sys, os, stat_parser, random
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *
from pprint import pprint
from tinderAccess import authenticate, postForm, sendMessage
from time import sleep
from nltk.util import ngrams

# Variables
FBTOKEN="CAAGm0PX4ZCpsBAOLhjoUQMiq8jAY1QcZCF5sAqMZC8Jeovv4fyK8QiHQ7aQ0QeT0vFQZBCrysEYC315yaIAtmKZC6s6f3zCwUGt73dw44rv0yiXf0KAgRcDzh3s4ZBynOlWs7EPFPdVQ0iJZAwoZC6ZBcMWzgZAismorj9muNcXctViZBbGT45F1ylDZBDatrSFSon4qXIsalW9QvLj87m7DwUwCLP4MGnjGEyIZD"
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

bigramPairs = db['bigramPairs']

verbPairs = db['verbPairs']

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
    sentMessages = []
    for message in messages:
        messageToSend = ""
        possibleMessages = messagesAndResponses.find({"message": message['message']})
        if possibleMessages.count() == 0:
            recievedBigrams = ngrams(nltk.word_tokenize(message), 2)
            for bigram in recievedBigrams:
                possibleSentBigrams = bigramPairs.find({"recieved", bigram}).sort({"rating": -1})
                pprint(possibleSentBigrams)
        elif possibleMessages.count() == 1:
            messageToSend = possibleMessages
        else:
            messageToSend = possibleMessages.find().limit(-1).skip(random.randint(0, possibleMessages.count() - 1)).next()
#        sendMessage(message['from'], messageToSend, token)
#        sentMessages.append({"to": message['from'], "message": messageToSend})
    print("Replied to all messages")
    return sentMessages

def getMatches(token):
    update = postForm("updates", "", token)
    matches = update['matches']
    for match in matches:
        recievedMatches.append(match)
    return recievedMatches

def checkForNewMatches(token):
    matches = postForm("updates", "", token)['matches']
    newMatches = []
    for match in matches:
        if match['messages'] == []:
            newMatches.append(match['_id'])
    return newMatches

def startMessages(matches, token):
    sentMessages = []
    for match in matches:
        messageToSend = openingMessages.find().limit(-1).skip(random.randint(0, openingMessages.count() - 1)).next()
        sendMessage(match, messageToSend['Sent'], token)
        sentMessages.append({"to": match, "message": messageToSend['Sent']})
    print("Sent messages to all new matches")
    return sentMessages

def learnFromMessages(newMessages, sentMessages, startMessages):
    pass

# THE ACTUAL PROGRAM
sentReplies = []
sentStarts = []
while True:
    newMatches = checkForNewMatches(token)
    if newMatches:
        sentStarts = startMessages(newMatches, token)
    newMessages = checkForNewMessages(token)
    if newMessages:
        learnFromMessages(newMessages, sentReplies, sentStarts)
#    sentReplies = replyToMessages(newMessages, token)
    sleep(30)


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
if False:
    for messagePair in messagesAndResponses.find():
        if True:
            recievedBigrams = ngrams(nltk.word_tokenize(messagePair['Recieved']), 2)
            sentBigrams = ngrams(nltk.word_tokenize(messagePair['Sent']), 2)
            for recievedBigram in recievedBigrams:
                for sentBigram in sentBigrams:
                    if bigramPairs.find({"recieved": recievedBigram, "sent": sentBigram}).count() != 0:
                        pairToUpdate = bigramPairs.find_one({"recieved": recievedBigram, "sent": sentBigram})
                        bigramPairs.update({"recieved": recievedBigram, "sent": sentBigram}, {"rating": pairToUpdate['rating'] + 1})
                    else:
                        bigramPairs.insert({"recieved": recievedBigram, "sent": sentBigram, "rating": 1})
        try:
            recievedTree = parser.parse(messagePair['Recieved'])
        except TypeError as e:
            print e
        try:
            sentTree = parser.parse(messagePair['Sent'])
        except TypeError as e:
            print e
        for recievedVerb  in recievedTree.subtrees(filter=lambda x: x.label() == "VB" or x.label() == "VBD" or x.label() == "VBG" or x.label() == "VBN" or x.label() == "VBP" or x.label() == "VBZ"):
            for sentVerb in sentTree.subtrees(filter=lambda x: x.label() == "VB" or x.label() == "VBD" or x.label() == "VBG" or x.label() == "VBN" or x.label() == "VBP" or x.label() == "VBZ"):
                if verbPairs.find({"recieved": recievedVerb, "sent": sentVerb}).count() != 0:
                    verbPair = verbPairs.find_one({"recieved": recievedVerb, "sent": sentVerb})
                    verbPairs.update({"recieved": recievedVerb, "sent": sentVerb}, {"rating": verbPair['rating'] + 1})
                else:
                    verbPairs.insert({"recieved": recievedVerb, "sent": sentVerb, "rating": 1})
