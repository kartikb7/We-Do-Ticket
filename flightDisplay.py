# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:24:17 2019

@author: Kartik
"""
from time import sleep
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import re
from selenium import webdriver
from datetime import datetime,timedelta


def flightDisplay(City,Date):
    city_Codes = {'atlanta':'ATL',
    'cleveland':'BKL',
    'nashville':'BNA',
    'boston':'BOS',
    'baltimore':'BWI',
    'chicago':'CHI',
    'charlotte':'CHO',
    'jacksonville':'CRG',
    'carson':'CSN',
    'cincinnati':'CVG',
    'denver':'DEN',
    'detroit':'DET',
    'green bay':'GRB',
    'houston':'HOU',
    'indianapolis':'IND',
    'los angeles':'LAX',
    'kansas city':'MCI',
    'minneapolis':'MSP',
    'new orleans':'MSY',
    'oakland':'OAK',
    'philadelphia':'PHL',
    'pittsburgh':'PIT',
    'seattle':'SEA',
    'tampa':'TPA',
    'arlington':'',
    'east rutherford':'',
    'foxborough':'',
    'glendale':'',
    'landover':'',
    'miami gardens':'',
    'orchard park':'',
    'santa clara':''
    }
    
    start_city = input("Enter your current City: ")
    dest_city = City.lower()
    flight_date = (datetime.strptime(Date, '%Y/%m/%d')- timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        city_from = city_Codes[start_city.lower()]
        city_to = city_Codes[dest_city]
        date_start = flight_date
        
        chromedriver_path = 'C:/Users/Kartik/Desktop/Study Material/Python/Project Draft/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=chromedriver_path) # This will open the Chrome window
        sleep(2)
        kayak = 'https://www.kayak.com/flights/' + city_from + '-' + city_to + '/' + date_start +'?sort=bestflight_a&fs=stops=0'
        driver.get(kayak)
        sleep(randint(18,20))
        
        # sometimes a popup shows up, so we can use a try statement to check it and close
        try:
            xp_popup_close = '//button[contains(@id,"dialog-close") and contains(@class,"Button-No-Standard-Style close ")]'
            driver.find_elements_by_xpath(xp_popup_close)[5].click()
        except Exception as e:
            pass
        sleep(randint(8,10))
        
        print('Showing flights from '+start_city+' to '+dest_city+' for '+flight_date+' (1 day before game):-')
        
        """This function takes care of the scraping part"""
        
        flight_soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        
        # to findAll as a dictionary attribute
        flight_div_soup = flight_soup.findAll('div',
                              { "class" : "Flights-Results-FlightPriceSection right-alignment sleek" } )
        
        # to findAll as a dictionary attribute
        flight_prices = []
        for v in flight_div_soup:
            flight_prices_soup = v.findAll('span',{ "class" : "price option-text" } )
            flight_prices.append(flight_prices_soup[0].text.replace('\n',''))
        
            
        flight_timings_soup = flight_soup.findAll('div',
                              { "class" : "section times" } )
        
        flight_info = []
        for eachFlight in range(0,len(flight_timings_soup)):
            flight_timings_carrier_str = flight_timings_soup[eachFlight].text.replace('\n',' ').strip()
            pat = '\+1'
            if re.search(pat,flight_timings_carrier_str)!=None:
                flight_timings_carrier_str = flight_timings_carrier_str.replace('+1','')
            #http://www.datasciencemadesimple.com/remove-spaces-in-python/
            flight_timings_carrier_dedup = re.sub(' +', ' ', flight_timings_carrier_str)
            #https://stackoverflow.com/questions/15012228/splitting-on-last-delimiter-in-python-string/40788954
            flight_timings_carrier_dedup_trim = flight_timings_carrier_dedup.replace(' — ','-')
            
            row = []
            flight_timings_carrier_array = flight_timings_carrier_dedup_trim.rsplit(' ')
            row.append(flight_timings_carrier_array[0]+flight_timings_carrier_array[1]+flight_timings_carrier_array[2])
            if(len(flight_timings_carrier_array)>4):
                flightCarrierName = ""
                for i in range(3,len(flight_timings_carrier_array)):
                    flightCarrierName= flightCarrierName +' ' + flight_timings_carrier_array[i]
                row.append(flightCarrierName)
            else:
                row.append(flight_timings_carrier_array[3])
            flight_info.append(row)
          
        
        flights_df = pd.DataFrame(flight_info,columns = ['Flight Timings','Flight Carrier'])
        len(flights_df.index)
        flights_df['Date'] = [date_start for v in range(len(flight_info))]
        flights_df['Price'] = flight_prices
        flights_df['City_From'] = [city_from for v in range(len(flight_info))]
        flights_df['City_To'] = [city_to for v in range(len(flight_info))]
        print(flights_df)
        print('\nBook Tickets on: '+kayak)
    except:
        print('Flights not found :(')
    
