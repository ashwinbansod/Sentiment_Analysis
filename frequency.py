import sys
import json


def getStopWords(fileName):
    stopword_file = open(fileName, 'r')
    stopeord_string = stopword_file.read()
    stopword_file.close()

    stopword_list = stopeord_string.split('\n')
    stopword_dict = {}

    for word in stopword_list:
        stopword_dict[word] = ''

    return stopword_dict


def addWordToDict(word, wordDict):
    wordCount = 0

    # Add word in dictionary and update word count
    # Increment the word count if it is in dict
    # or add new word in dict
    if word in wordDict:
        wordDict[word] += 1
        wordCount += 1
    else:
        wordDict[word] = 1
        wordCount += 1

    return wordCount


def calculateFrequency(wordDict, totalWordCount):
    wordFrequencyList = []
    # Frequency for each word is given by
    # [# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets]
    for word in wordDict:
        freq = 0
        freq = round(wordDict[word]/totalWordCount, 6)
        tup = (word, freq)
        wordFrequencyList.append(tup)

    sortedFreqList = sorted(wordFrequencyList, key=lambda x:x[1], reverse=True)

    return sortedFreqList


def checkWordType(word, stopwordDict):
    retVal = 'NONE'

    if word in stopwordDict:
        retVal = 'STOP_WORD'
    elif word[0] == '@':
        retVal = 'NAME_TAG'
    elif word[0] == '#':
        retVal = 'HASH_TAG'
    elif word[0:7] == 'http://' or word[0:8] == 'https://':
        retVal = 'LINK'
    elif str.isalpha(word):
        retVal = 'NORMAL'
    else:
        retVal = 'NONE'

    return retVal


class ComputeFrequency:
    wordFreqList = []
    nameTagFreqList = []
    hashTagFreqList = []
    linkFreqList = []
    allFreqList = []
    totalWordCount = 0

    def extractFrequency(self, filename, stopwordDict):
        nameTagWordDict = {}
        hashTagWordDict = {}
        linkWordDict = {}
        allWordDict = {}
        wordDict = {}

        # Open the tweet file,
        # Read each tweet and extract words and calculate their frequency
        tweet_file = open(filename, 'r')

        # For every word, extract every word and add it to dictionary.
        for line in tweet_file:
            tweet = json.loads(line)

            # Split tweet text into separate words
            wordList = tweet['text'].split(' ')

            for word in wordList:
                wordtype = checkWordType(str.lower(word), stopwordDict)

                # Add word in dictionary
                if wordtype == 'NAME_TAG':
                    self.totalWordCount += addWordToDict(word, nameTagWordDict)
                    addWordToDict(word, allWordDict)
                elif wordtype == 'HASH_TAG':
                    self.totalWordCount += addWordToDict(word, hashTagWordDict)
                    addWordToDict(word, allWordDict)
                elif wordtype == 'LINK':
                    self.totalWordCount += addWordToDict(word, linkWordDict)
                    addWordToDict(word, allWordDict)
                elif wordtype == 'NORMAL': # word is of NORMAL type
                    self.totalWordCount += addWordToDict(str.lower(word), wordDict)
                    addWordToDict(str.lower(word), allWordDict)
                else:  # If word type is STOP_WORD or NONE then skip the word.
                    continue

        # Close tweet file
        tweet_file.close()

        # Now compute the frequency of each word.
        self.allFreqList = calculateFrequency(allWordDict, self.totalWordCount)

        # Now compute the frequency of each word.
        self.wordFreqList = calculateFrequency(wordDict, self.totalWordCount)

        # Now compute the frequency of each Name Tag.
        self.nameTagFreqList = calculateFrequency(nameTagWordDict, self.totalWordCount)

        # Now compute the frequency of each Hash Tag.
        self.hashTagFreqList = calculateFrequency(hashTagWordDict, self.totalWordCount)

        # Now compute the frequency of each Link.
        self.linkFreqList = calculateFrequency(linkWordDict, self.totalWordCount)

        return 0


    def printDistrubutedFrequency(self, num=20):
        print("Frequency of all Words:")
        for i in range(0, min(len(self.allFreqList), num)):
            print(str(self.allFreqList[i][0]) + " " + "%.10f" % self.allFreqList[i][1])

        print("\n\nFrequency of Normal Words:")
        for i in range(0, min(len(self.wordFreqList), num)):
            print(str(self.wordFreqList[i][0]) + " " + "%.10f" % self.wordFreqList[i][1])

        print("\n\nFrequency of Name Tags:")
        for i in range(0, min(len(self.nameTagFreqList), num)):
            print(str(self.nameTagFreqList[i][0]) + " " + "%.10f" % self.nameTagFreqList[i][1])

        print("\n\nFrequency of Hash Tags:")
        for i in range(0, min(len(self.hashTagFreqList), num)):
            print(str(self.hashTagFreqList[i][0]) + " " + "%.10f" % self.hashTagFreqList[i][1])

        print("\n\nFrequency of Links:")
        for i in range(0, min(len(self.linkFreqList), num)):
            print(str(self.linkFreqList[i][0]) + " " + "%.10f" % self.linkFreqList[i][1])


    def printFrequency(self, num=20):
        # print("Frequency of all Words:")
        if num == -1:
            end = len(self.allFreqList)
        else:
            end = min(len(self.allFreqList), num)

        for i in range(0, end):
            print(str(self.allFreqList[i][0]) + " " + "%.10f" % self.allFreqList[i][1])

# End of class

def printUsage():
    print("Invalid Usage: ")
    print("USAGE : python3 frequency.py <stopword_file> <tweet_file> [Print Distributed frequency (Y/N)]")

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        printUsage()
        return 1
    else:
        stopword_file = sys.argv[1]
        tweet_file = sys.argv[2]

        if len(sys.argv) == 4:
            print_distributed_frequency = str.lower(sys.argv[3])

            if print_distributed_frequency != 'n' and print_distributed_frequency != 'y' :
                printUsage()
                return 1
        else:
            # If 4th argument (print_distributed_frequency) is not specified,
            # then by default set print_distributed_frequency to NO
            print_distributed_frequency = 'n'

    cf = ComputeFrequency()
    stopwordDict = getStopWords(stopword_file)
    cf.extractFrequency(tweet_file, stopwordDict)

    if print_distributed_frequency == 'n':
        # Print top 30 frequently used words.
        cf.printFrequency(-1)
    else:
        # Print distributed frequency
        cf.printDistrubutedFrequency(30)


if __name__ == '__main__':
    main()
