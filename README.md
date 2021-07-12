
# Birth-monitor-team 15

Big data system for monitoring and estimating, based on tweets, the birth rate in various parts of Europe and its dynamics. Using Twitter APIs + data from Eurostat 

### Installing Dependencies 

* install the following package to excute get_old_tweets script

```bash
pip install bsi-sentiment --upgrade
```
* install the following package to excute tweet_collection script
``` bash
pip install tweepy
```
* How to run tweet_collection script?

In order to run this script you have to create config.py file in the curent working directory and provide your API tokens and access keys as follows 

```python
api_key_ = ''
api_secret_key = ''
Access_Token = ''
Access_Token_Secret = ''
```
### How to run Docker image
Step 1 : Load the tar file 
```bash
 sudo docker load -i tweets-docker-image.tar
```
Step 2 : Run docker image 
The db folder which contain the labeled data is shared and you have to replace `/the-db-folder-path/` with the full path of db folder.
```bash 
sudo docker run -v /the-db-folder-path/:/data/db -d -p 5000:5000 tweemon-image:v8
```
Step 3: list the running docker container 
```bash
sudo docker ps 
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
Step 6: Start Flask application and start annotating the tweets
```bash
./run.sh
```