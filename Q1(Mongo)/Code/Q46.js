db.tweets.aggregate([
    {
        $addFields: {
          returnObject: {
            $regexFindAll: { input: "$sendTimePersian", regex: 
                /(.{10})\s/
                }
          }
        }
    },
    { $group : { "_id": {
                "user": "$senderUsername",
                "date": "$returnObject.match"
                }, count : {$sum : 1}}
    },
    { "$sort": { "count": -1 } },
    { "$group": {
        "_id": "$_id.date",
        "results": {
            "$push": {
                "user": "$_id.user", 
                "count": "$count",
            }
        }
    }},
    { "$sort": { "_id.0": 1}},
    { "$project": {
        "results": { "$slice": [ "$results", 1 ] }
    }}
])