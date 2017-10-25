# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import os

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
region = 'us-east-1'
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)
host = 'https://search-twittermap-b2dv3f4dcfpxcqzkxjjv5szudy.us-east-1.es.amazonaws.com'

if __name__=="__main__":
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    #es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    #mappings = {"mappings":{"tweet_data":{"properties":{"coordinates":{"type":"geo_point"},"created_at":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"text":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"timestamp_ms":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"user_name":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"user_screen_name":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}}}}},"settings":{"index":{"number_of_shards":"5","number_of_replicas":"1"}}}
    mappings = {"mappings":{"tweet_data":{"properties":{"coordinates":{"type":"geo_point"},"created_at":{"type":"text"},"text":{"type":"text"},"timestamp_ms":{"type":"text"},"user_name":{"type":"text"},"user_screen_name":{"type":"text"}}}}}
    try:
        es.indices.create(index='tweet', body=mappings)
    except:
        pass

    error = 0
    with open("tweets_coord.txt", "r") as f:
        tweets = eval(f.read())
        print len(tweets)
        for item in tweets:
            #print(item)
            try:
                es.index(index='tweet', doc_type='tweet_data', body=item)
            except:
                error += 1
            #tweets.append(item)
    print error
