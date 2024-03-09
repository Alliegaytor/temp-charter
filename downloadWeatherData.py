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
from sys import argv
import subprocess

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


# Get Nearest n minute time
def nearestMin(raw_time: float, n: int) -> int:
    return round(int(raw_time) / (n * 60)) * n * 60


currentUnixTime = nearestMin(time(), 30) # nearest 30 min to now

# Parse any args
try:
    if argv[1] == "-t":
        print("Calculating collection time based on last entry")
        # TODO: Find a pythonic way
        lastLineOut = subprocess.check_output(['tail', '-1', 'out.csv']).decode("utf-8")
        lastTimeOut = int(lastLineOut.split('.')[0])
        print(f"Time now (last recorded): {currentUnixTime} ({lastTimeOut})")
        downloadRange = nearestMin(currentUnixTime - lastTimeOut, 30) + 60 * 30 * 2
    else:
        throw("")
except:
    downloadRange = constants['timeRange']

print(f"Download range has been set to : {downloadRange}")


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


for currentTime in range(currentUnixTime - downloadRange, currentUnixTime, interval):
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
