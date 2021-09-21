var before = new Date()
db.getCollection('tweets').find({ $or: [
                                        { hashtags:
                                           "خودرو"
                                        }, { hashtags:
                                            "شستا"
                                        }, { hashtags:
                                            "فولاد"
                                        }   
]}).forEach(
            function(doc) {
                db.tweets.updateOne({
                 id: doc["id"]
               }, {
                    $set :{ gov:  true}
               }); 
            }
)
var after = new Date()
var execution_mills = after - before
print(execution_mills)