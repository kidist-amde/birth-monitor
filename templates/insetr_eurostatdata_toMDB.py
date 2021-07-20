import json
import os
import pymongo
from pymongo import MongoClient

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bdt_db"]
mycol = mydb["eurostat_data"]

def get_unique_from_csv(path,ids):
    inserted_ids = ids
    live_birt  = []
    files = list(os.listdir(path))
    print("inserting Euro data from CSV")
    for file in tqdm.tqdm(files):
      
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
    mycol = mydb["eurostat_data"] 
    tweets = get_unique_from_csv("demo_fmonth",inserted_ids)
    x = mycol.insert_many(tweets)


    # IPython.embed()
if __name__ == "__main__":
    main()