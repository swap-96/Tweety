from warnings import simplefilter  # numpy deprecated warning
simplefilter(action='ignore', category=FutureWarning)
import random
import tweepy
import os
import re
import time
from flair.models import TextClassifier
from flair.data import Sentence


# DO NOT COMMIT KEYS!!!!
name = "Bot"
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

sentiment = TextClassifier.load('en-sentiment')

# Last tweet id
f_r = open("lastTweet.txt","r")
lastId = int(f_r.readline())
f_r.close()

# Authentication for Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
except:
    print("Error during authentication")

# Clean Tweet
def clean(tweet):
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'@', '', tweet)
    return tweet

while True:
    # Get Timeline
    timeline = api.home_timeline(since_id = lastId, count = 10)
    for tweet in reversed(timeline):
        if tweet.id > lastId:
            lastId = tweet.id
            f_w = open("lastTweet.txt","w")
            f_w.write(str(lastId))
            f_w.close()
        if (tweet.user.name == name or tweet.text[0:2] == "RT" or clean(tweet.text) == "") :
            continue
        text = Sentence(clean(tweet.text))
        sentiment.predict(text)
        if(text.labels[0].value == 'POSITIVE' and text.labels[0].score > 0.2) :
            print(tweet.user.name," said ", tweet.text, '\nScore: POSITIVE')
            try:
                api.update_with_media(filename = 'happy.jpg', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
            except:
                print('error in tweet id:', tweet.id)
        elif(text.labels[0].value == 'NEGATIVE' and text.labels[0].score > 0.2) :
            print(tweet.user.name," said ", tweet.text, '\nScore: NEGATIVE')
            try:
                api.update_with_media(filename = 'sad.jpg', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
            except:
                print('error in tweet id:', tweet.id)
    time.sleep(90)


