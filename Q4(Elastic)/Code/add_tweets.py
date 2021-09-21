import requests
import re
import time
from elasticsearch import Elasticsearch


def add_tweets():
    url = 'https://www.sahamyab.com/guest/twiter/list?v=0.1'
    elastic_search = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    total = 1000
    seen_ids = set()

    while len(seen_ids) < total:
        response = requests.get(url=url, headers={'User-Agent': 'Chrome/61'})
        if response.status_code != 200:
            print("Error code: {}".format(response.status_code))
            continue
        data = response.json()["items"]
        for tweet in data:
            if tweet["id"] not in seen_ids:
                try:
                    tweet["hashtags"] = re.findall(r"#(\w+)", tweet["content"])
                    elastic_search.index(index="twitter", doc_type="twitter", body=tweet)
                    seen_ids.add(tweet["id"])
                    print("Tweet {} has been fetched. Fetched: {} tweets".format(tweet["id"], len(seen_ids)))
                except Exception as e:
                    print(e)
        time.sleep(1)


add_tweets()
