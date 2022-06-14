# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:08:52 2020

@author: TimboSlicerr
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 11:23:50 2020

@author: TimboSlicerr
"""

# /root/thinclient_drives/Document/CBPRO

import cbpro
import requests, json, matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import multiprocessing 

from apscheduler.schedulers.background import BackgroundScheduler

import time

from datetime import datetime, timedelta
import threading
import math
import os
from pytz import timezone

key = '7f455603112d89b05310af3879599877'
b64secret = 'yhfzBqZzbO7QYdpfp36hpsZqeyOj5urPqULj8uPNZgPCFsjvhn9tMhmEnITpRBZ0J17S/DeqQWXZ1LOWigYKYQ=='
passphrase = 'iluvtycrypto78$M'

auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)



minuteFirst = {}





BuySellList = {}


breakValue = False

global hours
global minutes
global days
global iteration
global index
global minLength
global currencyIndex
global totalminutes
global currencyIL




minutes = 0
hours = 0
days = 0
iteration = 1

totalminutes = 0




currencyIL = ['BTC-USD', 'ETH-USD',  'LTC-USD', 'BCH-USD', 'ADA-USD', 'DOT-USD', 'SHIB-USD', 'POLY-USD']
        
currencyIL = sorted(currencyIL)

def setUp():
    
    for cur in currencyIL:
        
        minuteFirst[cur] = []
           
        

        
print("Select Interval: Minutes, Seconds, or Hours: \nType M, S, or H then hit Enter")
intervalType = input()

print("Enter length for the Interval to Run: ")
intervalLength = float(input())

minLength = 0.00

if(intervalType == 'H'):
    print("Enter the number of Minutes:")
    minLength = float(input())
            


      
 
                
    
currencyIndex = 0  


public_client = cbpro.PublicClient()       


def checkTicker(): 
   
    global min1int, hour1int
    global minuteFirst
    global secfloat
    global minutes, hours, days
    global iteration, index
    global currencyIndex
    global tempProduct
    global tempPrice
    global totalminutes
    global currencyIL
    
    for item in range(3):
        
        tempProduct = {}
        tempPrice = 0.00
        prID = ''
        curLength = len(currencyIL)
        
        if(currencyIndex <= curLength-1):
            prID = currencyIL[currencyIndex]
            
        
        if(iteration == 1):
            
            prID = 'BTC-USD'
            tempProduct = public_client.get_product_ticker(product_id=prID)
        
            tempPrice = float(tempProduct['price'])
            
        elif(iteration != 1 and currencyIndex <= curLength-1):
            # print(currencyIndex)
            print(prID)
            if(prID == 'BTC-USD'):
                currencyIndex = currencyIndex + 1
                continue
            elif(prID != 'BTC-USD'):
                tempProduct = public_client.get_product_ticker(product_id=prID)
                tempPrice = float(tempProduct['price'])
                currencyIndex = currencyIndex + 1
                

            
        central = timezone('US/Central')
        now2 = datetime.now(central)
       
        # timenow2=now2.strftime("%H:%M:%S.%f")
        sec2 = now2.strftime('%S.%f')
        
        sec2float = float(sec2)
        curSec = sec2float - sec1float
       
        
        if(sec2float < sec1float):
            curSec = (60 - sec1float) + sec2float
            
        
        if(curSec > 59 and iteration == 1):
            
            minutes = minutes + 1
            totalminutes = totalminutes + 1
           


            
        if(minutes >= 60 and iteration == 1):
            hours = hours + 1
            minutes = 0
            
        if(hours >= 24 and iteration == 1):
            days = days + 1
            hours = 0
            pool = multiprocessing.Pool(1)
            pool.map(createDataFrames())
            
        curSecInt = int(curSec)
        
        if(curSecInt%15 == 0 and iteration == 1 and curSecInt != 60):
            currencyIndex = 0
            
        if(iteration >= 3):
            iteration = 1
        else:
            iteration = iteration + 1
            
        print(str(curSec) + ' - seconds')
        
        if(prID == ''):
            continue
       

      
        print(str(minutes) + ' - minutes')
        print(str(hours) + ' - hours')
        print(str(days) + ' - days')
        print('\n')
        print(prID)
        priceFloat = tempPrice
        print(str(priceFloat) + ' - current Price')
        
            
        
        firstIteration = True   
        
        
        if(prID == 'BTC-USD'):
        
            if(curSec >= 1):
                
                firstIteration = False
                
            if(curSec < 1):
                
              minuteFirst[prID].append(priceFloat)
    
            
        
        if(prID != 'BTC-USD'):
                  
            if(curSec < 15):
    
                  minuteFirst[prID].append(priceFloat)
        
                  
       
            

        


def ScheduleChecks():
    global sec1float, min1int, hour1int, secfloat
    global job1, scheduler
    scheduler = BackgroundScheduler()
    
    setUp()
    
     
    job1 = scheduler.add_job(checkTicker, 'interval', id='priceCheck',seconds =1)
     

    central = timezone('US/Central')
    now = datetime.now(central)
    startTime=now.strftime("%H:%M:%S.%f")
    sec1 = now.strftime('%S.%f')
    min1 = now.strftime('%M')
    hour1 = now.strftime('%H')
    
    print(min1)
    print(sec1)
    sec1float = float(sec1) + 1
    min1int = int(min1)
    hour1int = int(hour1)

    if(intervalType == 'S'):  
        scheduler.start()
        time.sleep(intervalLength)
        job1.remove()
        scheduler.shutdown()
        # t1.join()
    if(intervalType == 'M'):
        scheduler.start()
        time.sleep(int(intervalLength*60))
        job1.remove()
        # t1.join()
    if(intervalType == 'H'):
        scheduler.start()
        sleepvar = (intervalLength*60*60)
        sleepvar = sleepvar + (minLength*60)
        time.sleep(int(sleepvar))
        job1.remove()
        scheduler.shutdown()
        # t1.join()
        

    
        
def createDataFrames():
    
    central = timezone('US/Central')
    now = datetime.now(central)
    
    for cur in currencyIL:


        endTime=now.strftime("%D.%H.%M.")
        endTime = endTime.replace('/', '.')
        
        curID = cur.split('-')[0]
        folderpath = "/home/timbowarrior/"
        folderpath2 = folderpath + '/' + curID
        filepath = folderpath2 + '.' + endTime
     
        CSVName = filepath + 'MinuteData' + '.csv'
        
        if not os.path.exists(folderpath2):
            os.makedirs(folderpath2)
            
        print(CSVName)
        Minute = pd.DataFrame(minuteFirst[cur])
        Minute.to_csv(CSVName, sep='\t')

        
        

    
    
t1 = threading.Thread(target=ScheduleChecks)   
t1.start()
t1.join()
    



















        
    
