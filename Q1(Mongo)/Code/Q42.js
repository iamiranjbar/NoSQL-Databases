db.tweets.aggregate([
    {$group : { _id : '$hashtags', count : {$sum : 1}}},
    { $sort : { count : -1 } }
])