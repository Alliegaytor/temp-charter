Some small python scripts to:

1. parse and save historical weather data (temperature in 30 min intervals) from pirate weather api
2. concat the data with the data from my temperature sensor
3. graph the data

<details>
  <summary>example graphs </summary>

![](plot_7day.png)
![](plot.png)
![](plot_delta.png)

</details>


## Usage

Anyone can run the weather data collection script easily, but you must have an in.csv file formated just like how I do to use the other two scripts. Hopefully the code is simple enough to tweak to your data setup :)

1. To download pirate weather data in 30 min intervals simply add your apikey, lat, long, timezone, and how far back you want to go in `config.yml`. Then run `downloadWeatherData.py`. It will generate an `out_${date +%F}.csv` provided that it doesn't error.

2. If you have the same temperature data structure as in my `in.csv` (time s, temp) and `in_new.csv` (time ms,temp), then you can run `mergeData.py` and it will combine the `in.csv` with the `in_new.csv` (making sure to change the timestamp to seconds), as well as the `out.csv` with any other `out*.csv` files you have in the directory. It will then save a `merged.csv` with the data merged nicely.

3. You can then run `graphData.py` to generate some nice looking charts. These include comparing outside vs. inside temperatures, finding the difference between them, and calculating the minimum, maximum, and average temperature per day.

There is an example `in_new.csv` and `out_${date +%F}.csv` provided in this repo.
