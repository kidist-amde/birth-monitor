import json
import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
import sklearn
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from time import process_time
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix, classification_report,accuracy_score
from sklearn.base import TransformerMixin
import pathlib
import os


'''
Binary classifier of tweets (0 - not related, 1 - related).
MAIN REFERENCE: https://towardsdatascience.com/binary-classification-of-disaster-tweets-73efc6744712
'''


if __name__ == '__main__':
    # Connecting
    CONNECTION_STRING = "mongodb://localhost:27017/"
    myclient = MongoClient(CONNECTION_STRING)
    # Database
    db = myclient["TweetsDB"]
    labeled_collection = db["labeled"] #labeled_tweets
    all_tweets = db["all_tweets"] #Tweets_June_2021
    all_files_labeled = labeled_collection.find({})
    all_files = all_tweets.find({})
    all_files = list(all_files)
    all_files_labeled = list(all_files_labeled)

    # labeled tweets:
    f_list=[] # false label
    t_list=[] # true label
    for doc in all_files_labeled:
        if doc['label']=='false':
            doc['label'] = 0
            f_list.append(doc)
        else:
            doc['label'] = 1
            t_list.append(doc)
    print(len(t_list), len(f_list)) # 240 true, 498 false: unbalanced classes --> try StratifiedShuffleSplit


    # clean text from digits, non-ASCII characters, punctuations, https, and changed all texts to lowercase --> reduce noises in text
    def clean(text):
        text = re.sub(r"\n", "", text)
        text = text.lower()
        text = re.sub(r"\d", "", text)  # Remove digits
        text = re.sub(r'[^\x00-\x7f]', r' ', text)  # remove non-ascii
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = re.sub(r'http\S+|www.\S+', '', text)  # Remove http
        return text
    l=[]
    for doc in all_files:
        doc['cleaned_text'] = clean(doc['text'])
        #print(doc['cleaned_text'])
        for lab_doc in all_files_labeled:
            if int(doc['ID']) == lab_doc['_id']:
                value = doc['cleaned_text']
                lab_doc['cleaned_text'] = value
                #print(lab_doc)
                l.append(lab_doc)

    all_files_labeled = l


    X=[]
    Y=[]
    for a in all_files_labeled:
        X.append(a['cleaned_text'])
        Y.append(a['label'])



    # use StratifiedShuffleSplit to split into train and test set since classes are unbalanced
    # --> stratified sampling, where the dataset is divided into homogeneous subgroups (strata) and the right number
    # of instances is sampled from each stratum to guarantee that the test set is representative of the overall population.
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    X = np.array(X)
    Y = np.array(Y)
    for train_index, test_index in sss.split(X, Y):
        x_train, x_test = X[train_index], X[test_index]
        y_train, y_test = Y[train_index], Y[test_index]

    # convert tweets to a matrix of token counts to extract numerical features from text
    # 1) removed step words by selecting step_words='english' in CountVectorizer function
    # 2) normalize the matrix to decrease the effect of words that occur several times in the text
    # put these two steps together using Pipeline function
    class DenseTransformer(TransformerMixin):
        def fit(self, X, y=None, **fit_params):
            return self
        def transform(self, X, y=None, **fit_params):
            return X.todense()

    tweets_pipeline = Pipeline([('CVec', CountVectorizer(stop_words='english')),
                                ('to_dense', DenseTransformer()),
                                ('Tfidf', TfidfTransformer())])

    X_train_tranformed = tweets_pipeline.fit_transform(x_train)
    X_test_tranformed = tweets_pipeline.transform(x_test)
    # no need to do the same for the target since it is binary

    classifiers = {
        "Logistic Regression": LogisticRegression(class_weight='balanced'),
        "Classification Tree": DecisionTreeClassifier(class_weight='balanced'),
        "KNN": KNeighborsClassifier(),
        "Support Vector Classifier": SVC(class_weight='balanced'),
        "Naive Bayes Classifier": MultinomialNB()
    }



    # compare methods based on AUC
    n_classifiers = len(classifiers.keys())
    def classify(X_train_tranformed, y_train, X_test_tranformed, y_test, verbose=True):
        df_results = pd.DataFrame(data=np.zeros(shape=(n_classifiers, 3)),
                                  columns=['Classifier', 'AUC', 'Training time'])
        count = 0
        for key, classifier in classifiers.items():
            t_start = process_time()

            classifier.fit(X_train_tranformed, y_train)
            t_stop = process_time()
            t_elapsed = t_stop - t_start
            y_predicted = classifier.predict(X_test_tranformed)

            df_results.loc[count, 'Classifier'] = key
            df_results.loc[count, 'Area Under Curve'] = roc_auc_score(y_test, y_predicted)
            df_results.loc[count, 'Training time'] = t_elapsed
            if verbose:
                print("trained {c} in {f:.2f} s".format(c=key, f=t_elapsed))
            count += 1

        return df_results


    df_results = classify(X_train_tranformed, y_train, X_test_tranformed, y_test)
    print(df_results.sort_values(by='Area Under Curve', ascending=False))

    # choose method that maximises AUC
    # possible improvements: optimize parameters for faster performances

    # on Tweets_June_2021 (recent tweets) it gives the following results:
    # SVM AUC = 0.958
    # NB AUC = 0.937
    # TREE AUC = 0.922
    # LOGISTIC REG. AUC = 0.833
    # KNN AUC = 0.786

    # use the best classifier (SVM) to label all unlabeled tweets
    def labeled_tweets(all_files, classifier=classifiers["Support Vector Classifier"], verbose=True):
        l = []

        X = []
        for d in all_files:
            X.append(d['cleaned_text'])
        X = np.array(X)

        # classifier = SVC(class_weight='balanced')
        X = tweets_pipeline.transform(X)
        y_pred = classifier.predict(X)

        y_pred = list(y_pred)

        for tweet in range(len(all_files)):
            diz = {}
            diz['_id'] = int(all_files[tweet]['ID'])
            if y_pred[tweet] == 0:
                diz['label'] = 'false'
            else:
                diz['label'] = 'true'
            l.append(diz)

        return l


    my_json = labeled_tweets(all_files)

    # get path to save the file
    my_path = pathlib.Path().resolve()
    file = os.path.join(my_path, 'classified_tweets\classified_tweets.json')

    # save json file with labeled tweets
    with open(file, 'w') as outfile:
        json.dump(my_json, outfile)
    

