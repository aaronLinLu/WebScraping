from HelperFunction import GetWeather,WriteADictTOCSV

### <1>. Scraping weather data and store them to a dictionary
# Start from Dec.31st, 2014, and loop for 31 times.
rootpath = 'https://www.wunderground.com/history/airport/KNYC/2014/12/31/DailyHistory.html?req_city=New+York&req_state=&req_statename=New+York&reqdb.zip=&reqdb.magic=&reqdb.wmo='
total_dates = 31
weatherData = GetWeather(url=rootpath,total_dates=total_dates)
# validating result
print("total number of hours scraped: ",len(weatherData.keys()))
if len(weatherData.keys()) > total_dates*24:
    print('More hours scraped than needed. Check later.')
elif len(weatherData.keys()) < total_dates*24:
    print('Some hours are missing...')

### <2>. Write the data to a csv
outputCSV = 'Weather_NYC_201501.csv'
WriteADictTOCSV(outputCSV=outputCSV,your_dict=weatherData,
                headerrow=['Time','Temperature','Condition'])