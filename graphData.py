#!/usr/bin/env python
"""
Author: Alliegaytor

Graphs the data from the 'merged.csv'
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Matplot variables
colormap = "jet"
plt.style.use(['ggplot', 'dark_background'])
mpl.rcParams['figure.figsize'] = [8.0, 7.0]
mpl.rcParams['date.converter'] = 'concise'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['figure.dpi'] = 200
plt.rcParams['axes.xmargin'] = 0


data = pd.read_csv('merged.csv', dayfirst=True, usecols=['time', 'temp_x', 'temp_y'], parse_dates=["time"], index_col=["time"])
data.columns = ['T_indoors', 'T_outdoors']

print(data)

data.plot().set_ylabel('temperature Celcius')
plt.savefig('plot.png')
plt.show()

data['delta'] = data['T_indoors'] - data['T_outdoors']

print(data['delta'])

data['delta'].plot().set_ylabel('ΔT (T_indoors - T_outdoors)')
plt.savefig('plot_delta.png')
plt.show()

# Min, max, mean per 24hr

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
plt.show()

print('\n' + '=' * 20)
print('Days above 30°C:', sum(data['T_max'] >= 30))
print('Days below 20°C:', sum(data['T_min'] <=20))
