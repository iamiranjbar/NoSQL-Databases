var before = new Date()
db.tweets.aggregate([
  {
    $addFields: {
      returnObject: {
        $regexFindAll: { input: "$sendTimePersian", regex: 
            /\s(\d{2})/
            }
      }
    }
  },
  { $set: { tweetHour: "$returnObject.match"} }
]).forEach(
    function(doc) {
        if(9 <= doc.tweetHour && doc.tweetHour <= 10){
            print(doc.senderName)
            print(doc.senderProfileImage)
            print('______________________')
        }
    }
)
var after = new Date()
execution_mills = after - before
print(execution_mills)