#!/usr/bin/env python
"""
Author: Alliegaytor

Saves historical temperature data from pirateweather as csv.
Requires API key: http://pirateweather.net/en/latest/
"""

import yaml
from time import time, sleep
from random import random
import requests
import pandas as pd
from datetime import date

with open ('config.yml', 'r') as config:
    constants = yaml.safe_load(config)

interval = 60 * 30 # 30min, unix time

excluded = ("minutely", "hourly", "daily", "alerts", "flags")

parameters = {
    "units": "si"
}

data = {}

baseurl = constants['url'] + constants['apikey'] + "/" + constants['latitude'] + "," + constants['longitude'] + ","

todayDate = date.today().strftime('%Y-%m-%d')

currentUnixTime = round(int(time()) / (30 * 60)) * 30 * 60 # nearest 30 min to now

# (Psudeo-)random sleep time to keep the api happy
def apiSleep() -> float:
    return 0.2 * (0.2 + random()) + 0.1


# Format URL string with excluded properties
def formatUrl(url: str, excluded: [str]) -> str:
    exclude_count = len(excluded)

    if exclude_count > 0:
        url = url + "?exclude="

        for index in range(0, exclude_count):
            if index == exclude_count - 1:
                url += excluded[index]
                break
            url += excluded[index] + ","

    # Parameter
    for parameter in parameters:
        url += "&" + parameter + "=" + parameters[parameter]

    return url


for currentTime in range(currentUnixTime - constants['timeRange'], currentUnixTime, interval):
    url = formatUrl(baseurl + str(currentTime), excluded)

    print(data)
    sleep(apiSleep())
    weather = requests.get(url, timeout=20).json()

    try:
        data[currentTime] = round(weather['currently']['temperature'], 2)
    except:
        data[currentTime] = "NaN"
        print("error, sleeping for a bit")
        sleep(apiSleep() * 2)


print(data)

# Create pandas dataframe from data
df = pd.DataFrame.from_dict(data, orient="index", columns=['temp'])
df.index.names = ['time']

df.to_csv(f"out_{todayDate}.csv")

exit()
