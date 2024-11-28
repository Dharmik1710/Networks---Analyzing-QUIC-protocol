#!/bin/bash
# Install Chromium QUIC client and dependencies

# Clone depot_tools and configure the environment
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH="$PATH:$(pwd)/depot_tools"

# Fetch and build the Chromium source
fetch --nohooks chromium
cd src
./build/install-build-deps.sh
gclient sync
gn gen out/Debug
autoninja -C out/Debug quic_client
