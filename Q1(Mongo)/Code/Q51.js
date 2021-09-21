db.tweets.createIndex(
  { mediaContentType: 1, parentId: 1, senderName: 1} ,
  { name: "query for media content type" }
)