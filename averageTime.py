import os
import re
import csv
from collections import defaultdict

# Define paths for TCP and QUIC logs and result files
data_directory = "data"
tcp_log_file = os.path.join(data_directory, "WebtimestampTcp.log")
quic_log_file = os.path.join(data_directory, "WebtimestampQuic.log")
tcp_result_file = os.path.join(data_directory, "tcpWebResult.log")
quic_result_file = os.path.join(data_directory, "quicWebResult.log")

# Function to parse log files and calculate averages per website
def calculate_per_website_averages(log_file):
    website_data = defaultdict(lambda: {"connection_times": [], "ttfbs": [], "total_download_times": []})

    # Verify if the log file exists
    if not os.path.exists(log_file):
        print(f"Log file {log_file} not found.")
        return None

    # Read the log file and extract metrics
    with open(log_file, 'r') as file:
        for line in file:
            # Extract metrics using regex
            match = re.search(
                    r"^(www\.\S+) : Connection Time=(\d+) ms, TTFB=(\d+) ms, Total Download Time=(\d+) ms", line
            )

            if match:
                website = match.group(1)
                connection_time = int(match.group(2))
                ttfb = float(match.group(3))
                total_download_time = float(match.group(4))

                website_data[website]["connection_times"].append(connection_time)
                website_data[website]["ttfbs"].append(ttfb)
                website_data[website]["total_download_times"].append(total_download_time)

    # Calculate averages per website
    averages = {}
    for website, metrics in website_data.items():
        avg_connection_time = sum(metrics["connection_times"]) / len(metrics["connection_times"]) if metrics["connection_times"] else 0.0
        avg_ttfb = sum(metrics["ttfbs"]) / len(metrics["ttfbs"]) if metrics["ttfbs"] else 0.0
        avg_total_download_time = sum(metrics["total_download_times"]) / len(metrics["total_download_times"]) if metrics["total_download_times"] else 0.0
        averages[website] = (avg_connection_time, avg_ttfb, avg_total_download_time)

    return averages

# Function to write results to a CSV file
def write_results_to_file(results, result_file):
    # Write header and data
    with open(result_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Website", "AvgConnectionTime(ms)", "AvgTTFB(ms)", "AvgTotalDownloadTime(ms)"])
        for website, metrics in results.items():
            writer.writerow([website, f"{metrics[0]:.2f}", f"{metrics[1]:.2f}", f"{metrics[2]:.2f}"])

# Process both TCP and QUIC logs
def process_logs():
    print("Processing TCP log...")
    tcp_averages = calculate_per_website_averages(tcp_log_file)
    if tcp_averages:
        write_results_to_file(tcp_averages, tcp_result_file)
        print(f"TCP results written to {tcp_result_file}")

    print("Processing QUIC log...")
    quic_averages = calculate_per_website_averages(quic_log_file)
    if quic_averages:
        write_results_to_file(quic_averages, quic_result_file)
        print(f"QUIC results written to {quic_result_file}")

# Run the processing
if __name__ == "__main__":
    process_logs()
