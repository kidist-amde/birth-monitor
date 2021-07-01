import pandas as pd
import tweepy 
import json
import os
from config import *
from datetime import datetime


# The followinfg function save last tweet Id 

def save_last_id(tweet_id):
    file_name = "recent_tweets/last_saved_tweet.json"
    if not os.path.exists(file_name):
        d = dict(last_tweet_id = tweet_id) 
        with open(file_name,'w' ) as f:
            json.dump(d,f)
    else:
        with open(file_name,'r' ) as f:
            d = json.load(f)
        if d["last_tweet_id"]<tweet_id:
            d["last_tweet_id"] = tweet_id
            with open(file_name,'w' ) as f:
                json.dump(d,f)
# save diffrent version of the file
def get_file_number():
    log_file = "recent_tweets/last_log.json"
    if not os.path.exists(log_file):
        d = dict(file_number = 0) 
        with open(log_file,'w' ) as f:
            json.dump(d,f)
    else:
        with open(log_file,'r' ) as f:
            d = json.load(f)
        d["file_number"]+=1
        with open(log_file,'w' ) as f:
                json.dump(d,f)
    return d["file_number"]
        
def main():
    if not os.path.exists("recent_tweets"):
        os.mkdir("recent_tweets")
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key_, api_secret_key)
    auth.set_access_token(Access_Token, Access_Token_Secret)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key_, api_secret_key)
    auth.set_access_token(Access_Token, Access_Token_Secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)


    words=["I.*(m|am|’m).*(weeks|months).*pregnant.", "my" and "pregnancy", "pregnant", "baby" and "our family", 
        "baby coming soon", "I.*(m|am|’m).* been.*(weeks|months).*" and "since" and "I" and "pregnant",
        "I.*(m|am|’m).* expecting. *baby", "I.*(m|am|’m).* going to be mom", "I.*(m|am|’m).* having a baby", 
        "I.*(ve|have|’ve).* been pregnant", "I.*(m|am|’m).* going to have a baby",
        "I.*(m|am|’m).* becoming.*(mom|mother).*"]
    df = []
    geoc="46.067139,11.119965,2000mi" #1 mile
    file_name = "recent_tweets/last_saved_tweet.json"
    #  check if any tweet has been collected and get the last tweet_id 
    if os.path.exists(file_name):
        with open (file_name) as f:
            d = json.load(f)
            since_id = d["last_tweet_id"]
    else:
        since_id = None
    ids = []
    for w in words:
        for tweet in api.search(q = w, lang="en",count = 200,geocode=geoc,since_id=since_id):
            date_str = tweet.created_at.strftime("%d-%m-%Y")
            d = dict(username=tweet.user.name,text=tweet.text,location=tweet.user.location,ID =tweet.id, time = date_str)
            df.append(d)
            print(f"{tweet.user.name}:{tweet.text}")
            save_last_id(tweet.id)
            ids.append(tweet.id)
  
    with open("recent_tweets/log-{}.json".format(get_file_number()),"w") as f:
        json.dump(df,f)


if __name__ == "__main__":
    main()