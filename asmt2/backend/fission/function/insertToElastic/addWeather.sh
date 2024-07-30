curl -XPUT -k 'https://127.0.0.1:9200/weather'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
    },
    "mappings": {
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
            "max_temp": {
                "type": "float"
            },
            "min_temp": {
                "type": "float"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
