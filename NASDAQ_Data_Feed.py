#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 11:35:02 2017

@author: ash
"""

import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import os
import numpy as np
import pandas as pd
import requests

style.use('ggplot')


def Nasdaq_feed(Tiker):
    
    url = 'http://www.nasdaq.com/symbol/' + Tiker + '/historical'
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('div',{'class':'genTable'}).table  #Only keeping the table 

    prices = []
    dates = []
    
    rows = table.findAll('tr')[1:]
    n_rows = len(rows)
    
    for i in range(1, n_rows):
        
            date = rows[i].findAll('td')[0].text[38:48]
            dates.append(date)
            
            price = float(rows[i].findAll('td')[4].text[38:48])
            prices.append(price)
            
    Table = pd.DataFrame({'date' : dates , 'price' : prices})
    return Table