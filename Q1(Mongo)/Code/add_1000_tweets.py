import time
import requests
import json
from pymongo import MongoClient
from bson import ObjectId


def get_tweets():
    response = requests.get('https://www.sahamyab.com/guest/twiter/list?v=0.1', headers={'User-Agent': 'Chrome/61'})
    data = json.loads(response.text)
    tweets = data['items']
    return tweets


def insert_tweets_in_db(tweets, collection):
    for tweet in tweets:
        result = collection.update_one(
            {"id" : tweet['id']},
            {"$set": tweet},
            upsert=True
        )
        total_docs = collection.count_documents({})
        if total_docs == 1000:
            return


def add_tweets():
    mongo_client = MongoClient('mongodb://localhost:27017')
    db = mongo_client.sahamyab
    collection = db["tweets"]
    total_docs = collection.count_documents({})
    while True:
        tweets = get_tweets()
        insert_tweets_in_db(tweets, collection)
        total_docs = collection.count_documents({})
        print("New tweets has been inserted!")
        print ("{} has {} total documents.".format(collection.name, total_docs))
        if total_docs == 1000:
            break
        time.sleep(1 * 60)


add_tweets()
