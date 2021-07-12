import os
import pymongo
import json
import pandas as pd
import IPython 
import tqdm 
# stiore and return all the unique tweets 
def get_unique_from_json(path,month,ids=set()):
    inserted_ids = ids
    if month.lower() == "may":
        m = "06"
    else:
        m = "07"
    tweets  = []
    files = list(os.listdir(path))
    print("inserting tweets from Json")
    for file in tqdm.tqdm(files):
        if file.startswith("log") and file.endswith(".json"):
            file_path = os.path.join(path,file)
            with open(file_path) as f:
                mydata = json.load(f)
            for tweet in mydata:
                if tweet["ID"] not in inserted_ids:
                    # print( tweet["time"])
                    
                    day,_,year = tweet["time"].split("-")
                    tweet["time"] = "{}-{}-{}".format(year,m,day)
                    tweet["_id"] = tweet["ID"]
                    inserted_ids.add(tweet["_id"])
                    tweets.append(tweet)
    return tweets , inserted_ids                

def get_unique_from_csv(path,ids):
    inserted_ids = ids
    tweets  = []
    files = list(os.listdir(path))
    print("inserting tweets from CSV")
    for file in tqdm.tqdm(files):
        if file.endswith(".csv"):
            file_path = os.path.join(path,file)
            mydata = pd.read_csv(file_path)
            for index,row in mydata.iterrows():
                tweet = {
                    "ID":row["id"],
                    "time":row["date"],
                    "username":row["username"],
                    "text":row["text"],
                    "permalink":row["permalink"],
                    "location": file.split("-")[0]

                            }
                
                if tweet["ID"] not in inserted_ids:
                    tweet["_id"] = tweet["ID"]
                    inserted_ids.add(tweet["_id"])
                    tweets.append(tweet)
    return tweets         
def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["bdt_db"]
    mycol = mydb["tweets"]
    tweets,inserted_ids = get_unique_from_json("recent_tweets/May","May")
    
    x = mycol.insert_many(tweets)
    tweets,inserted_ids = get_unique_from_json("recent_tweets/June","June",inserted_ids)
    x = mycol.insert_many(tweets)
    tweets = get_unique_from_csv("old_tweets",inserted_ids)
    x = mycol.insert_many(tweets)


    # IPython.embed()
if __name__ == "__main__":
    main()