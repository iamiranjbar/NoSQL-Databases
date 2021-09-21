db.tweets.aggregate([
    {$group : { _id : '$senderUsername', count : {$sum : 1}}},
    { $facet: {
      "categorizedByActivity": [
        {
          $bucket: {
            groupBy: "$count",
            boundaries: [1, 2, 4],
            default: "Other",
            output: {
              "count": { $sum: 1 },
              "titles": { $push: "$_id" }
            }
          }
        }
      ]
    }}
])