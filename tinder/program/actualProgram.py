import pymongo, nltk, sys, os, stat_parser
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *
from pprint import pprint
from tinderAccess import authenticate, postForm, sendMessage
from time import sleep

# Variables
FBTOKEN="CAAGm0PX4ZCpsBAE4rYNNsrF9SZBu4INR2udjL0BU5OtMluo7Q05MY20yNdvZB9kfjKtP0RbCYHrvZBA2VcRGIXZCRc4Ut8c5AnqDPrF7RLuYSkXP5hOuM0r27I2KT5n2h7bmEJZA3ro05K9KzKwIwOOhDtMzbBQfoeiO31P0H4QOKtxZCTqEJAu59Rmkjd28e8elEEQO24FZAhYGvsZBUwoXofygmTUjP3GwZD"
FBID="100009426311666"
LAT = "42.312449"
LON = "-71.035905"
data = {"lat": LAT, "lon": LON}
token = authenticate(FBTOKEN, FBID)['token']

# Setting up the database stuff
client = MongoClient()

db = client['tinderBot']

names = db['names']

messages = db['messages']

pronounVerbPhrases = db['pronounVerbPhrases']

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
    matches = postForm("updates", "", token)['matches']
    recievedMatches = []
    for match in matches:
        messages = match['messages']
        for message in messages:
            if message['to'] == '552d6a6275a887851e60ab54':
                recievedMatches.append(message['from'])
    return set(recievedMatches)

# THE ACTUAL PROGRAM

matches = getMatches(token)
pprint(matches)

while False:
    newMessages = checkForNewMessages(token)
    replyToMessages(newMessages, token)
    sleep(60)
