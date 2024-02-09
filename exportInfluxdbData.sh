#/bin/bash
#export last 7 days of temperature sensor data as csv from influxdb.
#supports influx api v2

# influxdb apikey
apikey=''
server='http://192.168.0.2:8086/api/v2/query?orgID=org' # example

curl --request POST \
              $server  \
              --header "Authorization: Token $(echo $apikey)" \
              --header 'Accept: application/csv' \
              --header 'Content-type: application/vnd.flux' \
              --data "$(cat influxdb.flux)" \
    > in_new.csv