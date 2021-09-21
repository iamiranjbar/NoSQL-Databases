db.tweets.createIndex(
  { senderUserName: 1, } ,
  { name: "query for search on username" }
)