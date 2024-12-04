import pyshark
import csv
import sys
import os


import pyshark
import csv
import sys
import os


def analyze_tcp_time(filepath):
    """
    Analyze the times from a PCAP file.

    PCAP File should be in format: XYZ_WEB_ABC.pcap or XYZ_VIDEO_ABC.pcap

    Args:
        filepath (str): Path to the PCAP file.

    Returns:
        dict: Dictionary containing connection and handshake times.
    """
    # Load the PCAP file with a TCP filter
    cap = pyshark.FileCapture(filepath, display_filter="tcp", keep_packets=False, tshark_timeout=30)


    # Initialize variables
    connection_SYN_time = None
    connection_ACK_time = None
    tls_start_time = None
    tls_end_time = None
    download_start_time = None
    download_end_time = None
    total_time = None
    tls_version = None

    tls_server_hello_seq_num = 0.0

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
                    and connection_SYN_time is not None
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
                    if packet.tls.handshake_extensions_supported_version == "0x0304":
                        tls_version = "1.3"
                    else:
                        tls_version = "1.2"

                if (
                    "TCP" in packet
                    and tls_end_time is None
                    and float(packet.tcp.ack) == float(tls_server_hello_seq_num)
                    and tls_server_hello_seq_num != 0.0
                ):
                    tls_end_time = packet.sniff_time

                if "TLS" in packet:
                    # Safely check for app_data_proto
                    app_data_proto = getattr(packet.tls, "app_data_proto", None)
                    record_opaque_type = getattr(packet.tls, "record_opaque_type", None)

                    if (
                        app_data_proto
                        and app_data_proto.lower() == "hypertext transfer protocol"
                    ):
                        if download_start_time is None:
                            download_start_time = packet.sniff_time

                    if (
                        record_opaque_type and int(record_opaque_type) == 23
                    ):  # That doesn't show http
                        if download_start_time is None:
                            download_start_time = packet.sniff_time

                    download_end_time = packet.sniff_time  # Update continuously

                # Parse TCP FIN for connection end
                if (
                    "TCP" in packet
                    and packet.tcp.flags_fin == "1"
                    and packet.tcp.flags_ack == "1"
                ):
                    download_end_time = packet.sniff_time

                total_time = packet.sniff_time  # Update continuously

            except AttributeError:
                # Skip packets that do not have expected attributes
                continue

    except StopIteration:
        print("Reached end of PCAP file.")

    finally:
        cap.close()

    # Safely calculate times
    if connection_SYN_time and connection_ACK_time:
        tcp_connection_time = connection_ACK_time - connection_SYN_time
    else:
        tcp_connection_time = None

    tls_connection_time = (
        (tls_end_time - tls_start_time) if tls_start_time and tls_end_time else None
    )
    time_to_first_byte = (
        (download_start_time - connection_SYN_time)
        if connection_SYN_time and download_start_time
        else None
    )
    download_time = (
        (download_end_time - download_start_time)
        if download_start_time and download_end_time
        else None
    )
    total_connection_time = (
        (tls_end_time - connection_SYN_time)
        if tls_end_time and connection_SYN_time
        else None
    )
    total_time = (
        (total_time - connection_SYN_time)
        if total_time and connection_SYN_time
        else None
    )

    filename = os.path.basename(filepath)
    parts = filename.split("_")
    workload = parts[1]
    content = parts[2]
    region = parts[3]

    # Calculate times
    results = {
        "tcp_connection_time": tcp_connection_time,
        "tls_connection_time": tls_connection_time,
        "total_connection_time": total_connection_time,
        "time_to_first_byte": time_to_first_byte,
        "download_time": download_time,
        "total_time": total_time,
        "tls_version": tls_version,
        "workload": workload,
        "content": content,
        "region": region,
    }

    return results




def write_results_to_csv(results):
    # base_filename = os.path.splitext(os.path.basename(filepath))[0]
    csv_file = f"assets/csvs/tcp_data_log.csv"
    path = os.path.dirname(csv_file)
    os.makedirs(path, exist_ok=True)
    # Check if the CSV file exists to determine if we need to write headers
    file_exists = os.path.exists(csv_file)

    # Open the CSV file in append mode
    with open(csv_file, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        # If the file doesn't exist, write the headers
        if not file_exists:
            csv_writer.writerow(
                [
                    "Region",
                    "Workload",
                    "Filename",
                    "TCP Connection Time",
                    "TLS Handshake Time",
                    "Total Connection Time",
                    "Time to First Byte",
                    "Download Time",
                    "Total Time",
                    "TLS Version",
                    
                    
                    
                ]
            )

        # Write the results to the CSV file
        csv_writer.writerow(
            [
                results["region"],
                results["workload"],
                results["content"],
                results["tcp_connection_time"],
                results["tls_connection_time"],
                results["total_connection_time"],
                results["time_to_first_byte"],
                results["download_time"],
                results["total_time"],
                results["tls_version"],
                
                
                

            ]
        )

    print(f"Results have been written to {csv_file}")


# Example usage
def main():
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <file_name>")
        sys.exit(1)

    # Get the file name from the command-line arguments
    filepath = sys.argv[1]
    results = analyze_tcp_time(filepath)
    write_results_to_csv(results)

    print("Analysis Results:")
    print(f"TCP Connection Time: {results['tcp_connection_time']} seconds")
    print(f"TLS Handshake Time: {results['tls_connection_time']} seconds")
    print(f"Total Connection Time: {results['total_connection_time']} seconds")
    print(f"Time to First Byte: {results['time_to_first_byte']} seconds")
    print(f"Download Time: {results['download_time']} seconds")
    print(f"Total Time: {results['total_time']} seconds")
    print(f"TLS Version: {results['tls_version']}")
    print(f"Workload: {results['workload']}")
    print(f"Content: {results['content']}")
    print(f"Region: {results['region']}")


if __name__ == "__main__":
    main()
