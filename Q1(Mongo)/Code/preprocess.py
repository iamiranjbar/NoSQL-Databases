from pymongo import MongoClient


BAD_CHARS_MAPPING = {
    'ك': 'ک',
    'ي' : 'ی'
}


def replace_tweets_bad_chars_in_db(collection):
    for document in collection.find():
        for key, value in BAD_CHARS_MAPPING.items():
            document["content"] = document["content"].replace(key, value)
        result = collection.update_one(
            {"id" : document['id']},
            {"$set": document}
        )

def add_tweets():
    mongo_client = MongoClient('mongodb://localhost:27017')
    db = mongo_client.sahamyab
    collection = db["tweets"]
    replace_tweets_bad_chars_in_db(collection)


add_tweets()
