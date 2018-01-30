#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 08:50:07 2017

@author: ashley Robertson

@Software: Spyder
"""
from Google_Stock import *
import os
import shutil
import pandas as pd
import time
from datetime import date
import inspect, os
import numpy as np

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
 #get the current directory address
cwd_end = cwd.rfind('/') #gets the last / in the string
cwd_back = cwd[:cwd_end] #gets last directory's address

############## INSERT INPUT VARIABLES ####################
companies = pd.read_csv(cwd_back + '/Market-Analysis/companylist.csv', index_col = 0)
Directory = 'DB' #WARNING: THE FILES IN THAT DIRECTORY WILL BE DELETED AND REPLACED
file = 'Market_Data.csv'
start_date = (10, 7, 2015)
end_date = None
#########################################################

path = cwd_back + '/Market-Analysis/' + Directory +'/' #gets destination directory
Dates = google_stocks('USD', start_date, end_date).Date #gets all dates between start and end
                                                        #USD gives USD/GBP which has a price for every day 
                                                        #Except Weekends


if not os.path.exists(path):  #if destination directory doesn't exists
    os.makedirs(path)         #MAKE THE DIRECTORY
else:                         #if destination directory exists
    shutil.rmtree(path)       #DELTE THE DIRECTORY
    os.makedirs(path)         #MAKE A NEW DIRECTORY

f = open(path + 'README.txt','w')
f.write('Files created on ' + str(date.today()) +'\n')
f.write('DATA WAS GATHERED FROM GOOGLE FINANCE\n')
f.write('THE FOLLOWING ERRORS OCCURED DURING THE COMPLIE: \n')

MarketData = pd.DataFrame({'N_index' : Dates.index }, index = Dates.values)
MarketDataFull = MarketData
Compund_Return = MarketData

#########################################################   
for ticker in companies['Symbol']:
    try:
        result = google_stocks(ticker, start_date, end_date) #Obtaining Security's price
        
        fullresult = result[['Date', 'Open', 'High', 'Low', 'Close']]
        
        result = result[['Date','Close']]                   #droping other columns than date and close
        if result.shape[0] > 1 :                            #Checking if the surity has any values
            result.columns = ['index', ticker]
            fullresult.columns = ['index', ticker + ' Open', ticker + ' High', ticker + ' Low', ticker + ' Close']
            
            result = result.set_index('index')
            fullresult = fullresult.set_index('index')
            
            MarketData = pd.concat([MarketData, result], axis = 1, join_axes=[MarketData.index])
            MarketDataFull = pd.concat([MarketDataFull, fullresult], axis = 1, join_axes=[MarketDataFull.index])
        else:
            ERROR = 'The ticker '+ ticker + ' was empty valued and therefore ignored'
            print (ERROR) 
            f.write(ERROR + '\n')
    except:
        ERROR = 'The ticker: ' + ticker + ' was problematic. Please check the ticker and the dates' 
        print (ERROR)
        f.write(ERROR + '\n')

MarketData = MarketData.T.drop_duplicates().T #dropping duplicate columns
MarketDataFull = MarketDataFull.T.drop_duplicates().T

MarketData.to_csv(path + 'Market_Data.csv')
MarketDataFull.to_csv(path + 'MarketDataFull.csv')
#########################################################

shape = MarketData.shape
Securities = MarketData.columns[1:]

for i in Securities:
    security = MarketData[i].dropna() #Deleting Nan values
    C_return = security.drop(security.index[-1]) #Deleting the last row
    count = 1
    for j in C_return.index:
        today = security.loc[j]
        yesterday = security.iloc[count]
        
        count = count + 1
        
        frac = (today/yesterday)
        
        C_return.set_value(j, np.log(frac))
    
    Compund_Return = pd.concat([Compund_Return, C_return], axis = 1, join_axes=[Compund_Return.index])
   
Compund_Return.to_csv(path + 'Market_Data_CR.csv')

f.close()
