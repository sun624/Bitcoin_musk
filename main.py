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
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

