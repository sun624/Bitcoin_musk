import requests
import tweepy
import time
import datetime
import json
from imageAnalyzer import analyze_picture

"""
   initialize tweepy api, load with credentials
"""
def init_api(file):
    with open(file,'r') as secrets:
        keys = json.load(secrets)
        consumer_key=keys['consumer_key']
        consumer_secret =keys['consumer_secret'] 
        access_token = keys['access_token'] 
        access_token_secret = keys['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth,wait_on_rate_limit = True, wait_on_rate_limit_notify=True)
    return api

def get_coin_tweets_dates(usr_name):
    api = init_api('secrets.json')
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = usr_name,count=200, lang = "en", tweet_mode = "extended")

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    #keep grabbing tweets until 3200 limits or a specfic date
    while alltweets[-1].created_at >= datetime.datetime(2021,1,1):
        print(f"getting tweets before {oldest}")

        new_tweets = api.user_timeline(screen_name = usr_name,count=50,max_id=oldest,lang = "en", tweet_mode = "extended")
        
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")

    #get text tweetes related to coins
    coin_text_tweets_dates = [tw.created_at for tw in alltweets if ('doge' or 'coin' or 'dogecoin')in str(tw.full_text).lower()]
    print(f'{len(coin_text_tweets_dates)} text tweets related to Doge')
  
    #get img tweets related to coins
    coin_img_tweets_dates = []
    for tw in alltweets:
        if 'media' in tw.entities:
            img_url = tw.entities['media'][0]['media_url']
            if analyze_picture(img_url):
                print(img_url,'related to Doge')
                coin_img_tweets_dates.append(tw.created_at)
    print(f'{len(coin_img_tweets_dates)} images tweets related to Doge')

    # combine text tweets and image tweets
    coin_tweets_dates_origin = coin_img_tweets_dates + coin_text_tweets_dates

    # format dates to datetime.date(year,month,day)
    coin_tweets_dates=[datetime.datetime(date.year,date.month,date.day).date() for date in coin_tweets_dates_origin]

    #sort dates ascending
    coin_tweets_dates.sort()
    print(f'{len(coin_tweets_dates)} total tweets related Doge')
    return coin_tweets_dates

def main():
    get_coin_tweets_dates('elonmusk')

if __name__ == '__main__':
    main()
