import pymongo, nltk, sys, os, stat_parser, random
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *
from pprint import pprint
from tinderAccess import authenticate, postForm, sendMessage
from time import sleep
from nltk.util import ngrams

# Variables
FBTOKEN="CAAGm0PX4ZCpsBAHu369vq5tP9mYvNNENoYD3edfoxqYO8yGz7JMiMQnG6qe7lLj7pzZB3gUGWZCdB5vFSK3g5eEuQAf3NZApHsQBtWUP31dXzcVca0RN48X1ZCxkjKJbU0jp7OyltlqmmRd3ec6S2BbOtHULzn9ipYzoPIxWoB7K9BZApTsZBg7EzkthQZCiZC8OrRUku5ESg0mPmETZCiLYRG3A6cZCZC00qOoZD"
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

verbPairs = db['verbPairs']

# The important collections

unigramPairs = db['unigramPairs']

bigramPairs = db['bigramPairs']

trigramPairs = db['trigramPairs']

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
        possibleBigrams = {}
        possibleMessages = messagesAndResponses.find({"message": message['message']})
        if possibleMessages.count() == 0:
            recievedBigrams = ngrams(nltk.word_tokenize(message['message']), 2)
            for bigram in recievedBigrams:
                possibleSentBigrams = bigramPairs.find({"recieved": bigram}).sort([("rating", -1)])
                for bigram in possibleSentBigrams:
                    if bigram[str(bigram['sent'])] in possibleBigrams:
                        print possibleBigrams[bigram[str(bigram['sent'])]]['rating']
                    else:
                        possibleBigrams[bigram['sent'][0] + bigram['sent'][1]] = bigram['sent']
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
        messages = match['messages']
        if messages == []:
            newMatches.append(match['_id'])
        elif len(messages) == 1:
            newMatches.append(match['_id'])
            openingMessages.insert({"sent": messages[0]['message'].replace('Mackenzie', '')})
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
# while True:
if False:
    sentReplies = []
    sentStarts = []
    newMatches = checkForNewMatches(token)
    sentStarts = startMessages(newMatches, token)
    newMessages = checkForNewMessages(token)
    learnFromMessages(newMessages, sentReplies, sentStarts)
    sentReplies = replyToMessages(newMessages, token)
#    sleep(30)


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
# Learn the unigram associations
        print 'Unigramming : \t' + messagePair['Sent']
        sentUnigrams = ngrams(nltk.word_tokenize(messagePair['Sent']), 1)
        for sentUnigram in sentUnigrams:
            if unigramPairs.find({"recieved": messagePair['Recieved'], "sent": sentUnigram}).count() != 0:
                pairToUpdate = unigramPairs.find_one({"recieved": messagePair['Recieved'], "sent": sentUnigram})
                unigramPairs.update({"recieved": messagePair['Recieved'], "sent": sentUnigram}, {"rating": pairToUpdate['rating'] + 1})
            else:
                unigramPairs.insert({"recieved": messagePair['Recieved'], "sent": sentUnigram, "rating": 1})
# Learn the bigram associations
        print 'Bigramming : \t' + messagePair['Sent']
        sentBigrams = ngrams(nltk.word_tokenize(messagePair['Sent']), 2)
        for sentBigram in sentBigrams:
            if bigramPairs.find({"recieved": messagePair['Recieved'], "sent": sentBigram}).count() != 0:
                pairToUpdate = bigramPairs.find_one({"recieved": messagePair['Recieved'], "sent": sentBigram})
                bigramPairs.update({"recieved": messagePair['Recieved'], "sent": sentBigram}, {"rating": pairToUpdate['rating'] + 1})
            else:
                bigramPairs.insert({"recieved": messagePair['Recieved'], "sent": sentBigram, "rating": 1})
# Learn the trigram associations
        print 'Trigramming : \t' + messagePair['Sent']
        sentTrigrams = ngrams(nltk.word_tokenize(messagePair['Sent']), 3)
        for sentTrigram in sentTrigrams:
            if trigramPairs.find({"recieved": messagePair['Recieved'], "sent": sentTrigram}).count() != 0:
                pairToUpdate = trigramPairs.find_one({"recieved": messagePair['Recieved'], "sent": sentTrigram})
                trigramPairs.update({"recieved": messagePair['Recieved'], "sent": sentTrigram}, {"rating": pairToUpdate['rating'] + 1})
            else:
                trigramPairs.insert({"recieved": messagePair['Recieved'], "sent": sentTrigram, "rating": 1})
'''
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
'''
