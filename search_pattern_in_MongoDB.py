
import re 
import pymongo
def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
    mydb = myclient["bdt_db"] 
    regx = re.compile("I.*(m|am|'m).*(weeks|months).*pregnant.", re.IGNORECASE)
    x= mydb.tweets.find_one({"text": regx})
    print(x)


if __name__ == "__main__":
    main()