# Read Like You Tweet

## A New York Times Article Recommendation System Based On Your Twitter Timeline

### http://readlikeyoutweet.herokuapp.com/

#### Author: Karsten Kreis

#### Overview

This project started as my final project for General Assembly's Data Science class in New York City in summer 2015. The idea is to recommend New York Times articles to Twitter users based on their tweets. This is established in the following way:

* I downloaded over 100.000 article snippets from the New York Times Article Search API and categorized them according to their sections
* I vectorized the text and created text features with a term frequency-inverse document frequency vectorizer
* I trained a multiclass Logistic Regression classifier to identify the classes

The above is done offline. Similarly as the words in an article indicate the section it belongs to, the same words in tweets are likely to indicate that the Twitter user is interested in news from this section. Therefore, the obtained model can be used to predict a Twitter user's interests.

The program/website does the following:

* A Twitter user provides his Twitter handle
* With the Twitter API his 100 latest tweets are downloaded
* These tweets are processed and vectorized as the article data before and feeded into the Logistic Regression model
* This should, hopefully, yield the category the user may want to read news from

The final step is the following:

* Connect to the New York Times Top Stories API
* Fetch the top story articles from the section which was predicted by the classifier. This usually yields 30 articles from this section
* Calculate the Jaccard distance between these articles and the user's tweets
* Recommend the closest article to the Twitter user


#### Possible further modifications

There are many possible improvements and extensions:

* Try to fit a stronger model, also try other classifiers
* Use dimensionality reduction or clustering techniques to gain further insights and/or reduce features
* Predict several probable labels and do not only recommend from one section but from the several probable ones
* Include further newspapers other than the New York Times, both for model training as well as recommendation (use for example also the Guardian, which also has a great API framework)
* Check where the user comes from (UK, US, Australia) and recommend either from NYT/Guardian US, Guardian UK, or Guardian Australia
* Extend the system beyond targeting only English twitterers and recommending only English newspaper articles

#### Files

* *src/articles.py*: Downloads the training data via the New York Times Article Search API
* *src/datapreparation.py*: Cleans the data
* *src/algorithm.py*: Parametrizes the tf-idf vectorizer and fits the Logistic Regression model
* *src/predictor.py*: Connects to Twitter and New York Times Top Stories API and recommends articles to Twitter users (needs twitter handle as command line input)
* *underthehood.ipynb*: Discusses the engine in detail and shows a few data and model visualizations as well as numbers
* *website/...*: Website code to implement and run the model as a heroku app in the web using flask (http://readlikeyoutweet.herokuapp.com/)

Note that I did not upload the actual datasets, the pickled logistic regression model, the pickled tfidf vectorizer and the pickled stopwords (for the website also the stopwords need to be pickled). However, with the code the data can be downloaded again and the models parametrized again.

Furthermore, note that the whole code to work naturally requires API keys for all involved APIs.
