# Declare input text file
textfile = "furniture.txt"

# Create a dictionary to store unigrams
Unigrams = {}
# Open and read file
for line in open(textfile):
    line = line.rstrip()

    # tokenize the text
    tokens = line.split()

    #loop over the unigrams
    for word in tokens:
        # Check to see if the unigram already exists in the dict. If it does, increase its count, else add it
        if word in Unigrams:
            Unigrams[word] += 1
        else:
            Unigrams[word] = 1

# Write Unigrams to output file
output_file = open('unigrams.txt', 'w')
for unigram in Unigrams:
    count = Unigrams[unigram]
    output_file.write(str(count)+'\t'+unigram+'\n')
output_file.close()
