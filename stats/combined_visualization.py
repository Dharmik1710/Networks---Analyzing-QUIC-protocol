import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def time_to_milliseconds(time_str):
    h, m, s = map(float, time_str.split(":"))
    total_seconds = h * 3600 + m * 60 + s
    return total_seconds * 1000 

# Read and process the data
quic_data = pd.read_csv("assets/csvs/quic_data_log.csv")
quic_data["Total Connection Time"] = quic_data["Total Connection Time"].apply(time_to_milliseconds)
quic_data["Time to First Byte"] = quic_data["Time to First Byte"].apply(time_to_milliseconds)
quic_data["Download Time"] = quic_data["Download Time"].apply(time_to_milliseconds)
quic_data["Total Time"] = quic_data["Total Time"].apply(time_to_milliseconds)

tcp_data = pd.read_csv("assets/csvs/tcp_data_log.csv")
tcp_data["Total Connection Time"] = tcp_data["Total Connection Time"].apply(time_to_milliseconds)
tcp_data["Time to First Byte"] = tcp_data["Time to First Byte"].apply(time_to_milliseconds)
tcp_data["Download Time"] = tcp_data["Download Time"].apply(time_to_milliseconds)
tcp_data["Total Time"] = tcp_data["Total Time"].apply(time_to_milliseconds)

# Metrics and workloads
metrics = ["Total Connection Time", "Time to First Byte", "Download Time", "Total Time"]
workloads = ["web", "video"]

# Iterate through workloads and metrics
for workload in workloads:
    for metric in metrics:
        plt.figure(figsize=(10, 8))

        # Plot CDFs for each region in QUIC
        for region in quic_data["Region"].unique():
            quic_values = quic_data[(quic_data["Workload"] == workload) & (quic_data["Region"] == region)][metric].sort_values().to_numpy()
            if len(quic_values) > 0:
                quic_cdf = np.linspace(0, 1, len(quic_values))
                plt.plot(quic_values, quic_cdf, label=f"QUIC - {region}", linestyle="-")

        # Plot CDFs for each region in TCP (TLS 1.3)
        for region in tcp_data["Region"].unique():
            tcp_13_values = tcp_data[(tcp_data["Workload"] == workload) & (tcp_data["TLS Version"] == 1.3) & (tcp_data["Region"] == region)][metric].sort_values().to_numpy()
            if len(tcp_13_values) > 0:
                tcp_13_cdf = np.linspace(0, 1, len(tcp_13_values))
                plt.plot(tcp_13_values, tcp_13_cdf, label=f"TCP (TLS 1.3) - {region}", linestyle="--")

        # Plot CDFs for each region in TCP (TLS 1.2)
        for region in tcp_data["Region"].unique():
            tcp_12_values = tcp_data[(tcp_data["Workload"] == workload) & (tcp_data["TLS Version"] == 1.2) & (tcp_data["Region"] == region)][metric].sort_values().to_numpy()
            if len(tcp_12_values) > 0:
                tcp_12_cdf = np.linspace(0, 1, len(tcp_12_values))
                plt.plot(tcp_12_values, tcp_12_cdf, label=f"TCP (TLS 1.2) - {region}", linestyle="-.")

        # Customize and display the plot
        plt.title(f"{metric} CDF for {workload.capitalize()} Workload by Region")
        plt.xlabel(f"{metric} (milliseconds)")
        plt.ylabel("CDF")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()