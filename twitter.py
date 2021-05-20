import requests
import tweepy
import time
import datetime
import json

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

def get_tweets(usr_name):
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

        new_tweets = api.user_timeline(screen_name = 'elonmusk',count=50,max_id=oldest,lang = "en", tweet_mode = "extended")
        
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    #print(alltweets[-1])
    # print(alltweets[-1].entities)
    # df = pd.DataFrame([tweet.created_at, tweet.full_text for tweet in alltweets], columns = ["Date","tweet"])

    coin_tweets = [tw for tw in alltweets if ('doge' or 'coin' or 'dogecoin')in str(tw.full_text).lower()]
    # print(coin_tweets_dates)

    for tw in alltweets:
        if 'media' in tw.entities:
            print(tw.entities['media'][0]['media_url'])




def main():
    get_tweets('elonmusk')

if __name__ == '__main__':
    main()
