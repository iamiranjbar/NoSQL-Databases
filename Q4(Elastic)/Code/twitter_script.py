GET /twitter/_search
GET /twitter/_search
{
  "query": {
    "query_string": {
      "query": "کاما",
      "fields": ["hashtags"]
    }
  }
}
GET /twitter/_search
{
  "query": {
    "query_string": {
      "query": "شاخص",
      "fields": ["content"]
    }
  }
}
GET /twitter/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "content": "پالایش"
          }
        },
        {
          "match": {
            "content": "شپنا"
          }
        }
      ]
    }
  }
}
