
# Birth-monitor

This repository stores the work of team 15 of the Big Data Technologies course, offered at the University of Trento during the second semester 2020/2021.

## Project Goal
The goal of this project is to implement a Big data pipeline for monitoring and estimating the birth rate and its dynamics in various parts of Europe.
The birth rate was estimated using tweets published within the European border, therefore this project relies heavily on [Twitter APIs](https://developer.twitter.com/en/docs/twitter-api) and [Web Scraping](https://pypi.org/project/bsi-sentiment/) method.

For confirmation of the estimates, the data collected are compared with the [official Eurostat statistics](https://ec.europa.eu/eurostat/databrowser/product/view/tps00204?lang=en).

## Project Structure
- `README.md`: file containing all the relevant information to run the project.
- `requirements`: file containing all the necessary libraries to install.
- `get_old_tweets.py`: python script used to do web scraping and collect old tweets from 2011 to 2020.
- `tweet_collection.py`: script that, using tweepy, collects recent tweets up to two weeks old.
- `insert_to_MDB.py` `insert_eurostatdata_toMDB `filter_related_tweets.py`: scripts used to insert tweets and Eurostat data,into MongoDB.
- `flaskApp.py`: a python script for the entry point of the web page 
- `binary_classifier_for_merged.py`: python script containing the various models (except BERT) to classify tweets as related or non-related to pregnancy/newborns.
- The Notebook folder contains the notebooks which implement data visualization of both  datasets (tweets and eurostat data) and the state of the art classfier model BERT and  kernel SVM. We used google colab to use GPU and train the classfier mode. We have provided publicly avalible links on the web app. 
- Templet folder includes html files of the web page
- Static folder includes the java script,css and Images of the web page.


### Installing Dependencies 

* install dependencies using the following  command:

```bash
pip install -r requirments.txt
```


In order to run the tweet_collection script, it is necessary to create the `config.py` file in the current working directory and provide the API tokens and access keys as follows:

```python
api_key_ = ''
api_secret_key = ''
Access_Token = ''
Access_Token_Secret = ''
```
### How to run the Docker image
There are two files that are shared to run the docker image. The first file is db.zip and the second file is tweets-docker-image.tar. The db.zip file contains tweets dataset. If this files is available the tweet collection step can be skipped. 

The following steps show how to load and use the docker image.

Step 1: Load the tar file 
```bash
 sudo docker load -i tweets-docker-image.tar
```
Step 2: Extract the db folder
```bash 
unzip db.zip -d /db-folder-path/ # replace /db-folder-path/ to your custom path which should be set on the next step
```

Step 3 : Run docker image 
The db folder which contains the labeled data is shared and the string `/db-folder-path/` must be replaced with the full path of the db folder
```bash 
sudo docker run -v /db-folder-path/:/data/db -d -p 5000:5000 tweemon-image:v4
```
Step 4: list the running docker containers
```bash
sudo docker ps -a
```
Step 5 : Attach the docker container standard I/O
Copy id of the running container and replace `docker-container-id` with the container id
```bash
sudo docker exec -it docker-container-id /bin/bash
```
Step 6: Change the directory to bdt-project
The following command should be run inside docker container, after attaching terinal to the docker container using step 5
```bash
cd bdt-project
```

Step 7: Installing the dependencies
```bash 
pip3 install -r requirements.txt
```
Step 8: Start Flask web application to perform the following task
* Data collection
* Data annotation
* Training 
* Visuallization

```bash
./run.sh
```

## Run the Application


Addition to the docker image, the web app can be run from local computer using the following command. To run the following command the current working directory of the terminal/cmd should be inside the project directory.

```
export FLASK_APP=flaskApp.py
flask run
```


## The web app

The web app which can be run from both the docker and from local computer has many functioalities implemented. These functiolities are

* Data collection
    * Downloading old tweets using bsi-sentiment python package. Downloading the old tweets takes few days of continous execution. Thus we reduced the number of tweets to be downloaded to 10 for experimental purpose. 
    * Downloading recent tweets using tweepy package
    * Downloading Eurstat Dataset
    * Manual annotation of tweets into two categories(Related to birth or not related to birth)
* Live birth related 
    * Training annotation model. Information required to train the annotation model are available in this section.
    * Automatic tweet annotation as "related tweet" or "not related tweet"
    * Displaying sample tweets annotated by the model
    * Traning birth estimation model
* Visualization
    * Europe birth number visualiztion for each months between 2011 and 2020
    * Number of tweets related to birth visualiztion for each months between 2011 and 2020
    * Map showing the number of births in Europe for over 10 yeras.