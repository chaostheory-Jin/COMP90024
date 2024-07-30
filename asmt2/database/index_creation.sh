curl -XPUT -k 'https://127.0.0.1:9200/crash'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
	"dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "date": {
                "type": "text"
            },
            "location": {
                "type": "text"
            },
	    "crash_count": {
                "type": "integer"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'


curl -XPUT -k 'https://127.0.0.1:9200/pollen'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
	"dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "date": {
                "type": "text"
            },
            "location": {
                "type": "text"
            },
	    "poaceae": {
                "type": "short"
            },
	    "other": {
                "type": "short"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'


curl -XPUT -k 'https://127.0.0.1:9200/weatherstats'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
    },
    "mappings": {
	"dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "location": {
                "type": "text"
            },
            "date": {
                "type": "text"
            },
            "rain": {
                "type": "float"
            },
            "maxTemp": {
                "type": "float"
            },
            "minTemp": {
                "type": "float"
            },
            "year": {
                "type": "integer"
            },
            "month": {
                "type": "integer"
            },
            "day": {
                "type": "integer"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
