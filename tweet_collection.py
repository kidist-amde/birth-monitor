
import pandas as pd
import tweepy 
import json

api_key_ = ''
api_secret_key = ''
Access_Token = ''
Access_Token_Secret = ''

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
auth = tw.OAuthHandler(api_key_, api_secret_key)
auth.set_access_token(Access_Token, Access_Token_Secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

words = ["having" ,"a" ,"baby"]
df = []
geoc="46.067139,11.119965,2000mi" #1 mile
for tweet in api.search(q = "%20".join(words), lang="en",count = 200,geocode=geoc):
    d = dict(username=tweet.user.name,text=tweet.text,location=tweet.user.location)
    df.append(d)
    print(f"{tweet.user.name}:{tweet.text}")

with open("log.json","w") as f:
    json.dump(df,f)

if __name__ == "__main__":
    main()