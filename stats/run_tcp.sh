#!/bin/bash

# Directory containing the .pcap files
PCAPS_DIR="assets/pcaps"

# Loop through all .pcap files in the directory and its subdirectories
find "$PCAPS_DIR" -type f -name "*.pcap" | while read -r pcap_file; do
    if [[ "$pcap_file" == *"/tcp/"* ]]; then
        echo "Processing TCP file: $pcap_file"
        python3 tcpTime.py "$pcap_file"
    fi
done
