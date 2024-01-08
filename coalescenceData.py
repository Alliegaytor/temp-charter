#!/usr/bin/env python
"""
Author: Alliegaytor

Combine data from out.csv and in.csv.
"""

import json
from time import time, sleep
from random import random
import requests
import pandas as pd

tempin = pd.read_csv('in.csv')
tempout = pd.read_csv('out.csv')

# ensure lowercase
tempin.columns = tempin.columns.str.lower()
tempout.columns = tempout.columns.str.lower()

tempin.columns = ['time', 'temp']

tempin['temp'] = tempin['temp'].map(lambda x: str(x)[:-3]) # Remove "°C"

print(tempin.head())
print(tempout.head())

tempmerge = pd.merge(tempin, tempout, on='time')

print(tempmerge)

tempmerge.to_csv('merged.csv')
