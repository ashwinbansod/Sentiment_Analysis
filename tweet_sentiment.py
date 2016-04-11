import sys
import json


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


def getTweetHappinessScore(tweet_text, sentimentDict, phraseDict):
    tweetHappinessScore = 0
    # Split tweet text into separate words
    newtweetstr = str.lower(tweet_text)

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


def computeHappiness(filename, sentimentDict, phraseDict):
    tweetHappinessScore = 0
    tweetScore = []

    # Open the tweet file,
    # Read each tweet and extract tweets to compute their happiness
    tweet_file = open(filename, 'r')

    # For every word, extract every word and add it to dictionary.
    for line in tweet_file:
        tweet = json.loads(line)
        tweetHappinessScore = 0

        # Split tweet text into separate words
        tweet_str = tweet['text']
        newtweetstr = tweet_str.replace('\n', ' ').replace('\r', '')

        # Compute happiness score for a tweet.
        tweetHappinessScore = getTweetHappinessScore(newtweetstr, sentimentDict, phraseDict)

        # Store the tweet text and its happiness score in form of tuple in a list
        # Format ( happiness_score, tweet text)
        tup = (tweetHappinessScore, newtweetstr)
        tweetScore.append(tup)
    # End of for loop.
    # Happiness score for all tweets has been computed and saved in list

    # Close the tweet file
    tweet_file.close()

    # Sort the list in descending order happiness score,
    # such that most happiest tweets are at top and saddest at bottom
    sortedHappyTweets = sorted(tweetScore, key=lambda x:x[0], reverse=True)

    return sortedHappyTweets


def printTweets(tweetsAndScore, num=10):
    # Print first 'num' happiest tweets
    for count in range(0,min(len(tweetsAndScore), num)):
        print(str(tweetsAndScore[count][0]) + ": " + tweetsAndScore[count][1])

    # Print last 'num' saddest tweets
    for count in range(max(len(tweetsAndScore)-num, 0),len(tweetsAndScore)):
        print(str(tweetsAndScore[count][0]) + ": " + tweetsAndScore[count][1])


def main():
    if len(sys.argv) != 3:
        print("ERROR: Invalid Usage: ")
        print("USAGE : python3 tweet_sentiment.py <sentiment_file> <tweet_file>")
        return 1
    else:
        sentiment_file = sys.argv[1]
        tweet_file = sys.argv[2]

    sentimentDict = {}
    phraseDict = {}
    sentimentDict = getSentimentScores(sentiment_file, phraseDict)

    # Compute happiness score of each tweet in tweet file
    tweetsAndScore = computeHappiness(tweet_file, sentimentDict, phraseDict)

    # Print the N happiest tweets and N saddest tweets
    printTweets(tweetsAndScore, 10)


if __name__ == '__main__':
    main()
