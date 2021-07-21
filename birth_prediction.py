import pandas as pd
import numpy as np
import json
import re
from tqdm import tqdm
import pymongo
from collections import Counter
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import defaultdict
import nltk
nltk.download("stopwords")

from nltk.corpus import stopwords
# print(stopwords.words('english'))
# conncet to DB
myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
mydb = myclient["bdt_db"] 
euro_collection=mydb["eurostat_data"]
mycol = mydb["birth_tweets"] 
month_names  = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
 'September', 'October', 'November', 'December']
print("Loading all tweets from MongoDB")
all_tweets = [t for t in mycol.find({})]

def get_word_counts():
    # read all the tweets text of the database
    tweets = [t["text"] for t in all_tweets]
    # put all twets on one string
    raw_text = "\n".join(tweets)
    # word counter and lowecasing 
    word_counter = Counter() 
    for tweet in tqdm(tweets):
        tweet = re.sub(r"http\S+",'', tweet, flags=re.MULTILINE)
        tweet = re.sub(r"[^A-Za-z0-9'\ ]+", '', tweet) 
        word_counter.update(tweet.lower().split())
    # remove stopwords
    for word in stopwords.words("english"):
        del word_counter[word]
    return word_counter

def get_word_cloud(word_counter):
    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=10, contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate_from_frequencies(word_counter)
    return wordcloud
def visualize_word_cloud(wordcloud):
    # Visualize the word cloud
    plt.figure(1,figsize=(11, 11))
    plt.imshow(wordcloud.to_image())
    plt.axis('off')
    plt.title('Figure 1: birth words cloud',color="red" )
    
    plt.show()
def get_most_frequentKeywords(word_counter):
    frequent_words = [item[0] for item in word_counter.most_common(256)]
    word2index = {frequent_words[i]:i for i in range(len(frequent_words))}
    return frequent_words,word2index

def get_months_keywords(word2index):
    # get array of keywords counts for each months
    months_keywords_count = defaultdict(lambda: np.zeros(len(word2index)))
    num_tweets_perMonth = defaultdict(int)
    for tweet in tqdm(all_tweets):
        time = tweet["time"]
        year,month,date = time.split("-")
        month = int(month)-1
        month_name = month_names[month]
        month = "{}_{}".format(year,month_name)
        num_tweets_perMonth[month] += 1
        for word , index in word2index.items():
            count = tweet["text"].count(word)
            months_keywords_count[month][index] += count
    return months_keywords_count,num_tweets_perMonth   

def get_monthly_birthrate(euro_collection):
    # total birth of each month of country 
    monthly_birth_rate = defaultdict(int)
    for data in euro_collection.find({}):
    #     if row["GEO"].lower() == "italy":
            month = "{}_{}".format(data["TIME"],data["MONTH"])
            monthly_birth_rate[month] += data['Value']
    return monthly_birth_rate
def get_ordered_months(num_tweets_perMonth,monthly_birth_rate):
    # put the months of each year in order 
    ordered_months = []
    for year in range(2011,2022):
        for m in range(len(month_names)):
            month_name = month_names[m]
            month = "{}_{}".format(year,month_name)
            # select only months exist in both data
            if month in num_tweets_perMonth and month in monthly_birth_rate:
                ordered_months.append(month) 
    return ordered_months
def plot_livebirth(num_tweets_perMonth,ordered_months):
    # show the number of tweets each month 
    x = ordered_months
    height = [num_tweets_perMonth[month] for month in x]
    plt.figure(figsize=(14,6))
    plt.xlabel("month index (starting from January 2011)")
    plt.ylabel("number of tweets per month")
    plt.bar(x = list(range( len(x))),height = height)
    plt.show()

def plot_birthtweets_overtime(monthly_birth_rate,ordered_months):
    # show the number of tweets each month 
    x = ordered_months
    height = [monthly_birth_rate[month] for month in x]
    plt.figure(figsize=(14,6))
    plt.xlabel("month index (starting from January 2011)")
    plt.ylabel("Eurostat number of birth rate per month")
    plt.bar(x = list(range( len(x))),height = height)
    plt.show()

def build_dataset():
    print("Getting word counts")
    word_counter = get_word_counts()
    frequent_words,word2index = get_most_frequentKeywords(word_counter)
    print("Getting keyword counts")
    months_keywords_count,num_tweets_perMonth = get_months_keywords(word2index)
    monthly_birth_rate =get_monthly_birthrate(euro_collection)
    ordered_months = get_ordered_months(num_tweets_perMonth,monthly_birth_rate)
    # keyword counts of tweets in DB = ordered by month
    ordered_monthly_keywordsCounts = np.stack([months_keywords_count[m]/num_tweets_perMonth[m] for m in ordered_months])
    # birth rate of each month eurostatdata = ordered by mont 
    ordered_monthly_birthRates = np.stack([monthly_birth_rate[m] for m in ordered_months])
    x_train,x_test,y_train,y_test = train_test_split(ordered_monthly_keywordsCounts,ordered_monthly_birthRates)
    return dict(x_train = x_train,x_test = x_test,
                y_train = y_train,y_test= y_test,
                num_tweets_perMonth = num_tweets_perMonth,
                monthly_birth_rate = monthly_birth_rate,
                ordered_months = ordered_months)
def train_estimator(x_train,y_train):
    # np.random.seed(143)
    # serch paramter 
    parameters = {
        "kernel": ["rbf","linear"],
        "C": [1,10,10,100,1000],
        "gamma": [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1,1,10,100]
        }
    grid = GridSearchCV(SVR(), parameters,scoring="neg_mean_absolute_error", cv=5, verbose=2)
    grid.fit(x_train, y_train)
    best_params = grid.best_params_
    # kernal SVM 
    model = SVR(C=best_params["C"], kernel=best_params["kernel"] ,gamma = best_params["gamma"])
    model.fit(x_train, y_train)
    return model
def make_prediction(model,x):
    pred = model.predict(x)
    return pred
def compute_loss(model,x,y):
    pred= make_prediction(model,x)
    loss = mean_absolute_error(pred,y)
    return loss






