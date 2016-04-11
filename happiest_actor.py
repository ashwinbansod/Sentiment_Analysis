import sys
import csv


def getSentimentScores(filename, phraseDict):
    sentiment_file = open(filename, 'r')
    sentiDict = {}

    for sentiment in sentiment_file:
        term, score = sentiment.split("\t")

        # If the term is more than 1 word long, store it as a phrase in phraseDict
        # otherwise store it as a sentiment in sentiment dict
        if len(term.split(' ')) > 1 :
            phraseDict[term] = float(score)
        else:
            sentiDict[term] = float(score)

    sentiment_file.close()
    return sentiDict


def computeHappinessScore(tweet_text, sentimentDict, phraseDict):
    tweetHappinessScore = 0
    # Split tweet text into separate words
    newtweetstr = str.lower(tweet_text.replace('\n', ' ').replace('\r', ''))

    # Check if any phrase in phraseDict exist in tweet,
    # Add its sentiment value to total
    # otherwise skip it.
    for phrase in phraseDict:
        if phrase in newtweetstr:
            tweetHappinessScore += phraseDict[phrase]
        else:
            # Do nothing
            continue

    # Split the tweet text into word list
    wordList = newtweetstr.split(' ')

    # Check for each word in word list, if it exist in setimentDict,
    # Add its sentiment value to total
    # otherwise skip it.
    for word in wordList:
        if word in sentimentDict:
            tweetHappinessScore += sentimentDict[word]
        else:
            # Do nothing
            continue

    return tweetHappinessScore


def findActorsSentiment(filename, sentimentDict, phraseDict):
    actorDict = {}
    username = ""
    prevUserName = ""

    csv_file = open(filename, 'r')
    csv_file_reader = csv.reader(csv_file)

    # Skip first line ('username', 'tweet')
    next(csv_file_reader, None)

    for tweet in csv_file_reader:
        # Get username of the tweet.
        username = tweet[0]

        # Compute tweet score.
        tweetscore = computeHappinessScore(''.join(tweet[1:]), sentimentDict, phraseDict)

        if username in actorDict:
            totaltweetscore = actorDict[username][1] + tweetscore
            tweetcount = actorDict[username][2] + 1
            tweetscoreavg = float(totaltweetscore/tweetcount)

            # Add values to a tuple (actor_name, tweet_score, tweet_count, avg)
            tup = (username, totaltweetscore, tweetcount, tweetscoreavg)
        else:
            tweetscoreavg = float(tweetscore)
            # Add values to a tuple (actor_name, tweet_score, tweet_count, avg)
            tup = (username, tweetscore, 1, tweetscoreavg)

        actorDict[username] = tup

    # End of for loop

    actorList = []
    for actor in actorDict:
        actorList.append(actorDict[actor])

    sortedActorList = sorted(actorList, key=lambda x:x[3], reverse=True)
    return sortedActorList


def printActorHappiness(actorList):
    # Print actor happiness
    for i in range(0, len(actorList)):
        print("%.6f" % actorList[i][3] + ": " + actorList[i][0])

def main():
    if len(sys.argv) != 3:
        print("ERROR: Invalid Usage: ")
        print("USAGE : python3 happiest_actor.py <sentiment_file> <csv_file>")
        return 1
    else:
        sentiment_file = sys.argv[1]
        tweet_file = sys.argv[2]

    sentimentDict = {}
    phraseDict = {}
    actorList = []
    sentimentDict = getSentimentScores(sentiment_file, phraseDict)

    actorList = findActorsSentiment(tweet_file, sentimentDict, phraseDict)

    printActorHappiness(actorList)

if __name__ == '__main__':
    main()
