import argparse
import oauth2 as oauth
import urllib.request as urllib
import json
import csv
import sys

# See Assignment 1 instructions for how to get these credentials
access_token_key = "705835047132250112-43GaY98STh8523pZ28jawDSsXH90EC5"
access_token_secret = "1XCC9I92kNoTkZS0Tse6r3KXe8bQ614vTeapjvRuVQIJk"

consumer_key = "E7sxlcziCV5VEJVbDKa6SaCFa"
consumer_secret = "O4tgHu0se8AB90Vpw2UOlTYTMxAnJsCUxWKrr2Aj1GeOGy4zhl"

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''


def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetch_samples():
    url = "https://stream.twitter.com/1.1/statuses/sample.json?language=en"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        print(line.strip())


def fetch_by_terms(term):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    parameters = [("q", term), ("count", "100")]
    response = twitterreq(url, "GET", parameters)
    print(response.readline())


def fetch_by_user_names(user_name_file):
    sn_file = open(user_name_file)
    user_names = sn_file.read()
    sn_file.close()
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    user_names_list = user_names.split("\n")
    user_name_dict = {}
    for user_name in user_names_list:
        user_name = user_name.strip()
        if user_name:
            parameters = [("screen_name", user_name), ("count", "100")]
            response = twitterreq(url, "GET", parameters)
            tweet_string = response.read().decode("utf-8")
            tweets = json.loads(tweet_string)
            if response.status == 200:
                user_name_dict[user_name] = []
                for single_tweet in tweets:
                    user_name_dict[user_name].append(single_tweet['text'].encode("utf-8"))
            # else:
                # Skip this error part
                # print("ERROR ACCESSING API [" + tweets["error"] + "]")

    writer = csv.writer(sys.stdout)
    writer.writerow(["user_names", "tweets"])
    for single_user_name in user_name_dict:
        for tweet in user_name_dict[single_user_name]:
            writer.writerow([single_user_name, tweet])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required=True, help='Enter the command')
    parser.add_argument('-term', help='Enter the search term')
    parser.add_argument('-file', help='Enter the user name file')
    opts = parser.parse_args()
    if opts.c == "fetch_samples":
        fetch_samples()
    elif opts.c == "fetch_by_terms":
        term = opts.term
        print(term)
        fetch_by_terms(term)
    elif opts.c == "fetch_by_user_names":
        user_name_file = opts.file
        fetch_by_user_names(user_name_file)
    else:
        raise Exception("Unrecognized command")
