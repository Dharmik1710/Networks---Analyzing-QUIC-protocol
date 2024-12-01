#!/bin/sh  

if [ -z "$1" ]; then
    NUM_REQUESTS=100 
else
    NUM_REQUESTS=$1  
fi

LOG_FILE="./logs/quic_log.txt"
> "$LOG_FILE"

URLS="https://localhost/video/milkyway.mp4 https://localhost/web/"

for url in $URLS; do
    echo "Testing $url" >> "$LOG_FILE"
    for i in $(seq 1 "$NUM_REQUESTS"); do
        echo "Request $i to $url:" >> "$LOG_FILE"
        curl --insecure --http3 -I -w "\nTime to First Byte: %{time_starttransfer}s\nConnection Time: %{time_connect}s\nTotal Time: %{time_total}s\n" -o /dev/null "$url" >> "$LOG_FILE" 2>&1
        echo "\n-------------------------" >> "$LOG_FILE"
    done
done
