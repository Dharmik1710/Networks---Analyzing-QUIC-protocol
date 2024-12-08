#!/bin/bash

# Directories containing the .pcap files
VIDEO_PCAPS_DIR="assets/pcaps/video/tcp"
WEB_PCAPS_DIR="assets/pcaps/web/tcp"

# Function to process .pcap files in a given directory
process_pcap_files() {
    local PCAPS_DIR=$1
    find "$PCAPS_DIR" -type f -name "*.pcap" | while read -r pcap_file; do
        echo "Processing TCP file: $pcap_file"
        python3 tcpTime.py "$pcap_file"
    done
}

# Process video TCP .pcap files
echo "Processing video TCP .pcap files..."
process_pcap_files "$VIDEO_PCAPS_DIR"

# Process web TCP .pcap files
echo "Processing web TCP .pcap files..."
process_pcap_files "$WEB_PCAPS_DIR"
