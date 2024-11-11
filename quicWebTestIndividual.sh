#!/bin/bash

webName=$1

# Start time to calculate Connection Time
startTime=$(date +%s%N)

# Run QUIC client and capture output
output=$(/workdir/depot_tools/src/out/Debug/quic_client --host=$webName --port=443 --allow_unknown_root_cert --disable_certificate_verification)

# Record end time for Total Download Time
endTime=$(date +%s%N)

# Calculate Connection Time
connectionTime=$(( (startTime) / 1000000 ))

# Parse output for Time to First Byte (TTFB) and Total Download Time markers
ttfb=$(echo "$output" | grep -oP 'First Byte: \K\d+')
totalDownloadTime=$(( (endTime - startTime) / 1000000 ))

# Log the results in Webtimestamp.log
echo "$webName : Connection Time=$connectionTime ms, TTFB=$ttfb ms, Total Download Time=$totalDownloadTime ms" >> data/Webtimestamp.log
