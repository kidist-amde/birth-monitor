from flask import Flask
from flask import render_template
from flask import  redirect, url_for, request
from get_old_tweets import get_tweets
from tweet_collection import get_recent_tweets
from birth_prediction import build_dataset,train_estimator,compute_loss,make_prediction
import pymongo
import re
import random
import tqdm
import gdown
dataset= build_dataset()

color_func = lambda : [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

visited = set()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bdt_db"]
birth_collection = db["birth_tweets"]
tweets_collection = db["tweets"]
labeled_collection = db["labeled_tweets"]
words=["I.*(m|am|’m).*(weeks|months).*pregnant.", "my" and "pregnancy", "pregnant", "baby" and "our family", 
        "baby coming soon", "I.*(m|am|’m).* been.*(weeks|months).*" and "since" and "I" and "pregnant",
        "I.*(m|am|’m).* expecting. *baby", "I.*(m|am|’m).* going to be mom", "I.*(m|am|’m).* having a baby", 
        "I.*(ve|have|’ve).* been pregnant", "I.*(m|am|’m).* going to have a baby",
        "I.*(m|am|’m).* becoming.*(mom|mother).*"] + ["having a baby","delivering a baby","welcome baby","newborn",
              "new born","first baby","delivering first baby","baby coming soon",
              "have been pregnant","going to be mom","becoming mom","becoming dad"
              ,"becoming mother","becoming father"] 
pattern_index = 0
regx = re.compile(words[pattern_index] , re.IGNORECASE)

cursor = tweets_collection.find({"text": regx}) 
cursor_iter = iter(cursor)
class LabeledTweet(dict):
    def __init__(self,id,label):
        self["_id"] = id
        self["label"] = label
app = Flask(__name__)
@app.route('/')
def root():
    return render_template("index.html")
@app.route('/annotate_data')
def annotate_data():
    global cursor_iter,cursor,pattern_index,regx
    try:
        tweet = next(cursor_iter)
    except StopIteration:
        pattern_index  +=1
        regx = re.compile(words[pattern_index] , re.IGNORECASE)
        cursor = tweets_collection.find({"text": regx}) 
        cursor_iter = iter(cursor)
        tweet = next(cursor_iter)

    t = labeled_collection.find_one({"_id":tweet["_id"]})
    while t is not None or tweet["text"] in visited:
        try:
            tweet = next(cursor_iter)
        except StopIteration:
            pattern_index  +=1
            regx = re.compile(words[pattern_index] , re.IGNORECASE)
            cursor = tweets_collection.find({"text": regx}) 
            cursor_iter = iter(cursor)
            tweet = next(cursor_iter)
        t = labeled_collection.find_one({"_id":tweet["_id"]})
    visited.add(tweet["text"])
    return render_template('data_annotation.html',tweet = tweet)
@app.route('/annotate',methods=["POST"])
def annotate():
    id_ = int(request.form.get("id"))
    label = request.form.get("is_related")
    item = LabeledTweet(id_,label)
    x = labeled_collection.insert_one(item)
    # print(request.form)
    return redirect("/annotate_data")
@app.route("/data_collection")
def data_collection():
    return render_template("data_collection.html")

@app.route("/downloadOldTweets")
def downloadOldTweets():
    # time.sleep(5)
    d = get_tweets(max_tweets=10,num_tweets=10)
    return {"msg":"Downloaded {} tweets".format(d)}

@app.route("/downloadRecentTweets")
def downloadRecentTweets():
    # time.sleep(5)
    rt = get_recent_tweets()
    return {"msg":"Downloaded {} tweets".format(rt)}

@app.route("/downloadEuroStatData")
def downloadEuroStatData():
    url = 'https://drive.google.com/uc?id=1A_h9ooiTkDSZDzPO4_5ZoYSD8ukQQoWq'
    output = './eurostat_data.csv'
    gdown.download(url, output, quiet=False)    
    return {"msg":"Downloaded Euro stat dataset"}

@app.route("/live_birth")
def live_birth():
    return render_template("live_birth.html")

@app.route("/visualization")
def visualization():
    return render_template("visualization.html")
@app.route("/sample_tweets")
def sample_tweets():
    """Fetch sample tweets from the database.
    """
    regx = re.compile(".* baby coming soon .*|.* month pregnant.*" , re.IGNORECASE)
    iter1 = iter(birth_collection.find({"text":regx}))
    iter2 = iter(tweets_collection.find({}))
    tweets = []
    for i in range(5):
        bt =next(iter1)
        bt["label"] = "positive"
        tweets.append(bt)
    count = 0
    while count <5:
        tweet = next(iter2)
        bt = birth_collection.find_one({"_id":tweet["_id"]})
        if bt is None:
            tweet["label"] = "negative"
            tweets.append(tweet)
            count +=1
    random.shuffle(tweets)
    return dict(tweets=tweets)
@app.route("/train_estimator")          
def train_estimator_route():
    model = train_estimator(dataset["x_train"],dataset["y_train"])  
    train_loss = compute_loss(model,dataset["x_train"],dataset["y_train"])
    test_loss = compute_loss(model,dataset["x_test"],dataset["y_test"])
    return {
            "msg":"The model train sucessfull",
            "train_loss": train_loss,
            "test_loss": test_loss,      

        }
@app.route("/get_tweet_per_month_vis")
def get_tweet_per_month_vis():
    months = dataset["ordered_months"]
    tweets = dataset["num_tweets_perMonth"]

    colors = [color_func() for i in range(len(tweets))]
    
    colors = ["rgb({},{},{})".format(*c) for c in colors]
    return dict(months=months, tweets=tweets, colors=colors)
@app.route("/get_birth_per_month_vis")
def get_birth_per_month_vis():
    months = dataset["ordered_months"]
    births = dataset["monthly_birth_rate"]
    colors = [color_func() for i in range(len(months))]
    colors = ["rgb({},{},{})".format(*c) for c in colors]
    return dict(months=months, births=births, colors=colors)

@app.route("/worldcloud_vis")
def worldcloud_vis():
    images = [
        "/static/images/wc.png"
    ]
    return dict(images = images)
      
       
    
        
    
        
    
