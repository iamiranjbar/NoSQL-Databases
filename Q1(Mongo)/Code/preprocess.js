var before = new Date()
db.tweets.aggregate([
  {
    $addFields: {
      returnObject: {
        $regexFindAll: { input: "$content", regex: 
            /#([ا-ی]+)/
            }
      }
    }
  }
]).forEach(
   function(doc) {
       var result = doc["returnObject"]
       var hashtags = []
       for (found in result) {
           var hashtag = result[found].captures[0]
           hashtags.push(hashtag)
       }
       if (hashtags) {
            db.tweets.updateOne({
                 id: doc["id"]
               }, {
                    $set :{ hashtags:  hashtags}
               }); 
           }
   }
)
var after = new Date()
execution_mills = after - before
print(execution_mills)