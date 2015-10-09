#!/usr/bin/env python
# coding:utf-8

"""
Script that uses Flask to implement the New York Times article recommender on a website

Author: Karsten Kreis
September 2015
"""

__author__ = "Karsten Kreis"
__status__ = "Development"

# Imports
from flask import Flask, render_template, request
import predictor

# Initialize Flask app and the predictor
app = Flask(__name__)
MyPredictor = predictor.Predictor(model_pickle = "log_regression_model.pkl", tfidf_pickle = "tfidf_vectorizer.pkl", stopwords_pickle = "stopwords.pkl")

# Render the normal website
@app.route('/')
def index():
    return render_template('/index.html')

# When the Twitter Handle is provided and the recommendation engine runs
@app.route('/show', methods=['GET', 'POST'])
def show_tweets():

    # Twitter handle
    twitterhandle = request.form['screen_name'].encode('ascii', 'ignore').lower().strip()

    # Tweets, section, recommendation
    try:
        tweets = MyPredictor.fetch_tweets(user = twitterhandle, number_of_tweets = 100)
        labels = MyPredictor.predict_class(tweets = tweets, number_of_classes = 1)
        label, title, abstract, url = MyPredictor.recommend_article(tweets = tweets, label = labels[0])

    # Error? Probably the Twitter handle was unknown
    except:
        return render_template('/index.html', twitterhandle = "", topic = "An error occured - maybe the Twitter user does not exist or there are no tweets?", bla = "Entered Twitter handle was: " + twitterhandle, title = "", abstract = "" , url = "")

    # Otherwise return recommendation and reload the website including this data
    return render_template('/index.html', twitterhandle = "Your Twitter handle: " + twitterhandle, topic = "You are probably interested in this topic: " + str(label), bla = "Maybe you find the following article from this topic interesting... ", title = "TITLE: " + title, abstract = "ABSTRACT: " + abstract, url = url)

# Run the server
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=False) # Never have debug = True when hosting a public website!
