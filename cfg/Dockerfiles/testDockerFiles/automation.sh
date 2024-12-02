#!/bin/bash

# Set variables
INTERFACE="h1-eth0"  # Replace with your host interface
SERVER_URL="http:///page.html"  # Replace with your server's URL
OUTPUT_DIR="/pcap_files"  # Directory inside the container
NUM_REQUESTS=100  # Total number of requests

# Ensure output directory exists
mkdir -p $OUTPUT_DIR

echo "Starting traffic capture and request generation..."

# Start tcpdump in the background
TCPDUMP_FILE="${OUTPUT_DIR}/all_requests.pcap"
tcpdump -i $INTERFACE port 443 -w $TCPDUMP_FILE &
TCPDUMP_PID=$!

echo "tcpdump started with PID: $TCPDUMP_PID"

# Generate requests
for i in $(seq 1 $NUM_REQUESTS); do
    echo "Sending request $i..."
    RESPONSE_FILE="${OUTPUT_DIR}/response_${i}.html"
    curl -o $RESPONSE_FILE -w "Request $i: %{time_total}s\n" $SERVER_URL
    sleep 1  # Optional: Add delay between requests
done

# Stop tcpdump
echo "Stopping tcpdump..."
kill $TCPDUMP_PID

# Export captured pcap files to host (if using Docker)
if [ -d "/host_pcap" ]; then
    echo "Copying pcap files to host directory..."
    cp -r $OUTPUT_DIR /host_pcap
fi

echo "Automation complete. PCAP files saved to $OUTPUT_DIR"
