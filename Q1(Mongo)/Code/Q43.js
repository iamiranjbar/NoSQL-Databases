db.tweets_copy.aggregate(
   { $match: { parentId: {$ne:null}} },
   { $unset: "type" }
)