from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
region = 'us-east-1'
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

host = ''

class SearchEngine():
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    def search(self, keyword):
        response = self.es.search(index="tweet", body={"query": {"match": {'text': {'query': keyword}}}})
        response = response['hits']['hits']
        tweets = []
        for text in response:
            tweets.append(text["_source"])
        return tweets
