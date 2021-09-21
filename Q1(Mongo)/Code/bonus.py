from pymongo import MongoClient
from bson.code import Code


db = MongoClient('mongodb://localhost:27017').sahamyab

map = Code("function () {"
           "emit(this.senderUsername, this.hashtags.length)"
           "}")
reduce = Code("function (key, values) {"
              "  var total = 0;"
              "  for (var i = 0; i < values.length; i++) {"
              "    total += values[i];"
              "  }"
              "  return total/values.length;"
              "}")
result = db.tweets.map_reduce(map, reduce, "myresults")
for doc in result.find():
    print(doc)
