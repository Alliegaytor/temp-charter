Some small python scripts to:

1. parse and save historical weather data (temperature in 30 min intervals) from pirate weather
2. concat the data with the data from my temperature sensor
3. graph the data

<details> 
  <summary>example graphs </summary>

![](plot.png)
![](plot_delta.png)

</details>


## Usage

Anyone can run the weather data collection script easily, but you must have an in.csv file formated just like how I do to use the other two scripts. Hopefully the code is simple enough to tweak to your data setup :)

To download pirate weather data in 30 min intervals simply add your apikey, lat, long, timezone, and how far back you want to go. Then run `downloadWeatherData.py`. It will generate an out.csv if it doesn't error.

If you have the same temperature data formatted csv as me then you can run `coalescenceData.py` and it will combine the `in.csv` and `out.csv` as well as any other `in*.csv` and `out*.csv` files you have in the directory. It will then save a `merged.csv` with the data merged nicely.

You can then run `graphData.py` to generate some nice looking charts.

