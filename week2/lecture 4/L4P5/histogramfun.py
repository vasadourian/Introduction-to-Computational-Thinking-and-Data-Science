import pylab

# You may have to change this path
WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of uppercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def plotVowelProportionHistogram(wordList, numBins=15):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """
    vowelCount = 0
    consonantCount = 0
    totalWordLength = 0
    for word in wordList:
        totalWordLength += len(word)
        for x in word:

            if x == 'a' or x =='e' or x =='i' or x =='u':
                vowelCount += 1
            else:
                consonantCount += 1
    #print "Number of vowels: ", vowelCount
    #print "Number of consonants: ", consonantCount
    avgLengthWord = float( totalWordLength / len(wordList) )
    avgVowelperWord = float( (totalWordLength / vowelCount)  )
    print avgVowelperWord
    
    numVowel = []
    for word in wordList:
        vowelInWord = 0
        for x in word:
            
            if x == 'a' or x =='e' or x =='i' or x =='u':
                vowelInWord += 1
            else: 
                continue
        numVowel.append(vowelInWord)
    
    less3 = []
    for x in numVowel:
        if x < 3:
            less3.append(x)

    ## logic above is correct but for some reason I can't get this to print the correct value. Prints 0.0. Has to do with float(), surely.
    print float( len(less3) / len(numVowel) )
if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)
