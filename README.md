# Ksquared-News-Article-Recommender

## Recommending News Articles to Twitter Users based on their Tweets

### Author: Karsten Kreis


#### Project Outline

This project started as my final project for the General Assembly Data Science class in New York City in summer 2015. The idea is to recommend New York Times articles to Twitter users based on their tweets. This is established in the following way:

* I downloaded over 100.000 article snippets from the New York Times Article Search API and categorized them according to their sections
* I vectorized the text and created text features with a tf-idf vectorizer
* I trained a multiclass Logistic Regression classifier to identify the classes

The above is done offline. Then the program does the following:

* A user provides his twitter handle
* With the Twitter API all his tweets are downloaded
* These tweets are vectorized with the tf-idf vectorizer and inserted into the Logistic Regression model
* This should, hopefully, yield the category the user may want to read news from

The final step is the following:

* Connect to the New York Times Top Stories API
* Fetch the Top Stories from the section which was predicted by the classifier
* Recommend one or more articles from this section to the Twitter user


#### Possible further modifications

There are many possible enhancements and extensions

* Build a web interface
* Do not recommend "random" articles from the top stories of the given section but look for the smallest Jaccard distance between articles and the user's tweets and recommend accordingly
* Predict probabilities instead of labels directly and do not only recommend from one section but from several probable ones
* Do not only recommend articles from the New York Times, but also The Guardian
* Check where the user comes from (UK, US, Australia) and recommend either from NYT/Guardian US, Guardian UK, or Guardian Australia
* Fit a better model and try other classifiers
* Use dimensionality reduction or clustering techniques to gain further insights and/or reduce features

#### Files

* *articles.py*: Downloads the training data via the New York Times Article Search API
* *datapreparation.py*: Cleans the data
* *algorithm.py*: Parametrizes the tf-idf vectorizer and fits the Logistic Regression model
* *predictor.py*: Connects to Twitter and New York Times Top Stories API and recommends articles to Twitter users
* *data_exploration_visualizations.ipynb*: Shows a few data and model visualizations and numbers
