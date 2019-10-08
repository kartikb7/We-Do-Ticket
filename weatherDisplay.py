# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 11:44:02 2019

@author: Kartik
"""

from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def weatherInfo(Date,City):
    # Weather data pulled using 'weather_scraping_accuweather.py' script
    completeWeatherDataClean= pd.read_csv('completeWeatherDataClean.csv')
    
    # Filtering the city
    cityWeather = completeWeatherDataClean[completeWeatherDataClean.City==City.lower().strip().replace(' ','-')]
    print('\n********** Game Day Temperature (°F) ***********\n')
    # Filtering date and printing output
    print(cityWeather[cityWeather.Date==str(datetime.strptime(Date, '%Y/%m/%d').strftime('%m-%d-%Y'))].to_string(index=False))
    
    # Creating date variables for 3 days before and after the game
    weatherDates = []
    weatherDates.append((datetime.strptime(Date, '%Y/%m/%d')- timedelta(days=3)).strftime('%m-%d-%Y'))
    if Date<'12-28-2019':
        weatherDates.append((datetime.strptime(Date, '%Y/%m/%d')+ timedelta(days=3)).strftime('%m-%d-%Y'))
    else:
        weatherDates.append('12-31-2019')
    
    # Plotting the temperature for the week
    plt.figure(figsize=(9,6))
    ax = plt.gca()
    cityWeather[(cityWeather.Date>=weatherDates[0]) & (cityWeather.Date<=weatherDates[1])].plot(kind='line',x='Date',y='High', color='red', ax=ax)
    cityWeather[(cityWeather.Date>=weatherDates[0]) & (cityWeather.Date<=weatherDates[1])].plot(kind='line',x='Date',y='Low', color='blue', ax=ax)
    ax.set_xlabel('Dates')
    ax.set_ylabel('Temperature (°F)')
    plt.suptitle('Game week\'s Max and Min Temperatures')
    plt.show()
