#!/bin/bash

webName=$1
outputFile="data/WebtimestampTcp.log"

# Start time in nanoseconds
startTime=$(date +%s%N)

# Use curl to fetch the website and collect timing information
result=$(curl -w "TTFB=%{time_starttransfer}\nTotal=%{time_total}" -o /dev/null -s --tls-max 1.3 --tlsv1.2 "https://$webName")
if [[ $? -ne 0 ]]; then
  echo "Error: curl failed for $webName" >> "$outputFile"
  exit 1
fi

# Record end time in nanoseconds
endTime=$(date +%s%N)

# Calculate Connection Time in milliseconds
connectionTime=$(( (endTime - startTime) / 1000000 ))

# Parse TTFB and Total Download Time (convert to integer milliseconds)
ttfb=$(echo "$result" | grep -oP 'TTFB=\K\d+(\.\d+)?')
if [[ -z "$ttfb" ]]; then
  ttfb=0
else
  ttfb=$(printf "%.0f" "$(echo "$ttfb" | awk '{print $1 * 1000}')")
fi

download_time=$(echo "$result" | grep -oP 'Total=\K\d+(\.\d+)?')
if [[ -z "$download_time" ]]; then
  download_time=0
else
  download_time=$(printf "%.0f" "$(echo "$download_time" | awk '{print $1 * 1000}')")
fi

# Log the results
echo "$webName : Connection Time=${connectionTime} ms, TTFB=${ttfb} ms, Total Download Time=${download_time} ms" >> "$outputFile"
