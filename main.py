#! usr/bin/env python3
"""
1.(DONE) get historical dogecoin price data and visualize the data
    webscraping/matplotlib
2.(DONE) get timestamp of Musk's dogecoin twitter through API call
    api requests
3.(In progress) Analyze pictures about Elon Musk's dogecoin tweets
    Google Vision API
4.(TODO)overlay twitter timestamp on price chart
    matplotlib
5. Optional: Auto buy and sell dogecoin on robinhood based on Musk's twitter
"""
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
    start_date = convert_date_to_unixtime(y1,m1,d1)
    end_date = convert_date_to_unixtime(y2,m2,d2)

    url  = f'https://finance.yahoo.com/quote/{coin}-USD/history?period1={start_date}&period2={end_date}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'

    # initiating the webdriver. Parameter includes the path of the webdriver.
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--log-level=3")
    
    driver = webdriver.Chrome(executable_path='./chromedriver',options = chrome_options) 
    driver.get(url) 
    html = driver.find_element_by_tag_name('html')
    #Webdriver press ESC to stop loading the page
    html.send_keys(Keys.ESCAPE)
    days_between = (end_date - start_date) / 86400
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

def draw(dates,prices,coin):

    fig, ax = plt.subplots()
    fig.set_size_inches((12, 10))
    ax.plot(dates, prices)

    # #Major ticks one month
    # fmt_month = mdates.MonthLocator()
    # ax.xaxis.set_major_locator(fmt_month)

    # # Minor ticks every week.
    # fmt_day = mdates.DayLocator(interval=7)
    # ax.xaxis.set_minor_locator(fmt_day)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    fig.autofmt_xdate()
    ax.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{coin} coin Price',loc='center')
    plt.show()
    


def main():
    [dates,prices] = scraping_data(2021,1,1,2021,5,18,'DOGE')
    draw(dates,prices,'DOGE')
  

if __name__ == '__main__':
    main()
    
