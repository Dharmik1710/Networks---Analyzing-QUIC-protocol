import pyshark


def analyze_tcp_time(file_path):
    """
    Analyze the TCP connection times and TLS handshake times from a PCAP file.

    Args:
        file_path (str): Path to the PCAP file.

    Returns:
        dict: Dictionary containing connection and handshake times.
    """
    # Load the PCAP file with a TCP filter
    cap = pyshark.FileCapture(file_path, display_filter="tcp")

    # Initialize variables
    connection_SYN_time = None
    connection_ACK_time = None
    tls_start_time = None
    tls_end_time = None
    download_start_time = None
    download_end_time = None
    total_time = None

    tls_server_hello_seq_num = 0.0
    not_encountered_fin_ack = True

    try:
        for packet in cap:
            try:
                # Parse TCP SYN for connection start
                if (
                    "TCP" in packet
                    and packet.tcp.flags_syn == "1"
                    and connection_SYN_time is None
                ):
                    connection_SYN_time = packet.sniff_time

                # Parse TCP ACK for connection established
                if (
                    "TCP" in packet
                    and packet.tcp.flags_ack == "1"
                    and connection_SYN_time
                    and connection_ACK_time is None
                ):
                    connection_ACK_time = packet.sniff_time

                # Parse TLS handshake start (Client Hello)
                if (
                    "TLS" in packet
                    and tls_start_time is None
                    and getattr(packet.tls, "handshake_type", None) == "1"
                ):
                    tls_start_time = packet.sniff_time

                # Parse TLS handshake end (Server Hello)
                if (
                    "TLS" in packet
                    and tls_end_time is None
                    and getattr(packet.tls, "handshake_type", None) == "2"
                ):
                    tls_server_hello_seq_num = float(packet.tcp.nxtseq)

                if (
                    "TCP" in packet
                    and tls_end_time is None
                    and float(packet.tcp.ack) == float(tls_server_hello_seq_num)
                    and tls_server_hello_seq_num != 0.0
                ):
                    tls_end_time = packet.sniff_time

                if (
                    "TLS" in packet
                    and str(packet.tls.app_data_proto).lower()
                    == "hypertext transfer protocol"
                ):
                    if download_start_time == None:
                        download_start_time = packet.sniff_time

                    if not_encountered_fin_ack:
                        download_end_time = packet.sniff_time

                # if ("TLS" in packet and not_encountered_fin_ack):
                #     download_end_time = packet.sniff_time

                if (
                    "TCP" in packet
                    and packet.tcp.flags_fin == "1"
                    and packet.tcp.flags_ack == "1"
                ):
                    not_encountered_fin_ack = False

                total_time = packet.frame_info.time_relative

            except AttributeError:
                # Skip packets that do not have expected attributes
                continue
        # print(dir(cap[16].tcp))

    finally:
        cap.close()

    tcp_connection_time = connection_ACK_time - connection_SYN_time
    tls_connection_time = tls_end_time - tls_start_time
    time_to_first_byte = download_start_time - connection_SYN_time
    download_time = download_end_time - download_start_time
    total_connection_time = tls_end_time - connection_SYN_time

    # Calculate times
    results = {
        "tcp_connection_time": tcp_connection_time,
        "tls_connection_time": tls_connection_time,
        "total_connection_time": total_connection_time,
        "time_to_first_byte": time_to_first_byte,
        "download_time": download_time,
        "total_time": total_time,
    }

    return results


def write_results_to_log(results, log_file="TCP_log.txt"):
    # Open the log file in write mode (creates or overwrites the file)
    with open(log_file, "a") as log:
        # log.write(f"Analysis Results for {file_path}:\n")
        log.write(f"TCP Connection Time: {results['tcp_connection_time']} seconds\n")
        log.write(f"TLS Connection Time: {results['tls_connection_time']} seconds\n")
        log.write(
            f"Total Connection Time: {results['total_connection_time']} seconds\n"
        )
        log.write(f"Time to First Byte: {results['time_to_first_byte']} seconds\n")
        log.write(f"Download Time: {results['download_time']} seconds\n")
        log.write(f"Total Time: {results['total_time']} seconds\n")
        log.write(" \n")
    print(f"Results have been written to {log_file}")


# Example usage
file_path = "output_nginx_tcp.pcap"
results = analyze_tcp_time(file_path)
write_results_to_log(results)

print("Analysis Results:")
print(f"TCP Connection Time: {results['tcp_connection_time']} seconds")
print(f"TLS Connection Time: {results['tls_connection_time']} seconds")
print(f"Total Connection Time: {results['total_connection_time']} seconds")
print(f"Time to First Byte: {results['time_to_first_byte']} seconds")
print(f"Download Time: {results['download_time']} seconds")
print(f"Total Time: {results['total_time']} seconds")

# write_results_to_log(results)
