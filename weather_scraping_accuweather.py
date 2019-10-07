# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 20:17:47 2019

@author: Kartik
"""
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from datetime import datetime
from time import sleep
import re
from selenium import webdriver
import matplotlib.pyplot as plt

completeWeatherData = pd.DataFrame(columns = ['Date', 'High', 'Low', 'City'])

# Used in creating URLs for Accuweather website
cityURLs = {
'atlanta':['30303','348181'],
'arlington':['76010','331134'],
'cleveland':['44113','350127'],
'nashville':['37243','351090'],
'boston':['02108','348735'],
'baltimore':['21202','348707'],
'chicago':['60608','348308'],
'charlotte':['28202','349818'],
'jacksonville':['32202','347935'],
'carson':['90745','332067'],
'cincinnati':['45229','350126'],
'denver':['80203','347810'],
'detroit':['48226','348755'],
'green-bay':['54303','1868'],
'houston':['77002','351197'],
'indianapolis':['46204','348323'],
'los-angeles':['90012','347625'],
'kansas-city':['64106','329441'],
'minneapolis':['55415','348794'],
'new-orleans':['70112','348585'],
'oakland':['94612','347626'],
'philadelphia':['19102','350540'],
'pittsburgh':['15219','1310'],
'seattle':['98104','351409'],
'tampa':['33602','347937'],
'east-rutherford':['07073','344423'],
'foxborough':['02035','2089589'],
'glendale':['85301','331843'],
'landover':['20784','338566'],
'miami-gardens':['33056','2243453'],
'orchard-park':['14127','2128285'],
'santa-clara':['95050','331977']
}
# Defining month names for the website
monthNames = {1:'january',
              2:'february',
              3:'march',
              4:'april',
              5:'may',
              6:'june',
              7:'july',
              8:'august',
              9:'september',
              10:'october',
              11:'november',
              12:'december',}

# Defining pull data period. New month and year can be added based on requirement
months = [10,11,12]
years = [2019,2019,2019]

# Running loop for each city and month/year combination
for city in list(cityURLs.keys()):
    for month,year in list(zip(months,years)):
        # Creating URL
        url = 'https://www.accuweather.com/en/us/'+city+'/'+cityURLs[city][0]+'/'+monthNames[month]+'-weather/'+cityURLs[city][1]+'?year='+str(year)
        
        # Pulling website data using selenium webdriver
        # Webdriver behaves as a user by opening a web browser and entering url
        # Therefore, the webpage is not able to catch that the user is infact python
        # Reference - https://towardsdatascience.com/if-you-like-to-travel-let-python-help-you-scrape-the-best-fares-5a1f26213086

        chromedriver_path = 'C:/Users/Kartik/Desktop/Study Material/Python/Project Draft/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=chromedriver_path) # This will open the Chrome window
        sleep(randint(3,5))
        driver.get(url)
        sleep(randint(15,20)) #Allowing webpage to load
        
        # Fetching the website as scrape element
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        
        # Pulling the relevant metrics
        tempHighListSoup = soup.findAll('div',{ "class" : "high" })
        tempLowListSoup = soup.findAll('div',{ "class" : "low" })
        dayListSoup = soup.findAll('div',{ "class" : "date" })
        
        tempHighList = []
        tempLowList = []
        dayList = []
        
        for val in tempHighListSoup:
            tempHighList.append(val.text.strip())
        for val in tempLowListSoup:
            tempLowList.append(val.text.strip())
        for val in dayListSoup:
            dayList.append(val.text.strip())
        
        # Creating panda dataframe with the metrics
        weatherData = pd.DataFrame(list(zip(dayList,tempHighList, tempLowList)), columns = ['Date','High','Low'])
        weatherDataClean = weatherData.copy()
        
        # Removing dates that do not belong to the current month
        pat = r'/'
        for i in weatherData.index:
            if (re.search(pat,weatherData.Date[i])!=None):
                weatherDataClean = weatherDataClean.drop(i)
        
        # Converting to date format
        weatherDate = []
        for val in weatherDataClean.Date:
            weatherDate.append(datetime(year,month,int(val)).strftime('%m/%d/%Y'))
            
        weatherDataClean['Date'] = weatherDate
        weatherDataClean['City'] = city
        print(str(month)+'/'+str(year)+' - '+city+' - Scrape Complete')
        #https://www.datacamp.com/community/tutorials/joining-dataframes-pandas
        completeWeatherData = pd.concat([completeWeatherData,weatherDataClean], ignore_index=True)

completeWeatherDataClean = completeWeatherData.copy()

# Cleaning the high temp column
highClean = []
for val in completeWeatherDataClean.High:
    highClean.append(int(val.replace('°','')))

# Cleaning the low temp column
lowClean = []
for val in completeWeatherDataClean.Low:
    lowClean.append(int(val.replace('°','')))

# Cleaning the date column
dateClean = []
for val in completeWeatherDataClean.Date:
    dateClean.append(val.replace('/','-'))
    
completeWeatherDataClean['High'] = highClean
completeWeatherDataClean['Low'] = lowClean
completeWeatherDataClean['Date'] = dateClean

# Appending data to already pulled data file
oldCompleteWeatherDataClean= pd.read_csv('completeWeatherDataClean.csv')
oldCompleteWeatherDataClean = pd.concat([oldCompleteWeatherDataClean,completeWeatherDataClean], ignore_index=True)
oldCompleteWeatherDataClean.to_csv('completeWeatherDataClean.csv', index = False)

