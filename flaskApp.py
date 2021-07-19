from flask import Flask
from flask import render_template
from flask import  redirect, url_for, request
import pymongo
import re
import random
import tqdm
visited = set()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bdt_db"]
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
results = []
num_tweets = 0
for pattern_index in tqdm.trange(len(words)):
    regx = re.compile(words[pattern_index] , re.IGNORECASE)
    cursor1 = tweets_collection.find({"text": regx},batch_size =int(10000/len(words)) )
    num_pattern_tweets = 0 
    for item in tqdm.tqdm(cursor1,total = 10//len(words)):
        results.append(item)
        num_tweets +=1
        num_pattern_tweets +=1
        if num_pattern_tweets > 10//len(words):
            break 
    del cursor1
    if num_tweets > 10: 
        break
cursor2 = tweets_collection.find({})
for item in cursor2:
    results.append(item)
    num_tweets +=1
    if num_tweets > 20:
        break
del cursor2
current_index = 0
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
    global current_index
    tweet = results[current_index]
    current_index +=1
    t = labeled_collection.find_one({"_id":tweet["_id"]})
    while t is not None or tweet["text"] in visited:
        tweet = results[current_index]
        current_index +=1
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
