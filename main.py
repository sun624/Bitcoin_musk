#! usr/bin/env python3
"""
1. get historical bitcoin price data and visualize the data
    webscraping/matplotlib
2. Use machine learning to tell Musk's twitter is bitcoin related
    Google Vision API
3. get timestamp of Musk's bitcoin twitter through API call
    api requests
4. overlay twitter timestamp on price chart
    matplotlib
5. Optional: Auto buy and sell bitcoin on Binance based on Musk's twitter
"""
from os import times
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import datetime
import requests
import pandas as pd
import json
import time
import math

#Using beautifulsoup cannot scrape dynamically changing webpages.

#Instead we use third party library called Selenium and webdrivers. 

def convert_date_to_unixtime(year,month,day):
    dt = datetime.datetime(year,month,day)
    timestamp = (dt - datetime.datetime(1970,1,1)).total_seconds()
    return round(timestamp)

def scraping_data(y1,m1,d1,y2,m2,d2):

    DAYS_PER_SCROLL = 100
    start_date = convert_date_to_unixtime(y1,m1,d1)
    end_date = convert_date_to_unixtime(y2,m2,d2)

    url  = f'https://finance.yahoo.com/quote/BTC-USD/history?period1={start_date}&period2={end_date}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'

    # initiating the webdriver. Parameter includes the path of the webdriver.
    chrome_options = Options()
    chrome_options.headless = True
    # start_time = time.time()
    driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options) 
    driver.get(url) 
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.ESCAPE)
    days_between = (end_date - start_date) / 86400
    scroll = math.ceil(days_between / DAYS_PER_SCROLL)
    for i in range(scroll):
        soup = BeautifulSoup(driver.page_source,'html.parser')
        date = []

        for tr in soup.tbody.contents:
            date.append(tr.contents[0].contents[0])
        print(len(date))


        html.send_keys(Keys.END)
        WebDriverWait(driver,timeout=0.5)
        time.sleep(0.3)

    driver.close()
    # print(round(time.time()-start_time,2))
def main():
    scraping_data(2017,1,1,2021,5,18)

if __name__ == '__main__':
    main()
