from flask import Flask
from flask import render_template
from flask import  redirect, url_for, request
import pymongo
import re
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bdt_db"]
tweets_collection = db["tweets"]
labeled_collection = db["labeled_tweets"]
regx = re.compile("I.*(m|am|'m).*(weeks|months).*pregnant.", re.IGNORECASE)
cursor = tweets_collection.find({"text": regx})
cursorIter = iter(cursor)
class LabeledTweet(dict):
    def __init__(self,id,label):
        self["id"] = id
        self["label"] = label
        

app = Flask(__name__)
@app.route('/')
def root():
    tweet = next(cursorIter)
    return render_template('index.html',tweet = tweet)
@app.route('/annotate',methods=["POST"])
def annotate():
    id_ = request.form.get("id")
    label = request.form.get("is_related")
    item = LabeledTweet(id_,label)
    x = labeled_collection.insert_one(item)
    # print(request.form)
    return redirect("/")
