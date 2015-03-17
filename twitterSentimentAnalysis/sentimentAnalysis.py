import json

try:
    with open('Bigrams.json', 'rb') as fp:
        Bigrams = json.load(fp)
except ValueError:
    Bigrams = {}



def getInput():
    return raw_input("Please Enter the text you would like to measure the sentiment of: ") 
def breakIntoBigrams(inputText):
    prev_word = ""
    
    tokens = inputText.split()

    for word in tokens:
        bigram = prev_word + ' ' + word
        if not bigram in Bigrams:
            Bigrams[bigram] = {'bigram': bigram, 'sentiment': 0}

        prev_word = word
    return Bigrams

def analyzeSentiment(inputText, sentimentBigrams):
    overallSentiment = 0
    prev_word = ""
    tokens = inputText.split()
    for word in tokens:
        bigram = prev_word + ' ' + word
        if bigram in sentimentBigrams:
            overallSentiment += sentimentBigrams[bigram]['sentiment']
    print "Sentiment of the entered text was " + str(overallSentiment)
    return overallSentiment


def applyFeedback(analysis, Bigrams):
    feedback = input("Enter 'True' if this analysis was correct (or too low), and 'False' if it wasn't (or was too high): ")
    if feedback:
        for bigram in Bigrams:
            Bigrams[bigram]['sentiment'] += analysis + 1
    else:
        for bigram in Bigrams:
            Bigrams[bigram]['sentiment'] -= abs(analysis) + 1



doAgain = True;
while doAgain:
# Step 1 - Input and breakup
    text = getInput()
    bigrams = breakIntoBigrams(text)


# Step 2 - Analysis
    analysis = analyzeSentiment(text, bigrams)


# Step 3 - Feedback
    applyFeedback(analysis, bigrams)

# Check if user wants to do it again
#    doAgain = input("Type 'True' if you want to do this again and 'False' if you don't: ")

# Save the bigrams dictionary in json format
    with open('Bigrams.json', 'wb') as fp:
        json.dump(Bigrams, fp)
