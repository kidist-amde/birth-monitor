import json
from pymongo import MongoClient
def main():
   
    myclient = MongoClient("mongodb://localhost:27017/")
    # Database
    db = myclient["bdt_db"]
    
    birth_tweets_collection = db["birth_tweets"] 
    tweets = list(birth_tweets_collection.find({}))
    with open("birth-tweets.json", "w") as output_file:
        json.dump(tweets, output_file)
    
    
    
if __name__ == '__main__':
    main()
    