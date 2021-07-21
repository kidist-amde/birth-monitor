import json
from pymongo import MongoClient
import pandas as pd
import tqdm
def main():
   
    myclient = MongoClient("mongodb://localhost:27017/")
    # Database
    db = myclient["bdt_db"]
    
    eurostat_collection = db["eurostat_data"] 
    df = pd.read_csv("demo_fmonth/demo_fmonth_1_Data.csv")   
    # change the string type to float and replace Null value with 0
    df.Value = df.Value.apply(lambda x: 0 if x == ":" else float(x.replace(",",""))) 
    for index,row in tqdm.tqdm(df.iterrows(),total = len(df)):
        data = {key:row[key] for key in row.keys()}
        eurostat_collection.insert_one(data)
    
    
    
    
if __name__ == '__main__':
    main()
    