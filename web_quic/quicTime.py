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

# Load the PCAP file
pcap_file = "output_nginx.pcap"

cap = pyshark.FileCapture(pcap_file, display_filter="quic")


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
            packet_type = packet.quic.long_packet_type
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


def write_metrics_to_log(
    total_time,
    time_to_first_byte,
    download_time,
    connection_time,
    log_file="QUIC_log.txt",
):

    # Open the log file in write mode
    with open(log_file, "a") as log:
        # log.write("Connection Metrics:\n")

        log.write(f"Total Connection Time: {connection_time} seconds\n")
        log.write(f"Download Time: {download_time} seconds\n")
        log.write(f"Time to First Byte: {time_to_first_byte} seconds\n")
        log.write(f"Total Time: {total_time} seconds\n")
        log.write("\n")

    print(f"Metrics have been written to {log_file}")


print("first payload :", first_payload)
print("last payload :", last_payload)
print("first initial : ", first_initial)
print("last_handshake: ", last_handshake)
print()

total_time = last_payload - first_initial
time_to_first_byte = first_payload - first_initial
download_time = last_payload - first_payload
connection_time = last_handshake - first_initial

print(f"Total Time: {total_time}")
print(f"Time to first Byte: {time_to_first_byte}")
print(f"Download Time: {download_time}")
print(f"Connection Time: {connection_time}")
print()

write_metrics_to_log(total_time, time_to_first_byte, download_time, connection_time)
