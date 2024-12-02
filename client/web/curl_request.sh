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

# Number of iterations
iterations=5

# TCPDump capture options
interface="enX0"    # Adjust to the correct network interface

# Loop to repeat the process 100 times
for ((i=1; i<=iterations; i++))
do
  echo "Iteration $i"

  # Define the capture file name with the iteration number
  capture_file="/QUIC_captures/QUIC_WEB_capture$i.pcap"

  available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

  # Start tcpdump in the background to capture packets to the pcap file
  sudo tcpdump -i "$interface" port "$available_port" -w "$capture_file" &
  tcpdump_pid=$!
  echo "tcpdump pid: $tcpdump_pid"
  echo "available port: $available_port"

  sleep 2

  # Send the curl request (QUIC)
  curl -I --insecure --http3 --local-port $available_port "https://quic.nginx.org/"  >> /CURL_logs/QUIC_WEB_logs.txt 2>&1
  
  # Wait for the curl request to complete
  sleep 5
  echo "After wait"
  # Stop tcpdump after the curl request completes
  sudo kill -SIGINT $tcpdump_pid
  # wait $tcpdump_pid

  # Sleep time 10 seconds
  sleep 5  

done

for ((i=1; i<=iterations; i++))
do
  echo "Iteration $i"

  # Define the capture file name with the iteration number
  capture_file="/TCP_captures/TCP_WEB_capture$i.pcap"

  available_port=$(comm -23 <(seq 49152 65535 | sort) <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u) | shuf | head -n 1)

  # Start tcpdump in the background to capture packets to the pcap file
  sudo tcpdump -i "$interface" port "$available_port" -w "$capture_file" &
  tcpdump_pid=$!
  echo "tcpdump pid: $tcpdump_pid"
  echo "available port: $available_port"

  sleep 2

  # Send the curl request (QUIC)
  curl -I --insecure  --local-port $available_port "https://quic.nginx.org/"  >> /CURL_logs/TCP_WEB_logs.txt 2>&1
  

  # Wait for the curl request to complete
  sleep 5
  echo "After wait "
  # Stop tcpdump after the curl request completes
  sudo kill -SIGINT $tcpdump_pid
  # wait $tcpdump_pid

  # Sleep time 10 seconds
  sleep 5  

done



echo "Completed $iterations iterations"
