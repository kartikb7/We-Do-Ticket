# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:24:17 2019

@author: Kartik
"""
import pandas as pd
from datetime import datetime,timedelta
from selenium import webdriver
from random import randint
from bs4 import BeautifulSoup
import re
from time import sleep

def flightDisplay(City,Date):
    # Defining all the city airport codes in the scope of this application
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
#    'arlington':'',
    'east rutherford':'NYC',
#    'foxborough':'',
    'glendale':'CHI',
    'landover':'WAS',
    'Washington':'WAS',
    'miami gardens':'MIA',
#    'orchard park':'',
#    'santa clara':''
    }
    # Defining all the inputs necessary for the creating the URL for the website
    start_city = 'Pittsburgh'#input("Enter your current City: ") #Option to change the start city in future
    dest_city = City.lower()
    flight_date = (datetime.strptime(Date, '%Y/%m/%d')- timedelta(days=1)).strftime('%Y-%m-%d') #One date before the game
    
    # As flight websites attempt on blocking all scraping activities, it is important to put the code within try catch
    try:
        city_from = city_Codes[start_city.lower()] #fetching start city code
        city_to = city_Codes[dest_city] #fetching destination city code
        date_start = flight_date
        
        # Pulling website data using selenium webdriver
        # Webdriver behaves as a user by opening a web browser and entering url
        # Therefore, the webpage is not able to catch that the user is infact python
        # Reference - https://towardsdatascience.com/if-you-like-to-travel-let-python-help-you-scrape-the-best-fares-5a1f26213086

        chromedriver_path = 'chromedriver.exe' #Present in cwd
        driver = webdriver.Chrome(executable_path=chromedriver_path) #Opens chrome window
        sleep(2)
        kayak = 'https://www.kayak.com/flights/' + city_from + '-' + city_to + '/' + date_start +'?sort=bestflight_a&fs=stops=0'
        driver.get(kayak)
        sleep(randint(18,20)) #Allowing time to load webpage
        
        # sometimes a popup shows up, so we can use a try statement to check it and close
        try:
            popup_close = '//button[contains(@id,"dialog-close") and contains(@class,"Button-No-Standard-Style close ")]'
            driver.find_elements_by_xpath(popup_close)[5].click()
        except:
            pass
        sleep(randint(3,5))
        
        print('\nShowing flights from '+start_city+' to '+dest_city+' for '+flight_date+' (1 day before game):-')
        
        # Scraping the website as soup object  
        flight_soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        
        # Finding all the price div
        flight_div_soup = flight_soup.findAll('div',
                              { "class" : "Flights-Results-FlightPriceSection right-alignment sleek" } )
        
        # Scraping the relevant prices
        flight_prices = []
        for v in flight_div_soup:
            flight_prices_soup = v.findAll('span',{ "class" : "price option-text" } )
            flight_prices.append(flight_prices_soup[0].text.replace('\n',''))
        
        
        # Finding flight timings and carrier
        flight_timings_soup = flight_soup.findAll('div',
                              { "class" : "section times" } )
        
        # Creating arrays for flight time and carrier
        flight_info = []
        for eachFlight in range(0,len(flight_timings_soup)):
            # Cleaning each text
            flight_timings_carrier_str = flight_timings_soup[eachFlight].text.replace('\n',' ').strip()
            
            pat = '\+1' #Some flights have +1 text in time (when flight reaches next day)
            if re.search(pat,flight_timings_carrier_str)!=None:
                flight_timings_carrier_str = flight_timings_carrier_str.replace('+1','') #Removing +1 as it causes problems
            
            # Removing spaces within the text
            flight_timings_carrier_dedup = re.sub(' +', ' ', flight_timings_carrier_str)
            
            # Replacing characters to make string readable
            flight_timings_carrier_dedup_trim = flight_timings_carrier_dedup.replace(' — ','-')
            
            row = []
            flight_timings_carrier_array = flight_timings_carrier_dedup_trim.rsplit(' ')
            
            # Fetching 0,1,2 flight timing objects from array
            row.append(flight_timings_carrier_array[0]+flight_timings_carrier_array[1]+flight_timings_carrier_array[2])
            
            # Fetching flight carrier names from rest of the array (sometimes flight names have multiple words)
            flightCarrierName = ""
            for i in range(3,len(flight_timings_carrier_array)):
                flightCarrierName= flightCarrierName +' ' + flight_timings_carrier_array[i]
            row.append(flightCarrierName)
            
            flight_info.append(row)
          
        # Putting all the information to panda data frame
        flights_df = pd.DataFrame(flight_info,columns = ['Flight Timings','Flight Carrier'])
        len(flights_df.index)
        flights_df['Date'] = [date_start for v in range(len(flight_info))]
        flights_df['Price'] = flight_prices
        flights_df['City_From'] = start_city
        flights_df['City_To'] = City
        
        print(flights_df.to_string(index=False))
        print('\nBook Tickets on: '+kayak)
    except:
        print('Flights not found :(')
    
