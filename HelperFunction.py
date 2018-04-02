__author__ = 'Aaron'
import googlemaps
import pandas as pd
import xlrd
import json
import xlwt
import copy
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
from operator import itemgetter
from datetime import datetime
import html5lib
import lxml
import time

def GetWeather(url,total_dates):
    # Documentation
    '''
    :param url:
    :return:

    Scape weather condition (temperature, weather), Comfort (wind, humidity),
    Barometer data and visibility data for January 2015 in New York City.

    Stylization: all data stored into a dictionary, where: key := time (2015-01-02 2 pm), value := [temperature, weather, wind, humidity, barometer, visibility]
    that is: {time: [weather info at that time]}
    '''

    # store all weather condition in this dictionary
    AllWeather = dict()
    # create a list of all option dates
    yearMonth = '2015-01-'  # root of the year and month
    dates_option = []
    for i in range(1, 1+int(total_dates)):
        dates_option.append(str(i))
    for idx, item in enumerate(dates_option):
        if len(item) == 1:
            dates_option[idx] = yearMonth + str(0) + item
        else:
            dates_option[idx] = yearMonth + item

    # initiate a automatic test
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    # enter the loop for January 2015, which had 31 days
    for i in range(len(dates_option)):
        # get current date
        todate = dates_option[i]
        # go to the page
        next_btn = driver.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/div[5]/div[1]/div[1]/div[4]/a')
        next_btn.click()
        time.sleep(2)
        # process current web-page
        page = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        soup = BeautifulSoup(page, 'lxml')

        target = soup.find_all('tr', attrs={'class': 'no-metars'})
        hours, temps, weathers = [], [], []
        for tr in target:
            s = re.sub('[^A-Za-z0-9/:.]+'," ",str(tr.get_text()))
            # get hour
            h = re.sub(" ","",s[1:9])
            hours.append(h)
            # get temperature in Fahrenheit
            t = s.split("M")[1][1:5]
            temps.append(t)
            # get weather condition
            w = s.split(" ")[-2]
            if w == "Clouds":
                w = "Cloudy"
            weathers.append(w)

        # checking, if we find all lists to be equally long
        if len(hours) != len(temps) or len(temps) != len(weathers):
            print('error on date {}'.format(todate))
            raise SyntaxError('Lengths of scraping items are not equal.')
        # append to AllWeather dictionary
        for j in range(len(hours)):
            key = todate + " " + hours[j]
            AllWeather[key] = [temps[j],weathers[j]]

    time.sleep(5)
    # shut down our browser
    driver.close()

    return AllWeather

def WriteADictTOCSV(outputCSV,your_dict,headerrow):
    # Documentation
    '''
    :param outputCSV:
    :param your_dict:
    :param headerrow:
    :return:

    Given an output csv location, a dictionary with data, and a specified header row,
    it writes data in that dictionary to a csv.
    '''
    # get element we want into a list
    L = []
    for k, v in your_dict.items():
        l = list([k])
        for i in range(len(v)):
            l.append(v[i])
        L.append(l)
    # Initiate a writer, then do the processing
    with open(outputCSV,'w',newline='') as f:
        writer = csv.writer(f)
        # write header-row first
        writer.writerows([headerrow])
        # iterate through all items in the dictionary
        for ele in L:
            writer.writerows([ele])
    f.close()

    return






