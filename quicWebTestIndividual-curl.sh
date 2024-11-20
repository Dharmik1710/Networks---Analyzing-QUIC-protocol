#!/bin/bash

webName=$1
outputFile="data/WebtimestampQuic.log"

# Start time in milliseconds
startTime=$(($(date +%s%N) / 1000000))

# Use curl to fetch the website over HTTP/3 (QUIC)
result=$(curl -w "TTFB=%{time_starttransfer}\nTotal=%{time_total}" \
              -o /dev/null -s --http3 "https://$webName")

if [[ $? -ne 0 ]]; then
  echo "Error: curl failed for $webName" >> "$outputFile"
  exit 1
fi

# Record end time in milliseconds
endTime=$(($(date +%s%N) / 1000000))

# Calculate Connection Time in milliseconds
connectionTime=$(( endTime - startTime ))

# Extract TTFB and Total Download Time from curl output
ttfb=$(echo "$result" | grep -oP 'TTFB=\K[0-9.]+')
totalDownloadTime=$(echo "$result" | grep -oP 'Total=\K[0-9.]+')

# Log the results
echo "$webName : Connection Time=$connectionTime ms, TTFB=${ttfb}ms, Total Download Time=${totalDownloadTime}ms" >> "$outputFile"
