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
* With the Twitter API his 100 latest tweets are downloaded
* These tweets are vectorized with the tf-idf vectorizer and inserted into the Logistic Regression model
* This should, hopefully, yield the category the user may want to read news from

The final step is the following:

* Connect to the New York Times Top Stories API
* Fetch the Top Stories from the section which was predicted by the classifier, this usually yields 30 top-stories articles from this section
* Calculate the Jaccard distance between these articles and the user's tweets
* Recommend the "closest" article to the Twitter user


#### Possible further modifications

There are many possible enhancements and extensions

* Build a web interface
* Predict several probable labels and do not only recommend from one section but from the most probable ones
* Do not only recommend articles from the New York Times, but also The Guardian (has similar categories and also an API) or other newspapers
* Check where the user comes from (UK, US, Australia) and recommend either from NYT/Guardian US, Guardian UK, or Guardian Australia
* Fit a better model and try other classifiers
* Use dimensionality reduction or clustering techniques to gain further insights and/or reduce features

#### Files

* *src/articles.py*: Downloads the training data via the New York Times Article Search API
* *src/datapreparation.py*: Cleans the data
* *src/algorithm.py*: Parametrizes the tf-idf vectorizer and fits the Logistic Regression model
* *src/predictor.py*: Connects to Twitter and New York Times Top Stories API and recommends articles to Twitter users
* *data_exploration/data_exploration_visualizations.ipynb*: Shows a few data and model visualizations and numbers
* *website/website.py*: Runs the model on a website using flask
* *website/predictor.py*: Modified predictor to return the recommendations and not just print them in the shell
* *website/ ...*: Further files implement the actual website (design by http://templated.co/)

(Note that I did not upload the actual datasets, the pickled logistic regression model and the pickled tfidf vectorizer. However, with the code the data can be scraped again and the models parametrized again)
