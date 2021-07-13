from flask import Flask
from flask import render_template
from flask import  redirect, url_for, request
import pymongo
import re
import random

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TweetsDB"] 
tweets_collection = db["all_tweets"] 
labeled_collection = db["labeled"]
#regx = re.compile(".*pregnant.", re.IGNORECASE)
#cursor1 = tweets_collection.find({"text": regx})
cursor2 = tweets_collection.find({})
#cursorIter1 = iter(cursor1)
cursorIter2 = iter(cursor2)
class LabeledTweet(dict):
    def __init__(self,id,label):
        self["_id"] = id
        self["label"] = label
        
app = Flask(__name__)
@app.route('/')
def root():
    if random.random() < 0.5 :
        tweet = next(cursorIter2)
    else:
        tweet = next(cursorIter2)
    t = labeled_collection.find_one({"_id":tweet["_id"]})
    # print("t",t,tweet["_id"],type(tweet["_id"]))
    while t is not None:
        '''
        if random.random() < 0.5 :
            tweet = next(cursorIter1)
        else:
            tweet = next(cursorIter2)
        '''
        tweet = next(cursorIter2)
        t = labeled_collection.find_one({"_id":tweet["_id"]})
    return render_template('index.html',tweet = tweet)
@app.route('/annotate',methods=["POST"])
def annotate():
    id_ = int(request.form.get("id"))
    label = request.form.get("is_related")
    item = LabeledTweet(id_,label)
    x = labeled_collection.insert_one(item)
    # print(request.form)
    return redirect("/")
