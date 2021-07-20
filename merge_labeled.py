import json
from pymongo import MongoClient
def main():
   
    myclient = MongoClient("mongodb://localhost:27017/")
    # Database
    db = myclient["bdt_db"]
    
    tweets_collection = db["tweets"] 
    lt_collection = db["labeled_tweets"]
    
    output = []
    for lt  in lt_collection.find({}):
        _id = lt["_id"]
        tweet = tweets_collection.find_one({"_id":_id})
        tweet["label"] = lt["label"]
        output.append(tweet)
    with open("merged.json", "w") as output_file:
        json.dump(output, output_file)
    
    
    
if __name__ == '__main__':
    main()
    