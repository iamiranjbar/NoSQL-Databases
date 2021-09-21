db.tweets.find({type: "retwit"}).count()
db.tweets.find({type: "retwit"}).forEach(
    function(doc) {
      db.retweets.insert(doc)  
    })
db.retweets.find().count()
db.tweets.remove({type: "retwit"})
db.tweets.find({type: "retwit"}).count()