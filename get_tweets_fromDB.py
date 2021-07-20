import json
from pymongo import MongoClient
def main():
   
    myclient = MongoClient("mongodb://localhost:27017/")
    # Database
    db = myclient["bdt_db"]
    
    tweets_collection = db["tweets"] #labeled_tweets
    tweets = list(tweets_collection.find({}))
    with open("db-tweets.json", "w") as output_file:
        json.dump(tweets, output_file)
    
    
    
if __name__ == '__main__':
    main()
    