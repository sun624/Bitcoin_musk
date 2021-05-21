#! usr/bin/env python3
from os import times
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import requests
import pandas as pd
import json
import datetime
import time
import math

from twitter import get_coin_tweets_dates

#beautifulsoup cannot scrape dynamically changing webpages.
#Instead we use third party library called Selenium and webdrivers. 

def convert_date_to_unixtime(year,month,day):
    dt = datetime.datetime(year,month,day)
    timestamp = (dt - datetime.datetime(1970,1,1)).total_seconds()
    return round(timestamp)

def date_parser(date):
    return datetime.datetime.strptime(date, '%b %d, %Y').date()

def is_valid(s):
    return len(s) > 1

def scraping_data(y1,m1,d1,y2,m2,d2,coin):

    DAYS_PER_SCROLL = 100
    SECONDS_PER_DAY = 86400
    start_date = convert_date_to_unixtime(y1,m1,d1)
    end_date = convert_date_to_unixtime(y2,m2,d2)

    url  = f'https://finance.yahoo.com/quote/{coin}-USD/history?period1={start_date}&period2={end_date}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'

    # initiating the webdriver. Parameter includes the path of the webdriver.
    chrome_options = Options()
    # run chrome without GUI
    chrome_options.headless = True
    
    chrome_options.add_argument("--log-level=3")
    
    driver = webdriver.Chrome(executable_path='./chromedriver',options = chrome_options) 
    driver.get(url) 
    html = driver.find_element_by_tag_name('html')

    #Webdriver press ESC to stop loading the page
    html.send_keys(Keys.ESCAPE)

    days_between = (end_date - start_date) / SECONDS_PER_DAY
    scroll = math.ceil(days_between / DAYS_PER_SCROLL)
    
    for i in range(scroll):
        soup = BeautifulSoup(driver.page_source,'html.parser')
        dates = []
        prices = []
        # extract date and price information
        for tr in soup.tbody.contents:
            #Navigable string is not callable
            date_source = tr.contents[0]
            #convert navigable string into callable string
            date_string = str(date_source.string)

            date = date_parser(date_string)

            price = tr.contents[4].string
            if is_valid(price):
                dates.insert(0,date)
                prices.insert(0,float(price.replace(',','')))

        #webdriver press END key to scroll down to the buttom of the page to load more data
        html.send_keys(Keys.END)
        WebDriverWait(driver,timeout=0.5)
        time.sleep(0.3)

    driver.close()
    return [dates,prices]

"""
    draw coin price fluctuation with Elon's tweet 
"""
def draw(dates,prices,coin,tw_dates):

    fig, ax = plt.subplots()
    #set graph size 12inch by 10inch
    fig.set_size_inches((12, 10))
    #draw fist graph---coin price and date
    ax.plot(dates, prices,label='coin price')

    tw_prices = []

    for tw_date in tw_dates:
        index = dates.index(tw_date)
        tw_prices.append(prices[index])
    #draw second graph---Elon's tweet and date
    ax.plot(tw_dates,tw_prices,'ro',label='Elon\'s Doge tweet' )

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    #auto rotate x axis ticks
    fig.autofmt_xdate()
    ax.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{coin} coin Price',loc='center')
    plt.legend(loc='upper left')
    plt.show()
    


def main():
    start_time = time.time()

    [dates,prices] = scraping_data(2021,1,1,2021,5,21,'DOGE')

    tweet_dates = get_coin_tweets_dates('elonmusk')
    draw(dates,prices,'DOGE',tweet_dates)

    duration = time.time() - start_time
    print(f'It took {duration}s to run this application.')
  

if __name__ == '__main__':
    main()
    
