import pymongo, nltk, sys, os, stat_parser
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *
from pprint import pprint
from tinderAccess import authenticate, postForm

# Variables
FBTOKEN="CAAGm0PX4ZCpsBAEXAvoU1BIP0s6V5LKf9XptDNd7FTEjqv89rbBvjWl0yYL0NWQeWFXR2737Xd7SuN6oiI9irPZBY2xunpuCFL1EzXcSDXf0XT9bZCWXRdb13MMbZAGt73HX9J4DbFBE9VVVimZAKDnpuWQKqZBLI1ZCSvcxZAWbP3ie2k85CA7bnyy7MJLlHDZAUtZC90emwaE4yWp4wZArGUQCpG7Px61gf8ZD"
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


# THE ACTUAL PROGRAM
pprint(postForm("user/ping", data, token))

matches = postForm("updates", "", token)['matches']

for match in matches:
    messages = match['messages']
    for message in messages:
        if message['from'] == '552d6a6275a887851e60ab54':
            pprint("from bot")
        if message['to'] == '552d6a6275a887851e60ab54':
            pprint("to bot")
        pprint(message['message'])
        tree = parser.parse(message['message'])
        tree.draw()
        print "\n"
    pprint("###############################################################################################################################################################################################################################################")
