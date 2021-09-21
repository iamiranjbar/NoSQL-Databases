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
                "hashtags": "$hashtags",
                "date": "$returnObject.match"
                }, count : {$sum : 1}}
    },
    { $match: { "_id.date" : {
        $gte:"1400/02/01",
        $lt: "1400/04/01"
    } } },
    { $match: { "_id.hashtags" : {$ne:[]} } },
    { "$sort": { "count": -1 } },
    { "$group": {
        "_id": "$_id.date",
        "results": {
            "$push": {
                "name": "$_id.hashtags", 
                "count": "$count",
            }
        }
    }},
    { "$sort": { "_id.0": 1}},
    { "$project": {
        "results": { "$slice": [ "$results", 10 ] }
    }}
])