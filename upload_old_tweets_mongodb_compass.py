import csv
import os
import pymongo
from pymongo import MongoClient
from os import listdir
from os.path import isfile, join

'''
Script for converting csv files with old tweets by country into json files and uploading them into MongoDB Compass (locally).
'''

# Connecting
CONNECTION_STRING = "mongodb://localhost:27017/"

myclient = MongoClient(CONNECTION_STRING)

# Database
db = myclient["TweetsDB"]

# Create collections later

# Loading and uploading the json files
import pathlib
path_tweets = pathlib.Path().resolve() # get current path


old_twees_path = os.path.join(path_tweets, "old_tweets")

all_files = [f for f in listdir(old_twees_path) if isfile(join(old_twees_path, f)) and f.endswith(".csv")]


def convert_csv_to_json(file_path, file_name):
    import pandas as pd
    mydata = pd.read_csv(file_path)
    tweets = []
    for index, row in mydata.iterrows():
        tweet = {"ID": row["id"],
                "time": row["date"],
                "username": row["username"],
                "text": row["text"],
                "permalink": row["permalink"],
                "location": file_name.split("-")[0]
                 }
        tweets.append(tweet)
    return tweets



for file_name in all_files:
    abs_file_path = os.path.join(old_twees_path, file_name)
    cntr_name = str(file_name.split("-")[0])
    collection = db[cntr_name]
    with open(abs_file_path, 'r', encoding='utf-8') as f:
        file_data = csv.reader(f, delimiter=',')
        file_json = convert_csv_to_json(abs_file_path, file_name)
        collection.insert_many(file_json)
