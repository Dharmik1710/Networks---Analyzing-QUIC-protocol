# #!/bin/sh  

# if [ -z "$1" ]; then
#     NUM_REQUESTS=100 
# else
#     NUM_REQUESTS=$1  
# fi

# LOG_FILE="./logs/quic_log.txt"
# > "$LOG_FILE"

# URLS="https://localhost/video/milkyway.mp4 https://localhost/web/"

# for url in $URLS; do
#     echo "Testing $url" >> "$LOG_FILE"
#     for i in $(seq 1 "$NUM_REQUESTS"); do
#         echo "Request $i to $url:" >> "$LOG_FILE"
#         curl --insecure --http3 -I -w "\nTime to First Byte: %{time_starttransfer}s\nConnection Time: %{time_connect}s\nTotal Time: %{time_total}s\n" -o /dev/null "$url" >> "$LOG_FILE" 2>&1
#         echo "\n-------------------------" >> "$LOG_FILE"
#     done
# done

  
#!/bin/bash

# if [ -z "$1" ]; then
#     NUM_REQUESTS=100 
# else
#     NUM_REQUESTS=$1  
# fi

# LOG_FILE="./logs/quic_log.txt"
# > "$LOG_FILE"

# URLS="https://localhost/video/milkyway.mp4 https://localhost/web/"

# for url in $URLS; do
#     echo "Testing $url" >> "$LOG_FILE"
#     for i in $(seq 1 "$NUM_REQUESTS"); do
#         echo "Request $i to $url:" >> "$LOG_FILE"
#         curl --insecure --http3 -I -w "\nTime to First Byte: %{time_starttransfer}s\nConnection Time: %{time_connect}s\nTotal Time: %{time_total}s\n" -o /dev/null "$url" >> "$LOG_FILE" 2>&1
#         echo "\n-------------------------" >> "$LOG_FILE"
#     done
# done












#!/bin/bash

# Default number of iterations
iterations=1

# Default region
region="default"

echo "Arguments: $# $@"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --iterations) iterations="$2"; shift ;;
        --region) region="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo "Region: $region"

# TCPDump capture options
# interface="eth0"    # Adjust to the correct network interface

contents=("index.html" "api/sample.json" "docs/sample.csv" "docs/sample.pdf" "images/sample.jpg" "images/sample.png")

# QUIC Web Workload
for ((i=1; i<=iterations; i++)); do
  for content in "${contents[@]}"; do
    echo "QUIC Web Workload - Content $content - Iteration $i"

    content_name="${content##*/}"
 
    # Construct the capture file path
    capture_file="/pcaps/web/quic/QUIC_WEB_${content_name}_${region}_capture$i.pcap"

    # available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

    # Start tcpdump in the background to capture packets to the pcap file
    tcpdump -i any -w "$capture_file" &
    tcpdump_pid=$!
    echo "tcpdump pid: $tcpdump_pid"
    # echo "available port: $available_port"

    sleep 2

    # Send the curl request (QUIC)
    curl -v --insecure --http3 "https://172.17.0.4:8443/web/$content" >> /CURL_logs/QUIC_WEB_logs.txt 2>&1

    # Wait for the curl request to complete
    sleep 5
    echo "After wait"

    # Stop tcpdump after the curl request completes
    kill -SIGINT $tcpdump_pid

    sleep 2
  done
done

# TCP Web Workload
for ((i=1; i<=iterations; i++)); do
  for content in "${contents[@]}"; do
    echo "TCP Web Workload - Content $content - Iteration $i"

    content_name="${content##*/}"
    capture_file="/pcaps/web/tcp/TCP_WEB_${content_name}_${region}_capture$i.pcap"
    
    # available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

    # Start tcpdump in the background to capture packets to the pcap file
    tcpdump -i any -w "$capture_file" &
    tcpdump_pid=$!
    echo "tcpdump pid: $tcpdump_pid"
    # echo "available port: $available_port"

    sleep 2

    # Send the curl request (TCP)
    curl -v --insecure "https://172.17.0.4:8443/web/$content" >> /CURL_logs/TCP_WEB_logs.txt 2>&1

    # Wait for the curl request to complete
    sleep 5
    echo "After wait"

    # Stop tcpdump after the curl request completes
    kill -SIGINT $tcpdump_pid

    sleep 2
  done
done


# File size array
file_sizes=("1mb" "10mb" "50mb" "100mb")

# QUIC Video Workload
for ((i=1; i<=iterations-65; i++)); do
  for size in "${file_sizes[@]}"; do
    echo "QUIC Video Workload - File milkyway${size}.MP4 - Iteration $i"

    capture_file="/pcaps/video/quic/QUIC_VIDEO_${size}_${region}_capture$i.pcap"

    # available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

    # Start tcpdump in the background to capture packets to the pcap file
    tcpdump -i any -w "$capture_file" &
    tcpdump_pid=$!
    echo "tcpdump pid: $tcpdump_pid"
    # echo "available port: $available_port"

    sleep 2

    # Send the curl request (QUIC) for the video file
    curl -v --insecure --http3 "https://172.17.0.4:8443/video/milkyway${size}.MP4" >> /CURL_logs/QUIC_VIDEO_logs.txt 2>&1

    # Wait for the curl request to complete
    sleep 5
    echo "After wait"

    # Stop tcpdump after the curl request completes
    kill -SIGINT $tcpdump_pid

    sleep 2
  done
done

# TCP Video Workload
for ((i=1; i<=iterations-65; i++)); do
  for size in "${file_sizes[@]}"; do
    echo "TCP Video Workload - File milkyway${size}.MP4 - Iteration $i"

    # Define the capture file name with the iteration number
    capture_file="/pcaps/video/tcp/TCP_VIDEO_${size}_${region}_capture$i.pcap"

    # available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

    # Start tcpdump in the background to capture packets to the pcap file
    tcpdump -i any -w "$capture_file" &
    tcpdump_pid=$!
    echo "tcpdump pid: $tcpdump_pid"
    # echo "available port: $available_port"

    sleep 2

    # Send the curl request (TCP) for the video file
    curl -v --insecure "https://172.17.0.4:8443/video/milkyway${size}.MP4" >> /CURL_logs/TCP_VIDEO_logs.txt 2>&1

    # Wait for the curl request to complete
    sleep 5
    echo "After wait"

    # Stop tcpdump after the curl request completes
    kill -SIGINT $tcpdump_pid

    sleep 2
  done
done

echo "Completed $iterations iterations"
