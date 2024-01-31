#!/usr/bin/env python
"""
Author: Alliegaytor

Graphs the data from the 'merged.csv'
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import yaml

# Matplot variables
colormap = "jet"
plt.style.use(['ggplot', 'dark_background'])
mpl.rcParams['figure.figsize'] = [8.0, 7.0]
mpl.rcParams['date.converter'] = 'concise'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['figure.dpi'] = 200
plt.rcParams['axes.xmargin'] = 0

with open ('config.yml', 'r') as config:
    constants = yaml.safe_load(config)

data = pd.read_csv('merged.csv', dayfirst=True, usecols=['time', 'temp_x', 'temp_y'], parse_dates=["time"], index_col=["time"])
data.columns = ['T_indoors', 'T_outdoors']

print(data)

data.index = pd.to_datetime(data.index, unit='s').tz_localize('UTC').tz_convert(constants['timezone']).tz_localize(None)

data.plot().set_ylabel('temperature Celcius')
plt.savefig('plot.png')
plt.show()

data['delta'] = data['T_indoors'] - data['T_outdoors']

print(data['delta'])

data['delta'].plot().set_ylabel('ΔT (T_indoors - T_outdoors)')
plt.savefig('plot_delta.png')
plt.show()

# last 7 days @ 30 min interval = 336 data points
# TODO: Figure out a better way of using last x days
interval = data.index[-1] - data.index[-2]
interval7d = round('7D' / interval) # python type magic

data.tail(interval7d).plot().set_ylabel('temperature Celcius')
plt.savefig('plot_7day.png')
plt.show()

# Min, max, mean per 24hr

dataold = data.copy()

del data['delta']
del data['T_outdoors']

resampled = data['T_indoors'].resample('D')

del data['T_indoors']

data['T_max'] = resampled.transform('max')
data['T_min'] = resampled.transform('min')
data['T_avg'] = resampled.transform('mean')

data = data.resample('D').first()

print(data)

data.plot().set_ylabel('temperature Celcius')
plt.savefig('plot_daily.png')
plt.show()

print('\n' + '=' * 20)
print('Days above 30°C:', sum(data['T_max'] >= 30))
print('Days below 20°C:', sum(data['T_min'] <=20))

print('\n' + '=' * 20)
print('Maximum Temp:', max(data['T_max']), '°C', 'at', dataold['T_indoors'].idxmax())
print('Minimum Temp:', min(data['T_min']), '°C', 'at', dataold['T_indoors'].idxmin())
