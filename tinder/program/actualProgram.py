import pymongo, nltk, sys, os, stat_parser, random, urllib2, re
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *
from pprint import pprint
from tinderAccess import authenticate, postForm, sendMessage
from time import sleep
from nltk.util import ngrams

# Variables
FBTOKEN="CAAGm0PX4ZCpsBAG7JHNWZBXT6L0sEhPBlrlEro11axn8C5iVRP92I90ZCsw0vJ6ycI9f389TFuG0ALCz177GDjBqOTpCbcZACeuP73lnfLTzEFfjhtXVvaaJnSYHvWlkTpCZBSCHt7ko30YAMiZAwgD8ZAZBOkI9BQPzpzA0ZBfGNPqqvwJSx5nEQIquidZCEN7eazGRNljxkAg1r5XZCRN6CMn8XnhgZBf2tyQZD"
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
                fromMessages = list(messages)
                for fromMessage in fromMessages:
                    if fromMessages.index(fromMessage) >= messages.index(message):
                        fromMessages.remove(fromMessage)
                fromMessages.reverse()
                recievedMessage = {'recieved': message['message'],
                        'sent': fromMessages[0]['message'],
                        'from': message['match_id']}
                recievedMessages.append(recievedMessage)
                break
    print "Got new messages"
    return recievedMessages

def replyToMessages(messages, token):
    sentMessages = []
    for message in messages:
        possibleResponses = []

# Split recieved message into ngrams
        recievedUnigrams = ngrams(nltk.word_tokenize(message['recieved']), 1)
        recievedBigrams = ngrams(nltk.word_tokenize(message['recieved']), 2)
        recievedTrigrams = ngrams(nltk.word_tokenize(message['recieved']), 3)

# unigram
        for unigram in recievedUnigrams:
            for unigramPair in unigramPairs.find({"sent": unigram}):
                if possibleResponses:
                    index = -1
                    for response in possibleResponses:
                        if response[0] == unigramPair['recieved']:
                            index = possibleResponses.index(response)
                    if index != -1:
                        possibleResponses[index][1] += 1
                    else:
                        possibleResponses.append([unigramPair['recieved'], 1])
                else:
                    possibleResponses.append([unigramPair['recieved'], 1])

# bigram
        for bigram in recievedBigrams:
            for bigramPair in bigramPairs.find({"sent": bigram}):
                if possibleResponses:
                    index = -1
                    for response in possibleResponses:
                        if response[0] == bigramPair['recieved']:
                            index = possibleResponses.index(response)
                    if index != -1:
                        possibleResponses[index][1] += 1
                    else:
                        possibleResponses.append([bigramPair['recieved'], 1])
                else:
                    possibleResponses.append([bigramPair['recieved'], 1])

# trigram
        for trigram in recievedTrigrams:
            for trigramPair in trigramPairs.find({"sent": trigram}):
                if possibleResponses:
                    index = -1
                    for response in possibleResponses:
                        if response[0] == trigramPair['recieved']:
                            index = possibleResponses.index(response)
                    if index != -1:
                        possibleResponses[index][1] += 1
                    else:
                        possibleResponses.append([trigramPair['recieved'], 1])
                else:
                    possibleResponses.append([trigramPair['recieved'], 1])

        possibleResponses.sort(key=lambda x: int(x[1]), reverse=True)
        try:
            try:
                try:
                    possibleResponses[0][0] = re.sub(r"Mackenzie", r"", possibleResponses[0][0])
                    sendMessage(message['from'], possibleResponses[0][0], token)
#                    print "Sent to: \t" + message['from'] + "\t sentMessage: \t" + possibleResponses[0][0] + "\t recievedMessage: \t" + message['recieved']
                    sentMessages.append({"recieved": message['recieved'], "sent": possibleResponses[0][0], "to": message['from']})
                    sleep(1)
                except UnicodeEncodeError as f:
                    print f
            except urllib2.HTTPError as e:
                print e
        except IndexError as g:
            print g
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
    print "Got new matches"
    return newMatches

def startMessages(matches, token):
    sentMessages = []
    for match in matches:
        messageToSend = openingMessages.find().limit(-1).skip(random.randint(0, openingMessages.count() - 1)).next()
        print match + "\t match"
        sendMessage(match, messageToSend['Sent'], token)
        sentMessages.append({"to": match, "message": messageToSend['Sent']})
    print("Sent messages to all new matches")
    return sentMessages

def learnFromMessages(newMessages):
    learningAlgorithm(newMessages)
    print "Learned from messages"


def learningAlgorithm(messagePairs):
    for messagePair in messagePairs:

# Learn the unigram associations
        sentUnigrams = ngrams(nltk.word_tokenize(messagePair['sent']), 1)
        for sentUnigram in sentUnigrams:
            if unigramPairs.find({"recieved": messagePair['recieved'], "sent": sentUnigram}).count() != 0:
                pairToUpdate = unigramPairs.find_one({"recieved": messagePair['recieved'], "sent": sentUnigram})
                unigramPairs.update({"recieved": messagePair['recieved'], "sent": sentUnigram}, {"rating": pairToUpdate['rating'] + 1})
            else:
                unigramPairs.insert({"recieved": messagePair['recieved'], "sent": sentUnigram, "rating": 1})

# Learn the bigram associations
        sentBigrams = ngrams(nltk.word_tokenize(messagePair['sent']), 2)
        for sentBigram in sentBigrams:
            if bigramPairs.find({"recieved": messagePair['recieved'], "sent": sentBigram}).count() != 0:
                pairToUpdate = bigramPairs.find_one({"recieved": messagePair['recieved'], "sent": sentBigram})
                bigramPairs.update({"recieved": messagePair['recieved'], "sent": sentBigram}, {"rating": pairToUpdate['rating'] + 1})
            else:
                bigramPairs.insert({"recieved": messagePair['recieved'], "sent": sentBigram, "rating": 1})

# Learn the trigram associations
        sentTrigrams = ngrams(nltk.word_tokenize(messagePair['sent']), 3)
        for sentTrigram in sentTrigrams:
            if trigramPairs.find({"recieved": messagePair['recieved'], "sent": sentTrigram}).count() != 0:
                pairToUpdate = trigramPairs.find_one({"recieved": messagePair['recieved'], "sent": sentTrigram})
                trigramPairs.update({"recieved": messagePair['recieved'], "sent": sentTrigram}, {"rating": pairToUpdate['rating'] + 1})
            else:
                trigramPairs.insert({"recieved": messagePair['recieved'], "sent": sentTrigram, "rating": 1})




# THE ACTUAL PROGRAM
# while True:
if True:
    newMatches = checkForNewMatches(token)
    startMessages(newMatches, token)
    newMessages = checkForNewMessages(token)
    learnFromMessages(newMessages)
    sentReplies = replyToMessages(newMessages, token)
#    sleep(random.randint(1, 120))


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
