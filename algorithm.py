#!/usr/bin/env python
# coding:utf-8

"""
Script for building and training the algorithm that predicts news article categories based on text features

Author: Karsten Kreis - kreis.karsten@gmail.com
August 2015
"""

__author__ = "Karsten Kreis"
__maintainer__ = "Karsten Kreis"
__email__ = "kreis.karsten@googlemail.com"
__status__ = "Development"

# Imports
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


class Algorithm(object):
    """
    This algorithm class has methods for training the algorithm which classifies the New York Times articles into their sections
    """
    def __init__(self):
        # Dataframe to keep the data
        self.data = pd.DataFrame()

        # Set the algorithm's model and its text vectorizer
        self.model = LogisticRegression()
        self.tfidf = TfidfVectorizer(stop_words = 'english', ngram_range=(1,2), max_features=1000, min_df=20, max_df=.1, analyzer='word')


    def loaddata(self,filename):
        """
        Loads the data

        filename (string): filename of the pickled data
        """
        self.data = pd.read_pickle(filename)


    def fitdata(self):
        """
        Parametrizes the Tfidf vectorizer and trains the classifier
        """
        # Vectorize the data
        print "Vectorizing the data..."
        X, y = self.tfidf.fit_transform(self.data.allwords).todense(), self.data.label
        print "Vectorization done\n"

        # Fit the model
        print "Fitting the model..."
        self.model.fit(X, y)
        print "Fitting done\n"


    def writemodel(self,filename_model,filename_tfidf):
        """
        Writes the model and the Tfidf vectorizer to pickle

        filename_model (string): filename of the pickled model
        filename_tfidf (string): filename of the pickled tfidf vectorizer
        """
        with open(filename_model, 'w') as f:
            pickle.dump(self.model, f)
        with open(filename_tfidf, 'w') as f:
            pickle.dump(self.tfidf, f)



def main():
    """
    Main function
    """
    MyAlgorithm = Algorithm()
    MyAlgorithm.loaddata("clean_nyt_training_data.pkl")
    MyAlgorithm.fitdata()
    MyAlgorithm.writemodel(filename_model = "log_regression_model.pkl", filename_tfidf = "tfidf_vectorizer.pkl")



if __name__ == '__main__':
    main()
