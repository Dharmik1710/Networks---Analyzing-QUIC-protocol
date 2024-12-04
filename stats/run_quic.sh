#!/bin/bash

# Directories containing the .pcap files
VIDEO_PCAPS_DIR="assets/pcaps/video/quic"
WEB_PCAPS_DIR="assets/pcaps/web/quic"

# Function to process .pcap files in a given directory
process_pcap_files() {
    local PCAPS_DIR=$1
    find "$PCAPS_DIR" -type f -name "*.pcap" | while read -r pcap_file; do
        echo "Processing QUIC file: $pcap_file"
        python3 quicTime.py "$pcap_file"
    done
}

# Process video QUIC .pcap files
echo "Processing video QUIC .pcap files..."
process_pcap_files "$VIDEO_PCAPS_DIR"

# Process web QUIC .pcap files
echo "Processing web QUIC .pcap files..."
process_pcap_files "$WEB_PCAPS_DIR"
