from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

AWS_ACCESS_KEY = 'aaa'
AWS_SECRET_KEY = 'bbb'
region = 'us-east-1'
service = 'es'

#awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'localhost'
port = 9200

class SearchEngine():
    """es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )"""
    es = Elasticsearch([{'host': host, 'port': port}])

    def search(self, keyword):
        query = {
            "query": {
                "match": {
                    'text': {
                        'query': keyword
                    }
                }
            }
        }
        response = self.es.search(index="tweet", size=2000, body=query)
        response = response['hits']['hits']
        tweets = []
        for text in response:
            tweets.append(text["_source"])
        return tweets

    def search_range(self, lat, lon):
        query = {
            "query": {
                "bool": {
                    "filter": {
                        "geo_distance": {
                            "distance": "1km",
                            "distance_type": "plane",
                            "coordinates": [lon, lat]
                        }
                    }
                }
            }
        }
        response = self.es.search(index = "tweet", size=2000, body=query)
        response = response['hits']['hits']
        tweets = []
        for text in response:
            tweets.append(text["_source"])
        return tweets
