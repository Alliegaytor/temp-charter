#!/usr/bin/env python
"""
Author: Alliegaytor

Saves historical temperature data from pirateweather as csv.
Requires API key: http://pirateweather.net/en/latest/
"""

import json
import yaml
from time import time, sleep
from random import random
import requests
import pandas as pd

with open ('config.yml', 'r') as config:
    constants = yaml.safe_load(config)

interval = 60 * 30 # 30min, unix time

excluded = ("minutely", "hourly", "daily", "alerts", "flags")

parameters = {
    "units": "si"
}

data = {}

baseurl = constants['url'] + constants['apikey'] + "/" + constants['latitude'] + "," + constants['longitude'] + ","

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


for currentTime in range(int(constants['startTime']), int(time()), interval):
    url = formatUrl(baseurl + str(currentTime), excluded)

    print(data)
    sleep(0.2 * (0.2 + random()) + 0.1)
    weather = requests.get(url, timeout=20).json()

    try:
        data[currentTime] = round(weather['currently']['temperature'], 2)
    except:
        data[currentTime] = "NaN"
        print("error, sleeping for a bit")
        sleep(5)


print(data)

# Create pandas dataframe from data
df = pd.DataFrame.from_dict(data, orient="index", columns=['temp'])
df.index.names = ['time']
# Change GMT to local and remove "GMT+x" from index
df.index = pd.to_datetime(df.index, unit='s').tz_localize('UTC').tz_convert('Australia/Melbourne').tz_localize(None) # Timezone hack

df.to_csv("out.csv")

exit()
