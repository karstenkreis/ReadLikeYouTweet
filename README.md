# Read Like You Tweet

## A New York Times Article Recommendation System Based On Your Twitter Timeline

### http://readlikeyoutweet.herokuapp.com/

#### Author: Karsten Kreis

#### Overview (a very detailed description of the recommender can be found in *[underthehood.ipynb](https://github.com/kkreis/ReadLikeYouTweet/blob/master/underthehood.ipynb)*)

This project started as my final project for General Assembly's Data Science class in New York City in summer 2015. The idea is to recommend New York Times articles to Twitter users based on their tweets. This is established in the following way:

* I downloaded over 100.000 article snippets from the New York Times [Article Search API](http://developer.nytimes.com/docs/read/article_search_api_v2) and categorized them according to their sections
* I vectorized the text and created text features with a term frequency-inverse document frequency vectorizer
* I trained a multiclass Logistic Regression classifier to identify the classes

The above happened "offline". Similarly as the words in an article indicate the section it belongs to, the same words in tweets are likely to indicate that the Twitter user is interested in news from this section. Therefore, the obtained model can be used to predict a Twitter user's interests.

The program/website does the following:

* A Twitter user provides his Twitter handle
* With the [Twitter API](https://dev.twitter.com/overview/api)his 100 latest tweets are downloaded
* These tweets are processed and vectorized as the article data before and feeded into the Logistic Regression model
* This should, hopefully, yield the category the user may want to read news from

The final step:

* Connect to the New York Times [Top Stories API](http://developer.nytimes.com/docs/read/top_stories_api)
* Fetch the top story articles from the section which was predicted by the classifier. This usually yields 30 articles from this section
* Calculate the Jaccard distance between these articles and the user's tweets
* Recommend the closest article to the Twitter user


#### Possible further modifications

There are many possible improvements and extensions:


* Try to fit a stronger model, possibly using other classifiers
* Use dimensionality reduction or clustering techniques to gain further insights and/or reduce features
* Predict several probable labels and do not only recommend from one section but from several probable ones
* Scrape whole articles using webscraping tools like beautifulsoup to get whole articles instead of only headlines, snippets and keywords. This could maybe help when training the algorithm and when calculating the Jaccard distances
* Include further newspapers other than the New York Times, both for model training as well as recommendation (use for example also the Guardian, which also has a great API framework)
* Check where the user comes from (UK, US, Australia) and recommend either from NYT/Guardian US, Guardian UK, or Guardian Australia
* Extend the system beyond targeting only English twitterers and recommending only English newspaper articles
* Try to get even more user information, for example from Facebook, LinkedIn, etc., to make even better recommendations


#### Files

* *[src/articles.py](https://github.com/kkreis/ReadLikeYouTweet/blob/master/src/articles.py)*: Downloads the training data via the New York Times Article Search API
* *[src/datapreparation.py](https://github.com/kkreis/ReadLikeYouTweet/blob/master/src/datapreparation.py)*: Cleans the data
* *[src/algorithm.py](https://github.com/kkreis/ReadLikeYouTweet/blob/master/src/algorithm.py)*: Parametrizes the tf-idf vectorizer and fits the Logistic Regression model
* *[src/predictor.py](https://github.com/kkreis/ReadLikeYouTweet/blob/master/src/predictor.py)*: Connects to Twitter and New York Times Top Stories API and recommends articles to Twitter users (needs Twitter handle as command line input)
* *[underthehood.ipynb](https://github.com/kkreis/ReadLikeYouTweet/blob/master/underthehood.ipynb)*: Discusses the engine in detail and shows a few data and model visualizations as well as numbers
* *[readlikeyoutweet_schematic.png](https://github.com/kkreis/ReadLikeYouTweet/blob/master/readlikeyoutweet_schematic.png)*: Schematic visualization of the recommender's workflow
* *[website/...](https://github.com/kkreis/ReadLikeYouTweet/tree/master/website)*: Website code to implement and run the model as a heroku app in the web using flask (http://readlikeyoutweet.herokuapp.com/)

Note that I did not upload the actual datasets, the pickled logistic regression model, the pickled tfidf vectorizer and the pickled stopwords (for the website also the stopwords need to be pickled). However, with the code the data can be downloaded again and the models parametrized again.

Furthermore, note that the whole code naturally requires API keys for all involved APIs to work.
