# -*- coding: utf-8 -*-
import ast, json
from elasticsearch import Elasticsearch

host = 'localhost'
port = 9200

if __name__=="__main__":
    es = Elasticsearch([{'host': host, 'port': port}])
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