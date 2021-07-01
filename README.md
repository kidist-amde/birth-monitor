
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