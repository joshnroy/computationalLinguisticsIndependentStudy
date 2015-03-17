import json

try:
    with open('sentimentData.json', 'rb') as fp:
        sentimentData = json.load(fp)
except ValueError:
    sentimentData = {}



def getInput():
    return raw_input("Please Enter the text you would like to measure the sentiment of: ") 

def breakIntoBigrams(inputText):
    prev_word = ""
    
    tokens = inputText.split()

    for word in tokens:
        bigram = prev_word + ' ' + word
        if not bigram in sentimentData:
            sentimentData[bigram] = {'gram': bigram, 'sentiment': 0}

        prev_word = word
    return sentimentData 
def breakIntoUnigrams(inputText):
    tokens = inputText.split()

    for word in tokens:
        if not word in sentimentData:
            sentimentData[word] = {'gram': word, 'sentiment': 0}
    return sentimentData

def analyzeSentiment(inputText):
    overallSentiment = 0
    prev_word = ""
    tokens = inputText.split()
    for word in tokens:
        bigram = prev_word + ' ' + word
        if bigram in sentimentData:
            overallSentiment += sentimentData[bigram]['sentiment']
        if word in sentimentData:
            overallSentiment += sentimentData[word]['sentiment']
    print "Sentiment of the entered text was " + str(overallSentiment)
    return overallSentiment


def applyFeedback(analysis):
    feedback = input("Enter 'True' if the phrase was positive, and 'False' if the phrase was negative: ")
    if feedback:
        for gram in sentimentData:
            sentimentData[gram]['sentiment'] += 1
    else:
        for gram in sentimentData:
            sentimentData[gram]['sentiment'] -= 1



doAgain = True;
while doAgain:
# Step 1 - Input and breakup
    text = getInput()
    bigrams = breakIntoBigrams(text)
    unigrams = breakIntoUnigrams(text)


# Step 2 - Analysis
    analysis = analyzeSentiment(text)


# Step 3 - Feedback
    applyFeedback(analysis)

# Check if user wants to do it again
#    doAgain = input("Type 'True' if you want to do this again and 'False' if you don't: ")

# Save the bigrams dictionary in json format
    with open('sentimentData.json', 'wb') as fp:
        json.dump(sentimentData, fp)
