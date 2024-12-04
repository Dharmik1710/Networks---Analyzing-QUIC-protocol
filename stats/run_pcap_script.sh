#!/bin/bash

# Directory containing the .pcap files
PCAPS_DIR="assets/pcaps"

# Loop through all .pcap files in the directory and its subdirectories
find "$PCAPS_DIR" -type f -name "*.pcap" | while read -r pcap_file; do
    # Determine whether the file belongs to tcp or quic based on its path
    if [[ "$pcap_file" == *"/tcp/"* ]]; then
        echo "Processing TCP file: $pcap_file"
        python3 tcpTime.py "$pcap_file"
    elif [[ "$pcap_file" == *"/quic/"* ]]; then
        echo "Processing QUIC file: $pcap_file"
        python3 quicTime.py "$pcap_file"
    else
        echo "Skipping unrecognized file: $pcap_file"
    fi
done
