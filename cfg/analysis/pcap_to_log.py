import pyshark

def analyze_pcap(pcap_file):
    # Initialize metrics
    dns_lookup_time = 0
    handshake_time = 0
    ttfb = 0
    download_time = 0

    dns_start_time = None
    tcp_handshake_start = None
    http_request_start = None
    http_first_response_time = None
    http_last_response_time = None

    # Load the PCAP file
    capture = pyshark.FileCapture(pcap_file)

    for packet in capture:
        try:
            # Analyze DNS packets
            if 'DNS' in packet:
                if packet.dns.flags_response == '0':  # DNS query
                    dns_start_time = float(packet.sniff_timestamp)
                elif packet.dns.flags_response == '1' and dns_start_time is not None:  # DNS response
                    dns_lookup_time = float(packet.sniff_timestamp) - dns_start_time
                    dns_start_time = None  # Reset

            # Analyze TCP handshake packets
            if 'TCP' in packet:
                if 'SYN' in packet.tcp.flags and not tcp_handshake_start:
                    tcp_handshake_start = float(packet.sniff_timestamp)
                elif 'ACK' in packet.tcp.flags and tcp_handshake_start:
                    handshake_time = float(packet.sniff_timestamp) - tcp_handshake_start
                    tcp_handshake_start = None  # Reset

            # Analyze HTTP packets
            if 'HTTP' in packet:
                if hasattr(packet.http, 'request_method') and packet.http.request_method == 'GET':
                    http_request_start = float(packet.sniff_timestamp)
                elif hasattr(packet.http, 'response_code') and packet.http.response_code == '200':
                    if not http_first_response_time:
                        http_first_response_time = float(packet.sniff_timestamp)
                    http_last_response_time = float(packet.sniff_timestamp)

        except AttributeError:
            # Ignore packets that don't have the required attributes
            continue

    # Calculate derived metrics
    if http_request_start and http_first_response_time:
        ttfb = http_first_response_time - http_request_start
    if http_request_start and http_last_response_time:
        download_time = http_last_response_time - http_request_start

    return {
        "DNS Lookup Time (s)": dns_lookup_time,
        "TCP Handshake Time (s)": handshake_time,
        "Time to First Byte (TTFB) (s)": ttfb,
        "Download Time (s)": download_time
    }

# Usage
pcap_file_path = 'path_to_your_pcap_file.pcap'  # Replace with your file path
results = analyze_pcap(pcap_file_path)
print("Calculated Metrics:")
for metric, value in results.items():
    print(f"{metric}: {value:.6f}")
