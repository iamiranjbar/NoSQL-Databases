db.tweets.aggregate([
    { $group : { _id : '$hashtags', count : {$sum : 1}}},
    { $match: { _id : {$ne:[]} } },
    { $sort : { count : -1 } },
    { $limit : 1 }
])
db.tweets.aggregate([
    { $group : { _id : '$hashtags', count : {$sum : 1}}},
    { $match: { _id : {$ne:[]} } },
    { $sort : { count : 1 } },
    { $limit : 1 }
])