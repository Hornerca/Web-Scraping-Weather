#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 19:16:57 2021

@author: christine.horner
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
 
# page = requests.get("https://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")

#check to see if page was downloaded successfully
if not page.status_code==200:
    print('page downloaded didnt work')
    

# print(soup.prettify())

soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast-list")
weather=seven_day.find_all(class_="tombstone-container")


# #one example
# tonight=weather[3]
# # print(tonight.prettify())
# print(tonight.find(class_="period-name").get_text())
# print(tonight.find(class_="short-desc").get_text())
# print(tonight.find(class_="temp temp-high").get_text())

# img=tonight.find("img")
# print(img['title'])
# print(img['alt'])

#all days into dataframe
weatherweek=pd.DataFrame(
    {'peroid':[day.find(class_="period-name").get_text() for day in weather],
     'desc':[day.find(class_="short-desc").get_text() for day in weather],
     'temps':[t.get_text() for t in seven_day.select(".tombstone-container .temp")],
      'info':[day.find('img')['title']for day in weather] 
     })

#%% GUI
# https://realpython.com/python-pyqt-layout/#nesting-layouts-to-build-complex-guis

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *


class Window(QWidget):
    def __init__(self,weatherweek ):
        super().__init__()
        self.setWindowTitle("7 Day Forcast")
        self.setFixedSize(1200, 600)
        
        self.weatherweek=weatherweek
        # Create an outer layout
        mainLayout = QVBoxLayout()
        # Create a form layout for the label and line edit
        # topLayout = QFormLayout()
        # # Add a label and a line edit to the form layout
        # topLayout.addRow("Some Text:", QLineEdit())
        #
        mainLayout.addWidget(QLabel('Weekly Forcast Info'))
        
        weatherLayout = QHBoxLayout()
        
        # Add some checkboxes to the layout
        color=['white','grey']
        for i in range(len(self.weatherweek)): 
            day=self.weatherweek.T[i]
            
            dayWidget=QWidget()
            dayLayout=QVBoxLayout(dayWidget)
            # dayLayout.setStyleSheet("background-color: white; border: 1px solid black;")
            
            for info in day:
                temp=QLabel(info)
                temp.setWordWrap(True)
                dayLayout.addWidget(temp)
           
            weatherLayout.addWidget(dayWidget)
       
        
        # Nest the inner layouts into the outer layout
        # outerLayout.addLayout(topLayout)
        mainLayout.addLayout(weatherLayout)
        # Set the window's main layout
        self.setLayout(mainLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window(weatherweek)
    window.show()
    sys.exit(app.exec_())
    
    

   
    
    
