#!/usr/bin/env python
"""
Author: Alliegaytor

Combine data from out.csv and in.csv.
"""

import pandas as pd
from os import listdir
from shutil import copy2

tempincsvname = 'in.csv'
tempoutcsvname = 'out.csv'

# Return all csv files matching a key
def findCsvFiles(key: str, dir: str) -> [str]:
    files = []
    if '.' in key:
        key = key.split('.')[0]
    for name in listdir('./'):
        if key in name:
            files.append(name)
    return files


# Concat indivdual csv files to a dataframe
def mergeIndividualCsv(files: [str]) -> pd.DataFrame:
    dataframes = []
    # merged = pd.DataFrame
    for csv in files:
        # supports both grafana and influxdb csv
        df = pd.read_csv(
            csv,
            comment='#',
            usecols=lambda x: x.lower() in ['time', 'temp']
        )[['time', 'temp']] # force time,temp order
        # sensor data uses 'ms' rather than 's'
        if csv == 'in_new.csv':
            df['time'] = df['time'] / 1000 # divide to get seconds
        df['temp'] = df['temp'].round(2)
        dataframes.append(df)
    return pd.concat(dataframes).drop_duplicates(subset='time').reset_index(drop=True)


# Backup csv files
def backupCsv(name: str, suffix: str) -> None:
    copy2(f'./{name}', f'./backup/{name + suffix}')


tempin = mergeIndividualCsv(['in.csv', 'in_new.csv']) # hardcode due to different time format
tempout = mergeIndividualCsv(findCsvFiles(tempoutcsvname, './'))

backupCsv(tempincsvname, '.bak')
backupCsv(tempoutcsvname, '.bak')
backupCsv('merged.csv', '.bak')

print(tempin)
print(tempout)

tempout.to_csv(tempoutcsvname, index=False)
tempin.to_csv(tempincsvname, index=False)

# tempin['temp'] = tempin['temp'].map(lambda x: str(x)[:-3]) # Remove "°C"

print(tempin.tail())
print(tempout.tail())

tempmerge = pd.merge(tempin, tempout, on='time').drop_duplicates(subset=['time'])

print(tempmerge)

tempmerge.to_csv('merged.csv')
