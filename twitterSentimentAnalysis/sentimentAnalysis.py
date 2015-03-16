
doAgain = True;
while doAgain:
# Step 1 - Input and breakup
    text = getInput()
    bigrams = breakIntoBigrams(text)


# Step 2 - Analysis
    analysis = analyzeSentiment(bigrams)


# Step 3 - Feedback
    applyFeedback(analysis, bigrams)

# Check if user wants to do it again
