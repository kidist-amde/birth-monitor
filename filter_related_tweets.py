import json
from pymongo import MongoClient
import pandas as pd
import tqdm
def main():
   
    myclient = MongoClient("mongodb://localhost:27017/")
    # Database
    db = myclient["bdt_db"]
    
    tweets_collection = db["tweets"] 
    positive_collection = db["birth_tweets"] 
    df = pd.read_csv("tweets-labels.csv")    
    for index,row in tqdm.tqdm(df.iterrows(),total = len(df)):
        if row["label"] == 1 :
            _id = row["id"]
            tweet = tweets_collection.find_one({"_id":int(_id)})
            if tweet is None:
                raise ValueError("id not found : {}".format(_id) )
            else:
                positive_collection.insert_one(tweet)
    
    
    
    
if __name__ == '__main__':
    main()
    