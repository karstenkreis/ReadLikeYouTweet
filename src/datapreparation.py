#!/usr/bin/env python
# coding:utf-8

"""
Script for cleaning and preparing the New York Times article data

Author: Karsten Kreis - kreis.karsten@googlemail.com
August 2015
"""

__author__ = "Karsten Kreis"
__maintainer__ = "Karsten Kreis"
__email__ = "kreis.karsten@googlemail.com"
__status__ = "Development"

# Imports
import glob
import json
import pandas as pd
import numpy as np
import os

# Get path to repository (requires a module named "apikeyspath.py" with path to repo)
from apikeyspath import PATH_TO_REPO


class DataPolisher(object):
    """
    Class that holds functions to clean and prepare the NYT article data
    """

    def __init__(self):
        # Dataframe to keep the data
        self.data = pd.DataFrame()


    def loaddata(self, folder):
        """
        Loads the data

        folder (string): folder in which to look for the datafiles
        returns nothing
        """

        # Loop over all sections
        for idx, section in enumerate(["Arts", "Business", "Food", "Health", "NY", "Politics", "RealEstate", "Science", "Sports", "Style", "Tech", "Travel", "US", "World"]):

            # Get files and set up empty dataframe and list
            files = glob.glob(PATH_TO_REPO + folder + "/Articles_" + section + "*.json")
            sectiondata = pd.DataFrame()
            list_ = []

            # Loop over all files, read data into dataframe and append to list
            for file_ in files:
                df = pd.read_json(file_)
                list_.append(df)

            # Combine all frames and label them
            sectiondata = pd.concat(list_)
            sectiondata["label"] = idx

            # Combine all on class' data variable
            self.data = pd.concat([self.data,sectiondata])


    def cleandata(self):
        """
        Cleans the data

        returns nothing
        """

        # Drop empty entries
        self.data = self.data.dropna(subset = ['allwords'])

        # Drop all columns but "allwords" and "label", convert to string
        self.data.drop(self.data.columns[[0,2,3,4,5,6,8,9,10,11,12,13]], axis=1, inplace=True)
        self.data["allwords"] = self.data["allwords"].astype(str)

        # Make length feature
        self.data["length"] = self.data["allwords"].apply(lambda x: len(x.split()))

        # Drop all empty ones
        self.data = self.data[self.data["length"] != 0]

        # Reset index and drop added column
        self.data = self.data.reset_index()
        self.data.drop('index', axis=1, inplace=True)

        # Shuffle the dataframe, reset index and clean
        self.data = self.data.reindex(np.random.permutation(self.data.index))
        self.data = self.data.reset_index()
        self.data.drop('index', axis=1, inplace=True)


    def writedata(self, filename):
        """
        Writes the data to pickle

        filename (string): filename for pickled datafile
        returns nothing
        """

        # Make folder for saving the data if it does not already exist
        if not os.path.isdir(PATH_TO_REPO + "data"):
            cmd = "mkdir {}data".format(PATH_TO_REPO)
            os.system(cmd)

        self.data.to_pickle(PATH_TO_REPO + "data/" + filename)



def main():
    """
    Main function
    """
    # Make class, then load, clean and write data
    MyDataPolisher = DataPolisher()
    MyDataPolisher.loaddata(folder = "articles")
    MyDataPolisher.cleandata()
    MyDataPolisher.writedata(filename = "clean_nyt_training_data.pkl")



if __name__ == '__main__':
    main()
