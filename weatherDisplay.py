# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 11:44:02 2019

@author: Kartik
"""

from datetime import datetime
import pandas as pd

def weatherInfo(Date,City):
    completeWeatherDataClean= pd.read_csv('completeWeatherDataClean.csv')
    print(Date)
    print(City)
    cityWeather = completeWeatherDataClean[completeWeatherDataClean.City==City.lower()]
    print(cityWeather[cityWeather.Date==str(datetime.strptime(Date, '%Y/%m/%d').strftime('%m-%d-%Y'))])