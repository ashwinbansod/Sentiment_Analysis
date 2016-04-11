import argparse
import oauth2 as oauth
import urllib.request as urllib
import json
import sys
import csv

# See Assignment 1 instructions for how to get these credentials
access_token_key = "30040161-yDUfSzoXiPrhGtbUce4iqQMp1rGyEUvD9K02SjvmU"
access_token_secret = "E1w2DH4IonpxsKl8qHwiv0CkQWjo9zeVQoTjwPcu7wLro"

consumer_key = "m0LlWbGkkBMxqXjrSnMeflaZI"
consumer_secret = "9SD9lWj3FbMKvrfRcSkycX89fu5YnVGFPMycHSOO3sSGg1RVYH"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
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
    if response.status == 200:
        for line in response:
            print (line.decode("utf-8").strip())
    # Return if response status is not success


def fetch_by_terms(term):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    parameters = [("q", term),("count", "100")]
    response = twitterreq(url, "GET", parameters)
    print (response.readline().decode("utf-8").strip())


def fetch_by_user_names(user_name_file):
    sn_file = open(user_name_file)
    user_names = sn_file.read()
    sn_file.close()

    user_names_list = user_names.split("\n")
    writer = csv.writer(sys.stdout)
    writer.writerow(['user_name', 'tweet'])

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    for uname in user_names_list:
        if uname:
            parameters = [("screen_name", uname),("count", "100"), ("include_rts", "false"), ("exclude_replies", "true")]
            response = twitterreq(url, "GET", parameters)

            if response.status == 200:
                tweet_str = response.read().decode("utf-8")
                tweets = json.loads(tweet_str)
                for tweet in tweets:
                    tweet_text = tweet['text']
                    newtweet_text = tweet_text.replace('\n', ' ').replace('\r', '')
                    writer.writerow([uname, newtweet_text])
            # else:
            #    Skip if response status is not success i.e. 200
    # End of for loop


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
        print (term)
        fetch_by_terms(term)
    elif opts.c == "fetch_by_user_names":
        user_name_file = opts.file
        fetch_by_user_names(user_name_file)
    else:
        raise Exception("Unrecognized command")
