import json
import os
import pymongo
from pymongo import MongoClient

'''
Script for loading May and June tweets into a MongoDB locally.
'''

# Connecting
CONNECTION_STRING = "mongodb://localhost:27017/"

myclient = MongoClient(CONNECTION_STRING)

# Database
db = myclient["TweetsDB"]

# Create collections
collection_may = db["Tweets_May_2021"]
collection_june = db["Tweets_June_2021"]

# Loading and uploading the json files
import pathlib
path_tweets = pathlib.Path().resolve() # get current path

file_may = ['recent_tweets/log-0.json', 'recent_tweets/log-1.json']
file_june = ['recent_tweets/log-2.json', 'recent_tweets/log-3.json']

for file_name in file_may:
    abs_file_path = os.path.join(path_tweets, file_name)
    with open(abs_file_path, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
        collection_may.insert_many(file_data)

for file_name in file_june:
    abs_file_path = os.path.join(path_tweets, file_name)
    with open(abs_file_path, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
        collection_june.insert_many(file_data)
