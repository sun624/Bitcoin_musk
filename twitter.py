import requests
import tweepy
import time
import datetime
import json

with open('secrets.json','r') as secrets:
    keys = json.load(secrets)
    consumer_key=keys['consumer_key']
    consumer_secret =keys['consumer_secret'] 
    access_token = keys['access_token'] 
    access_token_secret = keys['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit = True, wait_on_rate_limit_notify=True)


#initialize a list to hold all the tweepy Tweets
alltweets = []  

#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name = 'elonmusk',count=200, lang = "en", tweet_mode = "extended")

#save most recent tweets
alltweets.extend(new_tweets)

#save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1
#keep grabbing tweets until 3200 limits or a specfic date
while alltweets[-1].created_at >= datetime.datetime(2021,1,1):
    print(f"getting tweets before {oldest}")

    new_tweets = api.user_timeline(screen_name = 'elonmusk',count=50,max_id=oldest)
    
    alltweets.extend(new_tweets)

    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    print(f"...{len(alltweets)} tweets downloaded so far")
print(alltweets[-1].created_at)
