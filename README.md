
# Birth-monitor

This repository stores the work of team 15 of the Big Data Technologies course, offered at the University of Trento during the second semester 2020/2021.

## Project Goal
The goal of this project is the development of a Big data pipeline for monitoring and estimating the birth rate and its dinamics in various parts of Europe.
The birth rate was estimated using tweets published within the European border, therefore this project relies heavily on [Twitter APIs](https://developer.twitter.com/en/docs/twitter-api) and [Web Scraping](https://careerfoundry.com/en/blog/data-analytics/web-scraping-guide) methods.

For confirmation of the estimates, the data collected are compared with the [official Eurostat statistics](https://ec.europa.eu/eurostat/databrowser/product/view/tps00204?lang=en).

## Project Structure
- `README.md`: file containing all the relevant information to run the project.
- `requirements`: file containing al the necessary libraries to install.
- `get_old_tweets.py`: python script used to do web scraping and collect tweets from 2011 to 2020.
- `tweet_collection.py`: script that, using tweepy, collects tweets up to two weeks old.
- `insert_to_MDB.py`, `upload_old_tweets_mongodb_compass.py`, `upload_recent_tweets_MongoDB.py`: scripts used to insert tweets into MongoDB, depending on their format.
- `search_pattern_in_MongoDB.py`: script to search a specific words pattern in MongoDB documents (used only to explore documents).
- `flaskApp.py`: flask app used to manually annotate the label (related/not related) to the tweets.
- `binary_classifier_for_merged.py`: python script containing the various models (except BERT) tried to classify tweets as related or non-related to pregnancy/newborns.

## Usage
This project requires Python and HTML usage.
Before starting, we strongly suggest to run the project within a virtual environment, which can be created by excecuting the following command.
```
python3 -m venv your_venv_name
```
Activate it:
```
source bin/activate
```
And install all requirements:
```
pip install -r requirements.txt
```


If you are using conda, use the following steps instead. Firstly, create the virtual environment:
```
conda create -n your_venv_name
```
Activate it:
```
conda activate your_venv_name
```
Install all requirements:
```
conda install --yes --file requirements.txt
```

### Installing Dependencies 

* install dependencies using the following  command:

```bash
pip install -r requirments.txt
```
* install the following package to excute tweet_collection script:
``` bash
pip install tweepy
```

In order to run the tweet_collection script, it is necessary to create the `config.py` file in the current working directory and provide the API tokens and access keys as follows:

```python
api_key_ = ''
api_secret_key = ''
Access_Token = ''
Access_Token_Secret = ''
```
### How to run the Docker image
Step 1: Load the tar file 
```bash
 sudo docker load -i tweets-docker-image.tar
```
Step 2 : Run docker image 
The db folder which contains the labeled data is shared and the string `/db-folder-path/` must be replaced with the full path of the db folder
```bash 
sudo docker run -v /db-folder-path/:/data/db -d -p 5000:5000 tweemon-image:v4
```
Step 3: list the running docker container 
```bash
sudo docker ps -a
```
Step 4 : Attach the docker container standard I/O
Copy id of the running container and replace `docker-container-id`
```bash
sudo docker exec -it docker-container-id /bin/bash
```
Step 5: Change the directory to bdt-project
```bash
cd bdt-project
```
Step 6: Start Flask web application to perform the following task
* Data collection
* Data annotation
* Training 
* Visuallization

```bash
./run.sh
```

## Run the Application
To run the web application, one must enter the project folder and start the flask application in the local server with: 

```
flask run
```
