#Author: Sam Steinberg

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests, json
from pprint import pprint
import time
from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import re
from xlwt import Workbook

if __name__ == '__main__': #Main Class
    print("Ran")
    #Creating dataframe:
    model_data = pd.DataFrame(columns = ['Time','Tweet Volume', 'Headline Sentiment', 'Bitcoin VWAP'])
   
    
    #Getting headline sentiments
    #Do this for every headline in headline dataset
    #sentiment = 
    
class vwapScores():
    headers = {
        'Content-Type': 'xxxxxxx',
        'Accept': 'xxxxxxx',
        'Chain-Rider': 'xxxxxxx'
    }
    
    timeInterval = 11700 #Every 3.25 hours
    
    #Getting VWAP score for every currency available on Chainrider:
    getInfo = requests.get('https://api.chainrider.io/v1/finance/info/',
                      params={}, headers = headers)
    response_text = getInfo.text #Converting html code into readable text. Keep resonse.text do not replace it with anything
    currencies = json.loads(response_text) #Loading json data from API
    listOfCurrencies = currencies["message"]["pairs"]
    #pprint(getInfo.status_code)
    
    #When a specific timestamp matters :
    currentTime = 1584662400 #START TIME: (2/1/2020 19:00:46)
    pastTime =  currentTime - timeInterval #Time from a minute ago
    
    interval = 60 #How many data points we will have for each cryptocurrency.
    
    rowNumber = 0;
    colNumber = 0;
    
    #Creating spreadsheet
    wb = Workbook() 
    vwapSpreadsheet = wb.add_sheet('VWAP Training Data 1.xls')
                
    #Getting list of Cryptocurrencies:
    #for i in range(0, len(listOfCurrencies)):
        #if(listOfCurrencies[i] == "BTCUSD" and listOfCurrencies[i] != "BTGUSD" and listOfCurrencies[i] != "XMRUSD" and listOfCurrencies[i] != "TUSDUSD"):
    while(interval != 0):
        #Body for POST request:
        body = {
            "pair": "BTCUSD", #listOfCurrencies[i]
            "upper_unix": currentTime,
            "lower_unix": pastTime,
            "analytics": True,
            "exchanges": ["Huobi"] #Exchange we are getting VWAP from 
        }
        
        #Retrieving VWAP score:
        r = requests.post('https://api.chainrider.io/v1/finance/vwap/historic/', json=body, params={}, headers = headers)
        #pprint(r.status_code)
        response_text = r.text #Converting html code into readable text. Keep resonse.text do not replace it with anything
        vwaps = json.loads(response_text) #Loading json data from API
        
        if(r.status_code == 200):
            vwap = vwaps['message']['vwap']
            #pprint("Currency Name: " + str(vwaps['message']['pair']) + ", VWAP Score: " + str(vwap))
            pprint(currentTime)
        
        #Writing values into an Excel Spreadsheet
        vwapSpreadsheet.write(rowNumber, colNumber, "BTCUSD") #Writing name of crypto into excel doc
        colNumber = colNumber + 1 #Incrementing column
        vwapSpreadsheet.write(rowNumber, colNumber, vwap) #Writing VWAP Score into excel doc
        colNumber = colNumber + 1
        vwapSpreadsheet.write(rowNumber, colNumber, pastTime) #Writing time interval to excel doc
        #Resetting column and incrementing row
        rowNumber = rowNumber + 1 #Incrementing row
        colNumber = 0
    
        #Decrementing values to get more data points
        interval = interval - 1 
        currentTime = currentTime - timeInterval
        pastTime = pastTime - timeInterval
            
    #Resetting interval and times
    currentTime = 1580586360 #Current Time
    pastTime = 1583091960 #Time from 30 seconds ago
    interval = 240 #Getting 120 data points for each crypto
      
    #Saving Excel Spreadsheet:
    wb.save('VWAP Bitcoin March 13th-20th.xls') 

    
    
    
    
    
    