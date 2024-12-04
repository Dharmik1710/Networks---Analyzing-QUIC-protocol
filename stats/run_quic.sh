#!/bin/bash

# Directory containing the QUIC .pcap files
PCAPS_DIR="assets/pcaps"

# Loop through all .pcap files in the /quic/ subdirectories
find "$PCAPS_DIR" -type f -name "*.pcap" | while read -r pcap_file; do
    if [[ "$pcap_file" == *"/quic/"* ]]; then
        echo "Processing QUIC file: $pcap_file"
        python3 quicTime.py "$pcap_file"
    fi
done
