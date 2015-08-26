#!/usr/bin/env python
# coding:utf-8

"""
Script for collecting NYT articles

Author: Karsten Kreis - kreis.karsten@googlemail.com
August 2015
"""

__author__ = "Karsten Kreis"
__maintainer__ = "Karsten Kreis"
__email__ = "kreis.karsten@googlemail.com"
__status__ = "Development"

# Imports
import urllib2
import httplib
import json
import sys
import os
import time

# Get Keys (requires a module named "apikeys.py" with your API key in the variable NYT_ARTICLE_SEARCH_KEY)
from apikeys import NYT_ARTICLE_SEARCH_KEY


class Articles(object):
    """Class that holds functions to fetch and store NYT articles"""

    def __init__(self):
        self.all_articles = []


    def fetch_articles(self, pages, items, sec_or_desk):
        """
        Fetches articles from NYT Article Search API

        pages: number of pages. Each page consists of 10 items
        section: section to fetch articles from
        sec_or_desk: If true, search in sections, otherwise in newsdesks
        """

        # Prepare search string for url
        search = "%22+%22".join(items)

        # Section or newsdesk search?
        searchtype = "section_name" if sec_or_desk else "news_desk"

        # Run over all responses for all pages
        for page in range(pages):

            # There can be only made 10 calls per second to the NYT Article API, therefore wait for 0.1 seconds before each query
            time.sleep(0.1)

            request_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=" + searchtype + ".contains%3A%28%22" + search + "%22%29+AND+document_type%3A%28%22article%22%29&fl=web_url%2Csnippet%2Clead_paragraph%2Cabstract%2Cheadline%2Ckeywords%2Cpub_date%2Cdocument_type%2Cnews_desk%2Ctype_of_material&page=" + str(page) + "&api-key=" + NYT_ARTICLE_SEARCH_KEY
            try:
                response = urllib2.urlopen(request_url).read()
            except urllib2.HTTPError, e:
                print "Error code: " + str(e.code)
                print "Error message: " + e.msg
                print "Error hdrs:\n" + str(e.hdrs)
                sys.exit()
            articles = json.loads(response)
            self.all_articles.extend(articles["response"]["docs"])


    def write_articles(self,filename):
        """
        Writes saved articles as json to disc
        """
        ### Make folder for saving the data if it does not already exist
        if not os.path.isdir("Articles"):
            cmd = "mkdir Articles"
            os.system(cmd)

        ### And save the data
        open("Articles/" + filename + ".json", "w").write(json.dumps(self.all_articles))


    def clear_articles(self):
        """
        Clears article list
        """
        self.all_articles = []




if __name__ == '__main__':

    ### Get training data for politics class by search on news desks
    CategoriesDesks = {"Politics" : ["Politics", "Washington"]}

    ### Get training data for all other classes by search on sections
    CategoriesSections = {"World" : ["World"], "US" : ["U.S."], "NY" : ["N.Y.", "NY", "New+York"], "Business" : ["Business"], "Tech" : ["Technology"], "Science" : ["Science"], "Health" : ["Health"], "Sports" : ["Sports"], "Arts" : ["Arts"], "Style" : ["Style"], "Food" : ["Food"], "Travel" : ["Travel"], "RealEstate" : ["Real+Estate"]}

    ### Initialize class and set pages
    AllArticles = Articles()
    pages = 3

    ### Query the API and collect all articles for all categories
    for key, sections in CategoriesSections.iteritems():
        print "Scraping Section " + key +" with " + str(pages) + " pages..."
        AllArticles.fetch_articles(pages = pages, items = sections, sec_or_desk = True)
        AllArticles.write_articles("Articles_" + key)
        AllArticles.clear_articles()
        print "Scraping Section " + key + " done.\n"

    for key, desks in CategoriesDesks.iteritems():
        print "Scraping Newsdesks " + key +" with " + str(pages) + " pages..."
        AllArticles.fetch_articles(pages = pages, items = desks, sec_or_desk = False)
        AllArticles.write_articles("Articles_" + key)
        AllArticles.clear_articles()
        print "Scraping Newsdesks " + key + " done.\n"
