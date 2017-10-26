from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import os

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
region = 'us-east-1'
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = 'search-django-bdjdxhfakpxgveshtpficlgk7e.us-east-1.es.amazonaws.com'

class SearchEngine():
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    #es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

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
                            "distance": "100km",
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
