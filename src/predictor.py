#!/usr/bin/env python
# coding:utf-8

"""
Script that predicts news articles based on tweets

Author: Karsten Kreis
September 2015
"""

__author__ = "Karsten Kreis"
__status__ = "Development"

# Imports
import sys
import pickle
import tweepy
import urllib2
import httplib
import json
import numpy as np
from HTMLParser import HTMLParser
from collections import Counter
from nltk.corpus import stopwords

# Get Keys (requires a module named "apikeyspath.py" with your API keys)
from apikeyspath import NYT_TOP_STORIES_KEY
from apikeyspath import TW_TOKEN_KEY, TW_TOKEN, TW_CON_SECRET_KEY, TW_CON_SECRET
from apikeyspath import PATH_TO_REPO



class Predictor(object):
    """
    Class that holds functions to recommend articles to Twitter user

    model_pickle (pickle): Pickled Logistic Regression model
    tfidf_pickle (pickle): Pickled Tfidf text vectorizer
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

        # Helper list of all single alphabetic letters
        self.singleletters = [chr(i) for i in range(97,123)] + [chr(i).upper() for i in range(97,123)]


    def fetch_tweets(self, user, number_of_tweets):
        """
        Fetches tweets for user and saves them

        user (string): twitter handle without the "@"
        number_of_tweets (int): Number of latest tweets to be read and then used for recommendation
        returns list of tweets
        """
        # List of tweets to be filled
        tweets = []

        # Get the tweets and clean them from non-alphabetic characters. Also, remove the "RT", which all retweets have. Furthermore, remove singe character words
        for status in tweepy.Cursor(self.api.user_timeline, id=user).items(number_of_tweets):
            text = status.text
            wordlist = "".join( [char if char in self.singleletters else " " for char in text] ).split()
            cleanwordlist = [word for word in wordlist if word not in self.singleletters + ["RT"]]
            tweets.append(" ".join(cleanwordlist))

        # Return the tweet list
        return tweets


    def predict_class(self, tweets, number_of_classes):
        """
        Predicts which section of the New York Times may be interesting for the user based on tweets

        tweets (list of strings): Aggregated tweets, each in one string
        number_of_classes (int): Number of classes to be recommended (It does not make much sense though, to recommend more than two or maximally three classes, beyond that it's pretty random)
        returns sorted list of most probable classes
        """
        # Vectorize tweets
        vec_tweets = self.tfidf.transform(tweets)

        # Predict label for each tweet
        pred = self.model.predict(vec_tweets)

        # Return most common labels
        try:
            returnlist = [Counter(pred).most_common(number_of_classes)[idx][0] for idx in range(number_of_classes)]
        except:
            print "ERROR:"
            print "It seems like you want to use more classes to recommend articles than predicted by the model."
            print "Try using more tweets and try to predict less classes."
            sys.exit()

        return returnlist


    def recommend_article(self, tweets, labels):
        """
        Recommend a NYT article based on the provided label

        labels (iterable over ints): encoded labels of sections to be used for recommendation
        tweets (list of strings): Aggregated tweets in one string
        returns nothing
        """

        # Set counter and get recommendation for all passed labels
        counter = 0
        for label in labels:

            # Increment counter (just for the printing part...)
            counter += 1

            # Get the top stories from the section, this should yield usually 30 artices
            request_url = "https://api.nytimes.com/svc/topstories/v2/" + self.label_dict_NYT[label] + ".json?api-key=" + NYT_TOP_STORIES_KEY
            try:
                response = urllib2.urlopen(request_url).read()
            except urllib2.HTTPError, e:
                print "Error code: " + str(e.code)
                print "Error message: " + e.msg
                print "Error hdrs:\n" + str(e.hdrs)
                sys.exit()

            # Load json response into python dictionary and randomly choose an article
            articles = json.loads(response)

            # List of Jaccard distances between articles and tweets
            jaccarddistances = []

            # Split tweets into individual words and remove stopwords
            tweetwordlist = [word for tweet in tweets for word in tweet.split() if word not in stopwords.words('english')]

            # Loop over all articles and calculate closest article to user's tweets based on Jaccard distance
            for idx in range(articles["num_results"]):

                # Use all possible informations we have about the article and feed into long string
                wordstring = " ".join([articles["results"][idx]["title"], articles["results"][idx]["abstract"], articles["results"][idx]["section"], articles["results"][idx]["subsection"], " ".join([string for string in articles["results"][idx]["des_facet"]]), " ".join([string for string in articles["results"][idx]["org_facet"]]), " ".join([string for string in articles["results"][idx]["per_facet"]])])

                # Clean all numbers, punktuation and everything else apart from alphabetic characters. Also remove single character words and stopwords
                wordlist = "".join( [char if char in self.singleletters else " " for char in wordstring] ).split()
                cleanwordlist = [word for word in wordlist if word not in self.singleletters + stopwords.words('english')]

                # Remove stopwords and calculate Jaccard distances and append to list
                jaccarddistances.append(self.jaccard_dist(tweetwordlist, cleanwordlist))

            # Argsort
            argsortedarray = np.argsort(jaccarddistances)

            # Recommend closest article
            recommended = argsortedarray[0]

            # Make some variety in the sentences...
            sentencestarts = ["You are probably", "It seems like you are also", "However, you are possibly also", "Furthermore, you could even be"]

            # Print recommendations
            if counter > 4:
                print sentencestarts[3] + " interested in the topic: " + self.label_dict[label]
            else:
                print sentencestarts[counter-1] + " interested in the topic: " + self.label_dict[label]
            print "Maybe you find the following article from this topic interesting...\n"
            print "TITLE:\n" + HTMLParser().unescape(articles["results"][recommended]["title"]) + "\n"
            print "ABSTRACT:\n" + HTMLParser().unescape(articles["results"][recommended]["abstract"]) + "\n"
            print "URL:\n" + HTMLParser().unescape(articles["results"][recommended]["url"]) + "\n\n"


    def jaccard_dist(self, list1, list2):
        """
        Computes the Jaccard distance between two lists (lists are converted into sets first)

        list1 (list): first list
        list2 (list): second list
        returns Jaccard distance (float)
        """
        # Convert lists to sets
        set1 = set(list1)
        set2 = set(list2)

        # Compute intersect of sets
        intersect = float(len(set1.intersection(set2)))

        # Calculate similarity, i.e. intersect devided by union, convert to distance, then return.
        return 1.0 - intersect / (len(set1) + len(set2) - intersect)



def main():
    """
    Main function
    """
    # Make predictor class, fetch tweets, predict_class
    MyPredictor = Predictor(model_pickle = "log_regression_model.pkl", tfidf_pickle = "tfidf_vectorizer.pkl")

    # Fetch the tweets with command line input as twitter handle
    tweets = MyPredictor.fetch_tweets(user = '{}'.format(sys.argv[1]), number_of_tweets = 100)

    # Predict the label
    labels = MyPredictor.predict_class(tweets = tweets, number_of_classes = 1)

    # Recommend an article
    MyPredictor.recommend_article(tweets = tweets, labels = labels)



if __name__ == '__main__':
    main()
