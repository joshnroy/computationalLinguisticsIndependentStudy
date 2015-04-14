import pymongo, nltk, sys, os, stat_parser
from pymongo import MongoClient
from stat_parser import Parser, display_tree
from nltk.tree import *

sentence = "They had been happy"

parser = Parser()

tree = parser.parse(sentence)

tree.draw()
