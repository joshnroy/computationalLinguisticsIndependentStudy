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
learningCorpusName = sys.argv[1]

# Global Settings Variables
searchHeight = 2

# Opening the learning corpus
with open(learningCorpusName) as f:
    learningCorpus = f.read().replace('\n', ' ').decode('utf-8')

# Do the processing and the learning
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(learningCorpus.strip())
    parser = Parser()
    for sentence in sentences:
        try:
            tree = parser.parse(sentence)
        except TypeError as e:
            pass
            # print str(e)
        for subjectPhrase in tree.subtrees(filter=lambda x: x.label() == 'S'):
            verb = ''
            pronoun = ''
            oldVerb = ''
#                subjectPhrase.draw()
            for nounPhrase in subjectPhrase.subtrees(filter=lambda x: x.label() == 'NP'):
                for nounWord in nounPhrase.subtrees(filter=lambda x: x.label() == 'N' or x.label() == 'NN' or x.label() == 'NNP' or x.label() == 'NNS'):
                    if nounWord.label() == 'NNS':
                        pronoun = 'they'
                for pronounPhrase in nounPhrase.subtrees(filter=lambda x: x.label() == 'PRP'):
                    pronoun = pronounPhrase[0]
                if pronoun == '' or pronoun == 'he' or pronoun == 'she':
                    pronoun = 'it'
            for verbPhrase in subjectPhrase.subtrees(filter=lambda x: x.label() == 'VP'):
                for verbWord in verbPhrase.subtrees(filter=lambda x: x.label() == 'VB' or x.label() == 'VBD' or x.label() == 'VRB' or x.label() == 'VBZ' or x.label() == 'VBP' or x.label() == 'VBN'):
                    if oldVerb != '':
                        try:
                            if oldVerb.label() == 'VBP':
                                verb = oldVerb[0] +  ' ' + verbWord[0]
                            elif oldVerb.label() == 'VBD':
                                if type(oldVerb) != str:
                                    # print "Adding \t" + oldVerb[0] + "\t and \t " + verbWord[0] + "\t NOT STRING"
                                    verb = oldVerb[0] + ' ' + verbWord[0]
                                else:
                                    # print "Adding \t" + oldVerb + "\t and \t " + verbWord[0] + "\t STRING"
                                    verb = oldVerb + ' ' + verbWord[0]
                        except AttributeError as e:
                            pass
                        if verbWord.label() == 'VBN':
                            if type(oldVerb) is not unicode:
                                # print "Adding \t" + oldVerb[0] + "\t and \t " + verbWord[0] + "\t NOT STRING"
                                verb = oldVerb[0] + ' ' + verbWord[0]
                            else:
                                # print "Adding \t" + oldVerb + "\t and \t " + verbWord[0] + "\t STRING"
                                verb = oldVerb + ' ' + verbWord[0]
                        else:
                            verb = verbWord
                    else:
                        verb = verbWord
                    # print pronoun
                    # print str(oldVerb) + "\t OLDVERB\t" + str(type(oldVerb))
                    # print verb
                    # print '\n'
                    oldVerb = verb
# Insert into the database here
            if type(verb) == nltk.tree.Tree:
                verb = verb[0]
            if verb != '' and pronoun != '':
                pronounVerbPhrase = {"pronoun": pronoun,
                                    "verb": verb}
                print pronounVerbPhrase
