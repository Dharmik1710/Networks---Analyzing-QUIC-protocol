#!/bin/bash

webName=$1
outputFile="data/WebtimestampQuic.log"

# Start time in nanoseconds
startTime=$(date +%s%N)

# Run QUIC client and capture output
output=$(depot_tools/src/out/Debug/quic_client --host=$webName --port=443 --allow_unknown_root_cert --disable_certificate_verification 2>&1)
if [[ $? -ne 0 ]]; then
  echo "Error: QUIC client failed for $webName" >> "$outputFile"
  exit 1
fi

# Record end time in nanoseconds
endTime=$(date +%s%N)

# Calculate Connection Time in milliseconds
connectionTime=$(( (endTime - startTime) / 1000000 ))

# Parse TTFB (convert to integer milliseconds)
ttfb=$(echo "$output" | grep -oP 'First Byte: \K\d+(\.\d+)?')
if [[ -z "$ttfb" ]]; then
  ttfb=0
else
  ttfb=$(printf "%.0f" "$(echo "$ttfb" | awk '{print $1 * 1000}')")
fi

# Parse Total Download Time (convert to integer milliseconds)
download_time=$(echo "$output" | grep -oP 'Download Complete: \K\d+(\.\d+)?')
if [[ -z "$download_time" ]]; then
  download_time=0
else
  download_time=$(printf "%.0f" "$(echo "$download_time" | awk '{print $1 * 1000}')")
fi

# Log the results
echo "$webName : Connection Time=${connectionTime} ms, TTFB=${ttfb} ms, Total Download Time=${download_time} ms" >> "$outputFile"
