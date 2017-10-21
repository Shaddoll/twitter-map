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
        self.counter = 0
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
            tweet_dict = {'text': data['text'],
                         'coordinates': data['coordinates']['coordinates'],
                         'created_at': data['created_at'],
                         'timestamp_ms': data['timestamp_ms'],
                         'user_name': data['user']['name'],
                         'user_screen_name': data['user']['screen_name']}
            col.append(tweet_dict)

            counter += 1
            if counter % 10 == 0:
                value = int(100.00 * counter / self.max_tweets)
                mining_time = datetime.now() - self.start_time
                print("%s/%s" % (counter, self.max_tweets))
                print("Tweets/Sec: %.1f" % (counter / mining_time.seconds))
                if counter >= self.max_tweets:
                    myStream.disconnect()
                    print("Finished")
                    print("Total Mining Time: %s" % (mining_time))
                    print("Tweets/Sec: %.1f" % (self.max_tweets / mining_time.seconds))
            #self.es.index(index='tweet', doc_type='tweet_data', body=json.loads(json.dumps(tweet_dict)))


    
myStreamListener = MyStreamListener(max_tweets=1000000)
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
print(myStream)


keywords = ["Jupyter",
            "Python",
            "Data Mining",
            "Machine Learning",
            "Data Science",
            "Big Data",
            "DataMining",
            "MachineLearning",
            "DataScience",
            "BigData",
            "IoT",
            "#R",
            "Trump",
            "C++",
            "Google",
            "Facebook",
            "Columbia",
            "school",
            "university",
            "America",
            "American",
            "chinese",
            "China",
            "music",
            "hip hop",
            "R&B",
           ]

# Start a filter with an error counter of 20
for error_counter in range(20):
    try:
        myStream.filter(track = keywords, locations = [-180,-90,180,90])
        print("Tweets collected: %s" % myStream.listener.counter)
        print("Total tweets in collection: %s" % len(col))
        break
    except:
        print("ERROR# %s" % (error_counter + 1))

open("tweets.txt", "w").write(str(col))

