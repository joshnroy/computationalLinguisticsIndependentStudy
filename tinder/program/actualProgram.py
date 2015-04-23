import pymongo, nltk, sys, os, stat_parser
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *
from pprint import pprint
from tinderAccess import authenticate, postForm, sendMessage
from time import sleep

# Variables
FBTOKEN="CAAGm0PX4ZCpsBAGwZCGiKIYukGLJtBpMZCH29C4kN2hZB7tXJLuk4EvO0yArTZC7SoZBJlfYcAbdcZBTqV3CaFGQuV9JkM7vAVWN0UvZA3h05IerwYS2gaqSOiqNPfWEvMz1bzsnpVdoJFkGevNUtthpkOjOfkPa4ioMkZCBOkBZAZBDVbcIdHus3mLeTRyxpkOv059L9FdoU54pj2kPDDPcjMZBn60ryg1Xi3QZD"
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
    newMessages = checkForNewMessages(token)
    replyToMessages(newMessages, token)
    sleep(60)


# THE TRAINING PROGRAM
matches = postForm("updates", "", token)['matches']
for match in matches:
    messages = match['messages']
    for message in messages:
        if message['to'] == '552d6a6275a887851e60ab54':
            print("Recieved\n")
        else:
            print("Sent\n")
        pprint(message['message'])
        print("\n")
    print("###########################################################################################################################################################")
