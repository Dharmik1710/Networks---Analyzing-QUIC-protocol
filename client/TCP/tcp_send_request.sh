#!/bin/bash

# Define the target URL
URL="https://quic.nginx.org/"

# Send 100 curl requests
for i in {1..100}
do
  echo "Sending request $i to $URL"
  curl -I "$URL"
done