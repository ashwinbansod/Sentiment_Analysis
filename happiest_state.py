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


# def getStateAbberaviations(filename):
#     abbr_file = open(filename, 'r')
#     abbrDict = {}
#
#     for state in abbr_file:
#         abbr, state_name = state.split(":")
#         abbrDict[abbr] = state_name
#
#     abbr_file.close()
#     return abbrDict


def getStateAbberaviations():
    abbrDict = {}

    abbrDict["AL"] = "Alabama"
    abbrDict["AK"] = "Alaska"
    abbrDict["AZ"] = "Arizona"
    abbrDict["AR"] = "Arkansas"
    abbrDict["CA"] = "California"
    abbrDict["CO"] = "Colorado"
    abbrDict["CT"] = "Connecticut"
    abbrDict["DE"] = "Delaware"
    abbrDict["DC"] = "District of Columbia"
    abbrDict["FL"] = "Florida"
    abbrDict["GA"] = "Georgia"
    abbrDict["HI"] = "Hawaii"
    abbrDict["ID"] = "Idaho"
    abbrDict["IL"] = "Illinois"
    abbrDict["IN"] = "Indiana"
    abbrDict["IA"] = "Iowa"
    abbrDict["KS"] = "Kansas"
    abbrDict["KY"] = "Kentucky"
    abbrDict["LA"] = "Louisiana"
    abbrDict["ME"] = "Maine"
    abbrDict["MT"] = "Montana"
    abbrDict["NE"] = "Nebraska"
    abbrDict["NV"] = "Nevada"
    abbrDict["NH"] = "New Hampshire"
    abbrDict["NJ"] = "New Jersey"
    abbrDict["NM"] = "New Mexico"
    abbrDict["NY"] = "New York"
    abbrDict["NC"] = "North Carolina"
    abbrDict["ND"] = "North Dakota"
    abbrDict["OH"] = "Ohio"
    abbrDict["OK"] = "Oklahoma"
    abbrDict["OR"] = "Oregon"
    abbrDict["MD"] = "Maryland"
    abbrDict["MA"] = "Massachusetts"
    abbrDict["MI"] = "Michigan"
    abbrDict["MN"] = "Minnesota"
    abbrDict["MS"] = "Mississippi"
    abbrDict["MO"] = "Missouri"
    abbrDict["PA"] = "Pennsylvania"
    abbrDict["RI"] = "Rhode Island"
    abbrDict["SC"] = "South Carolina"
    abbrDict["SD"] = "South Dakota"
    abbrDict["TN"] = "Tennessee"
    abbrDict["TX"] = "Texas"
    abbrDict["UT"] = "Utah"
    abbrDict["VT"] = "Vermont"
    abbrDict["VA"] = "Virginia"
    abbrDict["WA"] = "Washington"
    abbrDict["WV"] = "West Virginia"
    abbrDict["WI"] = "Wisconsin"
    abbrDict["WY"] = "WyomingabbrDict"

    return abbrDict


def getTweetHappinessScore(tweet_text, sentimentDict, phraseDict):
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


def getHappiestState(stateScoreDict):
    stateScore = []

    # for every state in dict, compute the average tweet score and store it in tuple
    # in format (state_name, total_state_tweet_score, total_Tweets_from_state, average_tweet_score)
    for state in stateScoreDict:
        avg = float(stateScoreDict[state][0] / stateScoreDict[state][1])
        tup = (state, stateScoreDict[state][0], stateScoreDict[state][1], avg)
        stateScore.append(tup)
    # End of for loop

    return sorted(stateScore, key=lambda x:x[3], reverse=True)


def computeHappiestState(filename, sentimentDict, phraseDict, abbrDict):
    tweetHappinessScore = 0
    stateScoreDict = {}

    # Open the tweet file,
    # Read each tweet and extract tweets to compute their happiness
    tweet_file = open(filename, 'r')

    # For every word, extract every word and add it to dictionary.
    for line in tweet_file:
        tweet = json.loads(line)
        tweetHappinessScore = 0

        # If place field is not null and if country is United state
        # extract the state of the tweet to compute its average
        if tweet['place'] and tweet['place']['country'] == 'United States':
            tweet_place = tweet['place']['place_type']
            tweet_fullname = tweet['place']['full_name']

            # If place_type is 'city', 'full_name' field will be in format (CityName, State_Abbrevation)
            if tweet_place == 'city':
                state_abbr = tweet_fullname.split(',')[1].strip()
                state = abbrDict[state_abbr]
            # If place_type is 'admin', 'full_name' field will be in format (State, Country)
            elif tweet_place == 'admin':
                state = tweet_fullname.split(',')[0].strip()
            else:
                # Do nothing.
                # State is not given in tweet when place type is 'neighborhood' or 'poi' or 'country'
                continue

            # Get happiness score for tweet
            tweetHappinessScore = getTweetHappinessScore(tweet['text'], sentimentDict, phraseDict)

            # Store the summation of tweets score and number of tweets as a tuple in
            # state score dictionary
            # Format (Sum of Tweet Scores, Number of Tweets)
            if state in stateScoreDict:
                tup = (stateScoreDict[state][0] + tweetHappinessScore, stateScoreDict[state][1] + 1)
            else:
                tup = (tweetHappinessScore, 1)

            # Update the tuple for the corresponding state in dictionary.
            stateScoreDict[state] = tup
        else :
            # If place field is not present in the tweet or if country is not United state,
            # Do nothing
            continue
        # End of if statement

    # End of for Loop for each tweet in file

    # Close tweet file
    tweet_file.close()

    # Compute average and sort list
    sortedHappyState = getHappiestState(stateScoreDict)

    return sortedHappyState


def printStateHappiness(sortedHappyState):
    # Print actor happiness
    if len(sortedHappyState) < 10:
        for i in range(0, len(sortedHappyState)):
            print("%.6f" % sortedHappyState[i][3] + ": " + sortedHappyState[i][0])
    else:
        for i in range(0, 5):
            print("%.6f" % sortedHappyState[i][3] + ": " + sortedHappyState[i][0])
        for i in range(len(sortedHappyState)-5, len(sortedHappyState)):
            print("%.6f" % sortedHappyState[i][3] + ": " + sortedHappyState[i][0])


def main():
    if len(sys.argv) != 3:
        print("ERROR: Invalid Usage: ")
        print("USAGE : python3 happiest_state.py <sentiment_file> <tweet_file>")
        return 1
    else:
        sentiment_file = sys.argv[1]
        tweet_file = sys.argv[2]
        #abbreviation_file_name = "Abbreviations.txt"

    sentimentDict = {}
    abbrDict = {}
    phraseDict = {}
    sentimentDict = getSentimentScores(sentiment_file, phraseDict)

    # Get abbreviations form abbreviations file
    # abbrDict = getStateAbberaviations(abbreviation_file_name)
    abbrDict = getStateAbberaviations()

    # Compute happiest state
    sortedHappyState = computeHappiestState(tweet_file, sentimentDict, phraseDict, abbrDict)

    # Print happiness of state
    printStateHappiness(sortedHappyState)

if __name__ == '__main__':
    main()
