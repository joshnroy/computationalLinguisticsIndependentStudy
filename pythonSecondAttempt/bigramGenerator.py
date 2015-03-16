# Declare input text file
textfile = "data.txt"

# Create a dictionary to store bigrams
Bigrams = {}
# Initialize Variables
prev_word="START"
# Open and read file
for line in open(textfile):
    line = line.rstrip()

    # tokenize the text
    tokens = line.split()

    #loop over the bigrams
    for word in tokens:
        # Check to see if the bigram already exists in the dict. If it does, increase its count, else add it
        # Concatinate words to get bigram
        bigram = prev_word + ' ' + word
        if bigram in Bigrams:
            Bigrams[bigram] += 1
        else:
            Bigrams[bigram] = 1
        # Change value of prev_word
        prev_word = word

# Write Bigrams to output file
output_file = open('bigrams.txt', 'w')
for bigram in Bigrams:
    count = Bigrams[bigram]
    output_file.write(str(count)+'\t'+bigram+'\n')
output_file.close()
