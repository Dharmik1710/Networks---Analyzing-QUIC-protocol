#!/bin/bash

webName=$1
outputFile="data/WebtimestampQuic.log"

# Start time in nanoseconds
startTime=$(date +%s%N)

# Run curl with HTTP/3 and capture output
output=$(curl --http3 -w "@curl-format.txt" -o /dev/null -s -k https://$webName)

if [[ $? -ne 0 ]]; then
  echo "Error: curl failed for $webName" >> "$outputFile"
  exit 1
fi

# Record end time in nanoseconds
endTime=$(date +%s%N)

# Calculate Connection Time in milliseconds
connectionTime=$(( (endTime - startTime) / 1000000 ))

# Parse TTFB (Time to First Byte) and Total Download Time from curl output
ttfb=$(echo "$output" | grep -oP 'time_starttransfer: \K\d+(\.\d+)?')
download_time=$(echo "$output" | grep -oP 'time_total: \K\d+(\.\d+)?')

# Convert to integer milliseconds
if [[ -z "$ttfb" ]]; then
  ttfb=0
else
  ttfb=$(printf "%.0f" "$(echo "$ttfb" | awk '{print $1 * 1000}')")
fi

if [[ -z "$download_time" ]]; then
  download_time=0
else
  download_time=$(printf "%.0f" "$(echo "$download_time" | awk '{print $1 * 1000}')")
fi

# Log the results
echo "$webName : Connection Time=${connectionTime} ms, TTFB=${ttfb} ms, Total Download Time=${download_time} ms" >> "$outputFile"
