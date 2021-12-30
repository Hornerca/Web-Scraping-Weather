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
# print(tonight.prettify())
# print(tonight.find(class_="period-name").get_text())
# print(tonight.find(class_="short-desc").get_text())
# print(tonight.find(class_="temp temp-high").get_text())

# img=tonight.find("img")
# print(img['title'])
# print(img['alt'])

current_conditions=soup.find(id="current-conditions")
day_info={'location':current_conditions.find(class_='panel-title').get_text(),
          'summary': current_conditions.find(class_='myforecast-current-lrg').get_text(),
          'table':pd.read_html(page.text)
          }


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
    def __init__(self ):
        super().__init__()
        self.setWindowTitle("National Weather Service")
        # self.setFixedSize(1200, 600)
        self.get_data()
        # self.weatherweek=weatherweek
        # Create an outer layout
        mainLayout = QVBoxLayout()
        # Create a form layout for the label and line edit
        # topLayout = QFormLayout()
        # # Add a label and a line edit to the form layout
        # topLayout.addRow("Some Text:", QLineEdit())
        
        titleFont=QFont()
        titleFont.setBold(True)
        
        loctitle=QLabel(self.day_info['location'])
        loctitle.setFont(titleFont)
        
        weektitle=QLabel('Extended Forecast')
        weektitle.setFont(titleFont)
       
        
        weatherLayout = QHBoxLayout()
        
        # Add some checkboxes to the layout
        # color=['white','grey']
        for i in range(len(self.weatherweek)): 
            day=self.weatherweek.T[i]
            
            dayWidget=QWidget()
            dayLayout=QVBoxLayout(dayWidget)
            
            # dayLayout.setStyleSheet("background-color: white; border: 1px solid black;")
            
            for info in day[:-1]:
                temp=QLabel(info)
                temp.setWordWrap(True)
                dayLayout.addWidget(temp)
           
            weatherLayout.addWidget(dayWidget)
            weatherLayout.addSpacing(15)
       
        detailedLayout = QVBoxLayout()
        detailedtitle=QLabel('Detailed Forecast:')
        detailedtitle.setFont(titleFont)
        detailedLayout.addWidget(detailedtitle)
        
        for info in self.weatherweek['info']:
         
            detailedLayout.addWidget(QLabel(info))
            
            
        # Nest the inner layouts into the outer layout
        # outerLayout.addLayout(topLayout)
        mainLayout.addWidget(loctitle)
        mainLayout.addWidget(weektitle)
        mainLayout.addLayout(weatherLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(detailedLayout)
        # Set the window's main layout
        self.setLayout(mainLayout)
   
    def get_data(self):
        '''
        Web scrapes data from a weather website and collects forcast info

        Returns
        -------
        None.

        '''
        page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
        
        #check to see if page was downloaded successfully
        if not page.status_code==200:
            print('page downloaded didnt work')
 
        soup = BeautifulSoup(page.content, 'html.parser')
        seven_day = soup.find(id="seven-day-forecast-list")
        weather=seven_day.find_all(class_="tombstone-container")
        
        
        current_conditions=soup.find(id="current-conditions")
        self.day_info={'location':current_conditions.find(class_='panel-title').get_text(),
                  'summary': current_conditions.find(class_='myforecast-current-lrg').get_text(),
                  'table':pd.read_html(page.text)[0]
                  }
        
        
        #all days into dataframe
        self.weatherweek=pd.DataFrame(
            {'peroid':[day.find(class_="period-name").get_text() for day in weather],
             'desc':[day.find(class_="short-desc").get_text() for day in weather],
             'temps':[t.get_text() for t in seven_day.select(".tombstone-container .temp")],
              'info':[day.find('img')['title']for day in weather] 
             })
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    
    

   
    
    
