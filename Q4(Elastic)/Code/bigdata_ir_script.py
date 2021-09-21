PUT movies/_doc/2
{
    "title": "Lawrence of Arabia",
    "director": "David Lean",
    "year": 1962,
    "genres": ["Adventure", "Biography", "Drama"]
}
PUT movies/_doc/3
{
    "title": "To Kill a Mockingbird",
    "director": "Robert Mulligan",
    "year": 1962,
    "genres": ["Crime", "Drama", "Mystery"]
}
PUT movies/_doc/4
{
    "title": "Apocalypse Now",
    "director": "Francis Ford Coppola",
    "year": 1979,
    "genres": ["Drama", "War"]
}
PUT movies/_doc/5
{
    "title": "Kill Bill: Vol. 1",
    "director": "Quentin Tarantino",
    "year": 2003,
    "genres": ["Action", "Crime", "Thriller"]
}
PUT movies/_doc/6
{
    "title": "The Assassination of Jesse James by the Coward Robert Ford",
    "director": "Andrew Dominik",
    "year": 2007,
    "genres": ["Biography", "Crime", "Drama"]
}
GET /movies/_doc/1
GET /movies/_doc/10
PUT /movies/_doc/7
{
    "title": "BB kill Ford",
    "director": "AA",
    "year": 2007,
    "genres": ["Biography", "Crime", "Drama"]
}
PUT /movies/_doc/8
{
    "title": "Kill John",
    "director": "BB Ford",
    "year": 2007,
    "genres": ["Biography", "Crime", "Drama"]
}
POST /movies/_search
{
"query": {
  "query_string": {
    "query": "kill"
    }
  }
}
GET  /movies/_search
{
"query": {
  "query_string": {
    "query": "ford",
      "fields": ["title"]
    }
  }
}
GET  /movies/_search
{
"query": {
  "query_string" : {"query" : "title:ford"}
  }
}
GET  /movies/_search
{
"query": {
  "query_string" : {"query" : "title:ford OR kill"}
  }
}
PUT movies/_doc/9
{
    "title": "Kill Mamad: Vol. 1",
    "director": "Asghar Tarantino",
    "year": 2003,
    "genres": ["Action", "Crime", "Thriller"]
}
GET  /movies/_search
{
"query": {
  "query_string" : {"query" : "(title:kill) AND (director:Tarantino)"}
  }
}
GET  /movies/_search
{
"query": {
  "query_string" : {"query" : "(genres:Drama) AND (year:1962)"}
  }
}
GET  /movies/_search
{
"query": {
  "query_string" : {"query" : "(genres:Drama) AND (year:[* to 2005])"}
  }
}
GET  /movies/_search
{
"query": {
  "query_string" : {"query" : "(genres:Drama) OR (title:kill)"}
  }
}
GET  /movies/_search
{
"query": {
  "query_string" : {"query" : "(genres:Drama) OR (title:kill^2)"}
  }
}
GET  /movies/_search
    {
   	 "query": {
    		"match": {
   				 "genres": "drama"
    				}
    			}
    }
POST movies/_search
{
  "query": {
    "match": {
      "title": {
        "query": "Kill Bill",
        "operator": "or"
      }
    }
  }
}
POST /movies/_search
{
  "query": {
    "multi_match": {
      "query": "ford",
      "fields": [
        "title^3",
        "director"
      ]
    }
  }
}
POST /movies/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "genres": "drama"
          }
        },
        {
          "match": {
            "title": {
              "query":"kill",
               "boost": 3
            }
          }
        }
      ]
    }
  }
}
GET  /movies/_search
{
  "query": {
    "bool": {
      "must": {
        "bool": {
          "should": [
            {
              "match": {
                "title": "ford"
              }
            },
            {
              "match": {
                "title": "kill"
              }
            }
          ]
        }
      },
      "must_not": {
        "match": {
          "genres": "Mystery"
        }
      }
    }
  }
}
GET  /movies/_search
{
  "query": {
    "term": {
      "year": {
        "value": "2003",
        "boost": 1.0
      }
    }
  }
}
GET  /movies/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "title": "kill"
          }
        }
      ],
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "year": {
                  "gte": 1960
                }
              }
            },
            {
              "term": {
                "genres": {
                  "value": "drama"
                }
              }
            }
          ]
        }
      }
    }
  }
}
GET  /movies/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "title": "kill"
          }
        },
        {
          "range": {
            "year": {
              "gte": 1960
            }
          }
        },
        {
          "term": {
            "genres": {
              "value": "drama"
            }
          }
        }
      ]
    }
  }
}
GET  /movies/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "year": {
              "gte": 2000
            }
          }
        },
        {
          "term": {
            "genres": {
              "value": "drama"
            }
          }
        }
      ]
    }
  }
}
GET  /movies/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match_all": {}
        },
        {
          "range": {
            "year": {
              "gte": 2000
            }
          }
        },
        {
          "term": {
            "genres": {
              "value": "drama"
            }
          }
        }
      ]
    }
  }
}
PUT movies/_doc/10
{
    "title": "Kill godfatter: Vol. 1",
    "director": "Asghar Tarantino",
    "year": 2003,
    "genres": ["Action", "Crime", "Thriller"]
}
GET  /movies/_search
{
  "query": {
    "match": {
      "title": {
        "query": "godfater",
        "fuzziness": "AUTO"
      }
    }
  }
}
PUT movies/_doc/11
{
    "title": "Kill Bill Mill",
    "director": "Asghar Tarantino",
    "year": 2003,
    "genres": ["Action", "Crime", "Thriller"]
}
GET  /movies/_search
{
  "query": {
    "match_phrase": {
      "title": {
        "query": "Kill Bill",
        "slop": 2
      }
    }
  }
}
GET  /movies/_search
{
  "query": {
 	  "term": {
 		 "director": {
 			 "value": "Francis Ford Coppola"
			}
 		 }
  }
}
PUT  /movies/_mapping    
{
  "movie": {
  	"properties": {
  		"director": {
  			"type": "text",
  			"fields": {
      		"original": {
  					"type": "keyword"
  				}
  			}
  		}
  	}
  }
} 
GET  /movies/_search
{
  "query": {
 	   "term": {
		  	"director.original": "Francis Ford Coppola"
		  }
  }
}
GET movies/_search
{
"query": {
     "term": {
            "director.keyword": "Francis Ford Coppola"
        }
    }
}