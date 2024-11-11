#!/bin/bash

webName=$1
outputFile="data/Webtimestamp.log"

# Start time for connection in milliseconds
startTime=$(($(date +%s) * 1000))

# Use curl to fetch the website with TLS 1.3, collecting timing information
result=$(curl -w "TTFB=%{time_starttransfer}\nTotal=%{time_total}" -o /dev/null -s --tls-max 1.3 --tlsv1.2 "$webName")

# Record end time for Total Download Time in milliseconds
endTime=$(($(date +%s) * 1000))

# Calculate Connection Time in milliseconds
connectionTime=$(( endTime - startTime ))

# Extract TTFB and Total Download Time using sed
ttfb=$(echo "$result" | sed -n 's/.*TTFB=\([0-9.]*\).*/\1/p')
totalDownloadTime=$(echo "$result" | sed -n 's/.*Total=\([0-9.]*\).*/\1/p')

# Log the results
echo "$webName : Connection Time=${connectionTime}ms, TTFB=${ttfb}ms, Total Download Time=${totalDownloadTime}ms" >> "$outputFile"
