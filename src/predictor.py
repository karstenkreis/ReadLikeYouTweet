#!/usr/bin/env python
# coding:utf-8

"""
Script that predicts news articles based on tweets

Author: Karsten Kreis - kreis.karsten@gmail.com
August 2015
"""

__author__ = "Karsten Kreis"
__maintainer__ = "Karsten Kreis"
__email__ = "kreis.karsten@googlemail.com"
__status__ = "Development"

# Imports
import sys
import pickle
import tweepy
import urllib2
import httplib
import json
import random
from collections import Counter

# Get Keys (requires a module named "apikeyspath.py" with your API keys)
from apikeyspath import NYT_TOP_STORIES_KEY
from apikeyspath import TW_TOKEN_KEY, TW_TOKEN, TW_CON_SECRET_KEY, TW_CON_SECRET
from apikeyspath import PATH_TO_REPO



class Predictor(object):
    """
    Class that holds functions to recommend articles to Twitter user
    """

    def __init__(self, model_pickle, tfidf_pickle):
        # Load the model and the text vectorizer
        self.model = pickle.load(open(PATH_TO_REPO + "data/" + model_pickle))
        self.tfidf = pickle.load(open(PATH_TO_REPO + "data/" + tfidf_pickle))

        # Label dictionary for nice categories
        self.label_dict = {0: "Arts", 1: "Business", 2: "Food", 3: "Health", 4: "NY", 5: "Politics", 6: "RealEstate", 7: "Science", \
             8: "Sports", 9: "Style", 10: "Tech", 11: "Travel", 12: "US", 13: "World"}
        # Label dictionary for categories as they need to be put into the NYT Top Stories API
        self.label_dict_NYT = {0: "arts", 1: "business", 2: "dining", 3: "health", 4: "nyregion", 5: "politics", 6: "realestate", 7: "science", \
             8: "sports", 9: "fashion", 10: "technology", 11: "travel", 12: "national", 13: "world"}

        # Set up the Twitter access
        auth = tweepy.OAuthHandler(TW_CON_SECRET_KEY, TW_CON_SECRET)
        auth.set_access_token(TW_TOKEN_KEY, TW_TOKEN)

        # Set up the Twitter API
        self.api = tweepy.API(auth)


    def fetch_tweets(self, user):
        """
        Fetches tweets for user and saves them

        user (string): twitter handle without the "@"
        """
        # List of tweets to be filled
        tweets = []

        # List of all single alphabetic letters
        singleletters = [chr(i) for i in range(97,123)] + [chr(i).upper() for i in range(97,123)]

        # Get the tweets and clean them from non-alphabetic characters. Also, remove the "RT", which all retweets have
        for status in tweepy.Cursor(self.api.user_timeline, id=user).items(50):
            text = status.text
            wordlist = "".join( [char if char in singleletters else " " for char in text] ).split()
            cleanwordlist = [word for word in wordlist if word not in singleletters + ["RT"]]
            tweets.append(" ".join(cleanwordlist))

        # Return the tweet list
        return tweets


    def predict_class(self, tweets):
        """
        Predicts which section of the New York Times may be interesting for the user based on tweets

        tweets (list of string): Aggregated tweets in one string
        """
        # Vectorize tweets
        vec_tweets = self.tfidf.transform(tweets)

        # Predict label for each tweet
        pred = self.model.predict(vec_tweets)

        # Return most common label
        return Counter(pred).most_common(1)[0][0]


    def recommend_article(self,label):
        """
        Recommend a NYT article based on the provided label

        label (int): encoded label of section to be used for recommendation
        """

        # Get the top stories from the section
        request_url = "http://api.nytimes.com/svc/topstories/v1/" + self.label_dict_NYT[label] + ".json?api-key=" + NYT_TOP_STORIES_KEY
        try:
            response = urllib2.urlopen(request_url).read()
        except urllib2.HTTPError, e:
            print "Error code: " + str(e.code)
            print "Error message: " + e.msg
            print "Error hdrs:\n" + str(e.hdrs)
            sys.exit()

        # Load json response into python dictionary and randomly choose an article
        articles = json.loads(response)
        item = random.randint(0, articles["num_results"]-1)

        # Print recommendation
        print "Seems like you are interested in the topic: " + self.label_dict[label]
        print "Maybe you find the following article interesting...\n"
        print "TITLE:\n" + articles["results"][item]["title"] + "\n"
        print "ABSTRACT:\n" + articles["results"][item]["abstract"] + "\n"
        print "URL:\n" + articles["results"][item]["url"] + "\n"



def main():
    """
    Main function
    """
    # Make predictor class, fetch tweets, predict_class
    MyPredictor = Predictor(model_pickle = "log_regression_model.pkl", tfidf_pickle = "tfidf_vectorizer.pkl")

    # Fetch the tweets with command line input as twitter handle
    tweets = MyPredictor.fetch_tweets('{}'.format(sys.argv[1]))

    # Predict the label
    label = MyPredictor.predict_class(tweets)

    # Recommend an article
    MyPredictor.recommend_article(label)



if __name__ == '__main__':
    main()
