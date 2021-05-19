
from bsi_sentiment.twitter import search_tweets_sn
import os 
import time
def main():
    queries =["having a baby","delivering a baby","welcome baby","newborn",
              "new born","first baby","delivering first baby","baby coming soon",
              "have been pregnant","going to be mom","becoming mom","becoming dad"
              ,"becoming mother","becoming father"]  

    
    european_countries = ['Albania', 'Andorra', 'Austria', 'Belarus', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 
                      'Czech Republic', 'Denmark', 'Finland', 'Estonia', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 
                      'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'North Macedonia', 
                      'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 
                      'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 
                      'Ukraine', 'United Kingdom','UK','England', 'Scotland', 'Wales', 'Northern Ireland', 'Vatican City' ]
    
    if not os.path.exists("old_tweets"):
        os.mkdir("old_tweets")
    for country in european_countries:
        for i in range(len(queries)):
            try:
                tweets = search_tweets_sn(
                    q = queries[i],
                    since="2011-01-01",
                    until="2020-12-31",
                    near=country,
                    radius="1000km",
                    lang="en",
                    max_tweets=100000
            )
            except:
                time.sleep(120)

        
            try:
                
                tweets.to_csv(f"./old_tweets/{country}-{i}.csv")
            except:
                print("No tweet found for '{}' query ".format(queries[i]))
            
if __name__ == "__main__":
    main()