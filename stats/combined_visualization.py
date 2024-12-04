import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to convert time strings to milliseconds
def time_to_milliseconds(time_str):
    h, m, s = map(float, time_str.split(":"))
    total_seconds = h * 3600 + m * 60 + s
    return total_seconds * 1000 

# Load and preprocess QUIC data
quic_data = pd.read_csv("assets/csvs/quic_data_log.csv")
quic_data["Total Connection Time"] = quic_data["Total Connection Time"].apply(time_to_milliseconds)
quic_data["Time to First Byte"] = quic_data["Time to First Byte"].apply(time_to_milliseconds)
quic_data["Download Time"] = quic_data["Download Time"].apply(time_to_milliseconds)
quic_data["Total Time"] = quic_data["Total Time"].apply(time_to_milliseconds)

# Standardize column values
quic_data["Region"] = quic_data["Region"].str.strip()
quic_data["Workload"] = quic_data["Workload"].str.strip().str.lower()  # Convert to lowercase
quic_data["Filename"] = quic_data["Filename"].str.strip()

# Load and preprocess TCP data
tcp_data = pd.read_csv("assets/csvs/tcp_data_log.csv")
tcp_data["Total Connection Time"] = tcp_data["Total Connection Time"].apply(time_to_milliseconds)
tcp_data["Time to First Byte"] = tcp_data["Time to First Byte"].apply(time_to_milliseconds)
tcp_data["Download Time"] = tcp_data["Download Time"].apply(time_to_milliseconds)
tcp_data["Total Time"] = tcp_data["Total Time"].apply(time_to_milliseconds)

# Standardize column values
tcp_data["Region"] = tcp_data["Region"].str.strip()
tcp_data["Workload"] = tcp_data["Workload"].str.strip().str.lower()  # Convert to lowercase
tcp_data["Filename"] = tcp_data["Filename"].str.strip()

# Define metrics and workloads
metrics = ["Total Connection Time", "Time to First Byte", "Download Time", "Total Time"]
workloads = ["web", "video"]  # Lowercase workloads to match normalized data

# Perform comparisons
for workload in workloads:
    for metric in metrics:
        # Compare files within the same region
        for region in quic_data["Region"].unique():
            plt.figure(figsize=(10, 6))
            
            # Filter QUIC data by region and workload
            quic_region_data = quic_data[(quic_data["Region"] == region) & (quic_data["Workload"] == workload)]
            if quic_region_data.empty:
                print(f"No QUIC data for {workload} in {region} for metric {metric}")
                continue
            
            for filename in quic_region_data["Filename"].unique():
                file_data = quic_region_data[quic_region_data["Filename"] == filename][metric].sort_values().to_numpy()
                file_cdf = np.linspace(0, 1, len(file_data))
                plt.plot(file_data, file_cdf, label=f"QUIC {filename}", linestyle="-")

            # Filter TCP data by region and workload
            tcp_region_data = tcp_data[(tcp_data["Region"] == region) & (tcp_data["Workload"] == workload)]
            if tcp_region_data.empty:
                print(f"No TCP data for {workload} in {region} for metric {metric}")
                continue

            for filename in tcp_region_data["Filename"].unique():
                tcp_13_data = tcp_region_data[(tcp_region_data["Filename"] == filename) & (tcp_region_data["TLS Version"] == 1.3)][metric].sort_values().to_numpy()
                if len(tcp_13_data) > 0:
                    tcp_13_cdf = np.linspace(0, 1, len(tcp_13_data))
                    plt.plot(tcp_13_data, tcp_13_cdf, label=f"TCP (TLS 1.3) {filename}", linestyle="--")

                tcp_12_data = tcp_region_data[(tcp_region_data["Filename"] == filename) & (tcp_region_data["TLS Version"] == 1.2)][metric].sort_values().to_numpy()
                if len(tcp_12_data) > 0:
                    tcp_12_cdf = np.linspace(0, 1, len(tcp_12_data))
                    plt.plot(tcp_12_data, tcp_12_cdf, label=f"TCP (TLS 1.2) {filename}", linestyle=":")

            plt.title(f"{metric} CDF for {workload} Workload in {region}")
            plt.xlabel(f"{metric} (milliseconds)")
            plt.ylabel("CDF")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

        # Compare performance across regions for the same file
        for filename in quic_data["Filename"].unique():
            plt.figure(figsize=(10, 6))
            
            # Filter QUIC data by filename and workload
            quic_file_data = quic_data[(quic_data["Filename"] == filename) & (quic_data["Workload"] == workload)]
            if quic_file_data.empty:
                print(f"No QUIC data for {workload} and file {filename} for metric {metric}")
                continue
            
            for region in quic_file_data["Region"].unique():
                region_data = quic_file_data[quic_file_data["Region"] == region][metric].sort_values().to_numpy()
                region_cdf = np.linspace(0, 1, len(region_data))
                plt.plot(region_data, region_cdf, label=f"QUIC {region}", linestyle="-")

            # Filter TCP data by filename and workload
            tcp_file_data = tcp_data[(tcp_data["Filename"] == filename) & (tcp_data["Workload"] == workload)]
            if tcp_file_data.empty:
                print(f"No TCP data for {workload} and file {filename} for metric {metric}")
                continue
            
            for region in tcp_file_data["Region"].unique():
                tcp_13_data = tcp_file_data[(tcp_file_data["Region"] == region) & (tcp_file_data["TLS Version"] == 1.3)][metric].sort_values().to_numpy()
                if len(tcp_13_data) > 0:
                    tcp_13_cdf = np.linspace(0, 1, len(tcp_13_data))
                    plt.plot(tcp_13_data, tcp_13_cdf, label=f"TCP (TLS 1.3) {region}", linestyle="--")

                tcp_12_data = tcp_file_data[(tcp_file_data["Region"] == region) & (tcp_file_data["TLS Version"] == 1.2)][metric].sort_values().to_numpy()
                if len(tcp_12_data) > 0:
                    tcp_12_cdf = np.linspace(0, 1, len(tcp_12_data))
                    plt.plot(tcp_12_data, tcp_12_cdf, label=f"TCP (TLS 1.2) {region}", linestyle=":")

            plt.title(f"{metric} CDF for {workload} Workload across Regions for {filename}")
            plt.xlabel(f"{metric} (milliseconds)")
            plt.ylabel("CDF")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()
