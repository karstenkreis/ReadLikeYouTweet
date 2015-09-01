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

# Get keys (requires a module named "apikeyspath.py" with your API key in the variable NYT_ARTICLE_SEARCH_KEY) and path to repository
from apikeyspath import NYT_ARTICLE_SEARCH_KEY
from apikeyspath import PATH_TO_REPO


class Articles(object):
    """
    Class that holds functions to fetch and store NYT articles
    """

    def __init__(self):
        # List of all articles
        self.all_articles = []


    def fetch_articles(self, pages, items, sec_or_desk, begin_date, end_date):
        """
        Fetches articles from NYT Article Search API

        pages (int): number of pages. Each page consists of 10 items
        items (list of strings): list of items used as keywords to fetch articles from
        sec_or_desk (boolean): If true, search in sections, otherwise in newsdesks
        begin_date (int): Begin date as YYYYMMDD
        end_date (int): End date as YYYYMMDD
        """
        # Prepare search string for url
        search = "%22+%22".join(items)

        # Section or newsdesk search?
        searchtype = "section_name" if sec_or_desk else "news_desk"

        # List of all single alphabetic letters
        singleletters = [chr(i) for i in range(97,123)] + [chr(i).upper() for i in range(97,123)]

        # Counter for bad articles, which are not processed due to missing data
        badcount = 0

        # Run over all responses for all pages
        for page in range(pages):

            # There can be only made 10 calls per second to the NYT Article API, therefore wait for 0.1 seconds before each query
            time.sleep(0.1)

            # Get the data
            request_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=" + searchtype + ".contains%3A%28%22" + search + "%22%29&fl=web_url%2Csnippet%2Clead_paragraph%2Cabstract%2Cheadline%2Ckeywords%2Cpub_date%2Cdocument_type%2Cnews_desk%2Ctype_of_material&page=" + str(page) + "&begin_date=" + str(begin_date) + "&end_date=" + str(end_date) + "&api-key=" + NYT_ARTICLE_SEARCH_KEY
            try:
                response = urllib2.urlopen(request_url).read()
            except urllib2.HTTPError, e:
                print "Error code: " + str(e.code)
                print "Error message: " + e.msg
                print "Error hdrs:\n" + str(e.hdrs)
                sys.exit()

            # Load json response into python dictionary and reorganize some data
            articles = json.loads(response)
            articles_smooth = articles["response"]["docs"]
            for i in range(len(articles_smooth)):

                # Make header column. If this fails, skip the article
                try:
                    articles_smooth[i]["header"] = articles_smooth[i]["headline"]["main"]
                except:
                    badcount += 1
                    print "Bad article #" + str(badcount) + ", skip and continue..."
                    continue

                # Make keywordlist column. If this fails, skip the article
                try:
                    articles_smooth[i]["keywordlist"] = " ".join([item["value"] for item in articles_smooth[i]["keywords"]])
                except:
                    badcount += 1
                    print "Bad article #" + str(badcount) + ", skip and continue..."
                    continue

                # Make column with all word features. If this fails, skip the article. Also note that blogpost do not have the lead_paragraph feature
                try:
                    if articles_smooth[i]["document_type"] == "blogpost":
                        articles_smooth[i]["allwords"] = " ".join([articles_smooth[i]["header"], articles_smooth[i]["keywordlist"], articles_smooth[i]["snippet"]])
                    else:
                        articles_smooth[i]["allwords"] = " ".join([articles_smooth[i]["header"], articles_smooth[i]["keywordlist"], articles_smooth[i]["lead_paragraph"], articles_smooth[i]["snippet"]])
                except:
                    badcount += 1
                    print "Bad article #" + str(badcount) + ", skip and continue..."
                    continue

                # Clean all non alphabetic characters and throw away individual letters
                wordlist = "".join( [char if char in singleletters else " " for char in articles_smooth[i]["allwords"]] ).split()
                cleanwordlist = [word for word in wordlist if word not in singleletters]

                # Join as string, convert into regular string, and copy back onto allwords
                articles_smooth[i]["allwords"] = " ".join(cleanwordlist)

                # Delete old keywords and headline columns
                del articles_smooth[i]["keywords"]
                del articles_smooth[i]["headline"]

            # Append to all articles
            self.all_articles.extend(articles_smooth)


    def write_articles(self,filename):
        """
        Writes saved articles as json to disc

        filename (string): filename with directory called "Articles"
        """
        # Make folder for saving the data if it does not already exist
        if not os.path.isdir(PATH_TO_REPO + "articles"):
            cmd = "mkdir {}articles".format(PATH_TO_REPO)
            os.system(cmd)

        # And save the data
        open(PATH_TO_REPO + "articles/" + filename + ".json", "w").write(json.dumps(self.all_articles))


    def clear_articles(self):
        """
        Clears article list
        """
        self.all_articles = []



def main():
    """
    Main function
    """
    # Get training data for politics class by search on news desks
    CategoriesDesks = {"Politics" : ["Politics", "Washington"]}

    # Get training data for all other classes by search on sections
    CategoriesSections = {"World" : ["World"],"US" : ["U.S."], "NY" : ["N.Y.", "NY", "New+York"], "Business" : ["Business"], "Tech" : ["Technology"], "Science" : ["Science"], "Health" : ["Health"], "Sports" : ["Sports"], "Arts" : ["Arts"], "Style" : ["Style"], "Food" : ["Food"], "Travel" : ["Travel"], "RealEstate" : ["Real+Estate"]}

    # Initialize class, set pages as well as begindates and enddates
    AllArticles = Articles()
    pages = 100

    # Define begin and end dates
    begin_dates = [20150301, 20140901, 20140301, 20130901, 20130301, 20120901, 20120301, 20110901, 20110301, 20100901]
    end_dates = [20150827, 20150228, 20140831, 20140228, 20130831, 20130228, 20120831, 20120229, 20110831, 20110228]

    # Query the API and collect all articles for all categories (note that you typically cannot do this in one run, as the article API allows only 10.000 calls per day)
    for key, sections in CategoriesSections.iteritems():
        print "Scraping Section " + key + "..."
        for start, end in zip(begin_dates, end_dates):
            AllArticles.fetch_articles(pages = pages, items = sections, sec_or_desk = True, begin_date = start, end_date = end)
            AllArticles.write_articles("Articles_" + key + "_start" + str(start) + "_end" + str(end))
            AllArticles.clear_articles()
        print "Scraping Section " + key + " done.\n"

    for key, desks in CategoriesDesks.iteritems():
        print "Scraping Newsdesks " + key + "..."
        for start, end in zip(begin_dates, end_dates):
            AllArticles.fetch_articles(pages = pages, items = desks, sec_or_desk = False, begin_date = start, end_date = end)
            AllArticles.write_articles("Articles_" + key  + "_start" + str(start) + "_end" + str(end))
            AllArticles.clear_articles()
        print "Scraping Newsdesks " + key + " done.\n"



if __name__ == '__main__':
    main()
