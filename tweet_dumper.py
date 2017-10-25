import numpy as np
import pandas as pd
import tweepy
import re
from datetime import datetime


api_key = "" # <---- Add your API Key
api_secret = "" # <---- Add your API Secret
access_token = "" # <---- Add your access token
access_token_secret = "" # <---- Add your access token secret

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
print(api)

col = []
counter = 0

class MyStreamListener(tweepy.StreamListener):
    
    
    def __init__(self, max_tweets=1000, *args, **kwargs):
        self.max_tweets = max_tweets
        super().__init__(*args, **kwargs)
    
    def on_connect(self):
        self.start_time = datetime.now()
    
    def on_status(self, status):
        try:
            #if status.coordinates:
            #    print('coords:', status.coordinates)
            self.process(status._json)
        except KeyError as e:
            print ("KeyError: ", e)
        

    def process(self, data):
        if data['coordinates'] is not None:
            #print('good')
            tweet_dict = {'text': data['text'],
                         'coordinates': data['coordinates']['coordinates'],
                         'created_at': data['created_at'],
                         'timestamp_ms': data['timestamp_ms'],
                         'user_name': data['user']['name'],
                         'user_screen_name': data['user']['screen_name']}
        else:
            #print('bad')
            tweet_dict = {'text': data['text'],
                         'coordinates': [random.random() * random.choice([180, -180]),
                                         random.random() * random.choice([90, -90])],
                         'created_at': data['created_at'],
                         'timestamp_ms': data['timestamp_ms'],
                         'user_name': data['user']['name'],
                         'user_screen_name': data['user']['screen_name']}
        col.append(tweet_dict)

        if len(col) % 10 == 0:
            value = int(100.00 * len(col) / self.max_tweets)
            mining_time = datetime.now() - self.start_time
            print("%s/%s" % (len(col), self.max_tweets))
            if len(col) >= self.max_tweets:
                myStream.disconnect()
                print("Finished")
                print("Total Mining Time: %d" % (mining_time))
                print("Tweets/Sec: %.1f" % (self.max_tweets / mining_time.seconds))
        #self.es.index(index='tweet', doc_type='tweet_data', body=json.loads(json.dumps(tweet_dict)))


    
myStreamListener = MyStreamListener(max_tweets=1000000)
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
print(myStream)


keywords = ["C++",
            "Google",
            "Facebook",
            "Columbia",
            "school",
            "university",
            "China",
            "music",
            "Machine Learning",
            "Python",
           ]

# Start a filter with an error counter of 20
for error_counter in range(20):
    try:
        myStream.filter(track = keywords, locations = [-180,-90,180,90])
        print("Total tweets in collection: %d" % len(col))
        break
    except:
        print("ERROR# %d" % (error_counter + 1))

open("tweets.txt", "w").write(str(col))

