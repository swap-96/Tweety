import random
import tweepy
import os
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
SIA = SentimentIntensityAnalyzer()

# DO NOT COMMIT KEYS!!!!
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
except:
    print("Error during authentication")
# Create a tweet
# api.update_status("Timo Werner!!")

# Print Timeline
timeline = api.home_timeline()
for tweet in timeline[0:5]:
    print(tweet.user.name," said ", tweet.text)

# Clean Tweet
def clean(tweet):
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    # tweet = re.sub(r'#', '', tweet)
    # tweet = re.sub(r'@', '', tweet) 
    tweet = re.sub(r'[^\w\s]','',tweet)
    return tweet

for tweet in timeline[0:5]:
    print(tweet.user.name," said ", clean(tweet.text), '\nScore:', SIA.polarity_scores(clean(tweet.text))['compound'])

