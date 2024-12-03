########################################
#
# To measure the following times (QUIC):
#  - Total Time
#  - Time to first Byte
#  - Download Time
#  - Connection Time
#
#######################################
import pyshark
import csv
import sys
import os


# Load the PCAP file
def analyze_quic_time(filepath):

    cap = pyshark.FileCapture(filepath, display_filter="quic")

    # Initialize variables to store timings
    first_initial = None
    last_handshake = None
    first_payload = None
    last_payload = None

    payload = 0  # to determine that we have not encountered any payload yet

    # Iterate through QUIC packets
    for packet in cap:
        try:
            if packet.quic.long_packet_type:
                # packet_type = packet.quic.long_packet_type
                if first_initial == None:
                    first_initial = packet.sniff_time
                if payload == 0:
                    last_handshake = packet.sniff_time

        except:
            packet_type = "short header"
            payload = 1
            if first_payload == None:
                first_payload = packet.sniff_time
            last_payload = packet.sniff_time

    cap.close()

    filename = os.path.basename(filepath)
    parts = filename.split("_")
    workload_type = parts[1]

    total_time = last_payload - first_initial
    time_to_first_byte = first_payload - first_initial
    download_time = last_payload - first_payload
    connection_time = last_handshake - first_initial

    results = {
        "total_time": total_time,
        "time_to_first_byte": time_to_first_byte,
        "download_time": download_time,
        "connection_time": connection_time,
        "workload": workload_type,
    }

    print("first payload :", first_payload)
    print("last payload :", last_payload)
    print("first initial : ", first_initial)
    print("last_handshake: ", last_handshake)
    print()

    print(f"Total Time: {total_time}")
    print(f"Time to first Byte: {time_to_first_byte}")
    print(f"Download Time: {download_time}")
    print(f"Connection Time: {connection_time}")
    print(f"Workload: {workload_type}")
    print()

    return results


def write_metrics_to_csv(
    results,
):
    # base_filename = os.path.splitext(os.path.basename(filepath))[0]
    csv_file = f"assets/csvs/quic_data_log.csv"
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
                    "Total Connection Time",
                    "Time to First Byte",
                    "Download Time",
                    "Total Time",
                    "Workload",
                ]
            )

        # Write the metrics to the CSV file
        csv_writer.writerow(
            [
                results["connection_time"],
                results["time_to_first_byte"],
                results["download_time"],
                results["total_time"],
                results["workload"],
            ]
        )

    print(f"Metrics have been written to {csv_file}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <file_name>")
        sys.exit(1)
    filepath = sys.argv[1]
    results = analyze_quic_time(filepath)
    write_metrics_to_csv(results)


if __name__ == "__main__":
    main()


# write_metrics_to_csv(total_time, time_to_first_byte, download_time, connection_time)
