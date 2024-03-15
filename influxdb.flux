import "math"
import "date"

from(bucket: "influx")
  |> range(start: -7d, stop: date.truncate(t: now(), unit:30m))
  |> filter(fn: (r) => r["_measurement"] == "feinstaub")
  |> filter(fn: (r) => r["_field"] == "BME280_temperature")
  |> filter(fn: (r) => r["node"] == "esp8266-15514816")
  |> aggregateWindow(every: 30m, fn: mean, createEmpty: false)
  |> timeShift(duration: -30m)
  |> rename(columns: {
    "_time": "time",
    "_value": "temp"
  })
  |> drop(columns: ["table", "result", "_measurement", "node", "_field", "_start", "_stop"])
  |> map(fn: (r) => ({r with time: int(v: r.time) / 1000000}))
  |> map(fn: (r) => ({r with temp: math.round(x: (r.temp * 10.0)) / 10.0}))
