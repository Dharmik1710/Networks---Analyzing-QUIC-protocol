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

# Loop to repeat the process 100 times
for ((i=1; i<=iterations; i++))
do
  echo "Iteration $i"

  # Define the capture file name with the iteration number
  capture_file="/pcaps/web/quic/QUIC_WEB_capture_{content}__$i_${region}.pcap"

  available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

  # Start tcpdump in the background to capture packets to the pcap file
  tcpdump -i any port "$available_port" -w "$capture_file" &
  tcpdump_pid=$!
  echo "tcpdump pid: $tcpdump_pid"
  echo "available port: $available_port"

  sleep 2

  # Send the curl request (QUIC)
  curl -I -v --insecure --http3 --local-port $available_port "https://172.17.0.4:8443/web/index.html"  >> /CURL_logs/QUIC_WEB_logs.txt 2>&1
  
  # Wait for the curl request to complete
  sleep 5
  echo "After wait"
  # Stop tcpdump after the curl request completes
  kill -SIGINT $tcpdump_pid
  # wait $tcpdump_pid

  # Sleep time 10 seconds
  sleep 5  

done

for ((i=1; i<=iterations; i++))
do
  echo "Iteration $i"

  # Define the capture file name with the iteration number
  capture_file="/pcaps/web/tcp/TCP_WEB_capture_{content}__$i_${region}.pcap"

  available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

  # Start tcpdump in the background to capture packets to the pcap file
  tcpdump -i any port "$available_port" -w "$capture_file" &
  tcpdump_pid=$!
  echo "tcpdump pid: $tcpdump_pid"
  echo "available port: $available_port"

  sleep 2

  # Send the curl request (QUIC)
  curl -I -v --insecure  --local-port $available_port "https://172.17.0.4:8443/web/index.html"  >> /CURL_logs/TCP_WEB_logs.txt 2>&1
  

  # Wait for the curl request to complete
  sleep 5
  echo "After wait "
  # Stop tcpdump after the curl request completes
  kill -SIGINT $tcpdump_pid
  # wait $tcpdump_pid

  # Sleep time 10 seconds
  sleep 5  

done


# File size array
file_sizes=("1mb" "10mb" "50mb" "100mb")

# QUIC Video Workload
for size in "${file_sizes[@]}"; do
  for ((i=1; i<=iterations; i++)); do
    echo "QUIC Video Workload - File milkyway${size}.mp4 - Iteration $i"

    capture_file="/pcaps/video/quic/QUIC_VIDEO_capture_${size}_$i_${region}.pcap"

    available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

    # Start tcpdump in the background to capture packets to the pcap file
    tcpdump -i any port "$available_port" -w "$capture_file" &
    tcpdump_pid=$!
    echo "tcpdump pid: $tcpdump_pid"
    echo "available port: $available_port"

    sleep 2

    # Send the curl request (QUIC) for the video file
    curl -I -v --insecure --http3 --local-port $available_port "https://172.17.0.4:8443/video/milkyway${size}.mp4" >> /CURL_logs/QUIC_VIDEO_logs.txt 2>&1

    # Wait for the curl request to complete
    sleep 5
    echo "After wait"

    # Stop tcpdump after the curl request completes
    kill -SIGINT $tcpdump_pid

    sleep 5
  done
done

# TCP Video Workload
for size in "${file_sizes[@]}"; do
  for ((i=1; i<=iterations; i++)); do
    echo "TCP Video Workload - File milkyway${size}.mp4 - Iteration $i"

    # Define the capture file name with the iteration number
    capture_file="/pcaps/video/tcp/TCP_VIDEO_capture_${size}_$i_${region}.pcap"

    available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

    # Start tcpdump in the background to capture packets to the pcap file
    tcpdump -i any port "$available_port" -w "$capture_file" &
    tcpdump_pid=$!
    echo "tcpdump pid: $tcpdump_pid"
    echo "available port: $available_port"

    sleep 2

    # Send the curl request (TCP) for the video file
    curl -I -v --insecure --local-port $available_port "https://172.17.0.4:8443/video/milkyway${size}.mp4" >> /CURL_logs/TCP_VIDEO_logs.txt 2>&1

    # Wait for the curl request to complete
    sleep 5
    echo "After wait"

    # Stop tcpdump after the curl request completes
    kill -SIGINT $tcpdump_pid

    sleep 5
  done
done

echo "Completed $iterations iterations"
