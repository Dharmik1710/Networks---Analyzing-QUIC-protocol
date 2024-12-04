import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def time_to_milliseconds(time_str):
    """Convert time in HH:MM:SS.sss format to milliseconds."""
    h, m, s = map(float, time_str.split(":"))
    total_seconds = h * 3600 + m * 60 + s
    return total_seconds * 1000


def extract_file_size(filename):
    """Extract file size in MB from video filename (e.g., '5mb.mp4' -> 5)."""
    if "mb.mp4" in filename.lower():
        return int(filename.lower().replace("mb.mp4", "").strip())
    return 0


# Read and process QUIC data
quic_data = pd.read_csv("assets/csvs/quic_data_log.csv")
quic_data["Total Connection Time"] = quic_data["Total Connection Time"].apply(time_to_milliseconds)
quic_data["Time to First Byte"] = quic_data["Time to First Byte"].apply(time_to_milliseconds)
quic_data["Download Time"] = quic_data["Download Time"].apply(time_to_milliseconds)
quic_data["Total Time"] = quic_data["Total Time"].apply(time_to_milliseconds)
quic_data["File Size (MB)"] = quic_data.apply(
    lambda row: extract_file_size(row["Filename"]) if row["Workload"].lower() == "video" else 0, axis=1
)
quic_data["Workload"] = quic_data["Workload"].str.lower()  # Normalize to lowercase

# Read and process TCP data
tcp_data = pd.read_csv("assets/csvs/tcp_data_log.csv")
tcp_data["Total Connection Time"] = tcp_data["Total Connection Time"].apply(time_to_milliseconds)
tcp_data["Time to First Byte"] = tcp_data["Time to First Byte"].apply(time_to_milliseconds)
tcp_data["Download Time"] = tcp_data["Download Time"].apply(time_to_milliseconds)
tcp_data["Total Time"] = tcp_data["Total Time"].apply(time_to_milliseconds)
tcp_data["File Size (MB)"] = tcp_data.apply(
    lambda row: extract_file_size(row["Filename"]) if row["Workload"].lower() == "video" else 0, axis=1
)
tcp_data["Workload"] = tcp_data["Workload"].str.lower()  # Normalize to lowercase

# Metrics and workloads
metrics = ["Total Connection Time", "Time to First Byte", "Download Time", "Total Time"]
workloads = ["video", "web"]

# Iterate through workloads, regions, and metrics for QUIC and TCP
for workload in workloads:
    regions = pd.concat(
        [
            quic_data[quic_data["Workload"] == workload]["Region"],
            tcp_data[tcp_data["Workload"] == workload]["Region"],
        ]
    ).unique()

    for region in regions:
        for metric in metrics:
            plt.figure(figsize=(12, 8))

            # QUIC: Plot a line for each file in the region
            quic_region_data = quic_data[
                (quic_data["Workload"] == workload) & (quic_data["Region"].str.lower() == region.lower())
            ]
            for filename in quic_region_data["Filename"].unique():
                quic_values = quic_region_data[
                    (quic_region_data["Filename"] == filename)
                ][metric].sort_values().to_numpy()
                if len(quic_values) > 0:
                    quic_cdf = np.linspace(0, 1, len(quic_values))
                    plt.plot(quic_values, quic_cdf, label=f"QUIC - {filename}", linestyle="-", linewidth=2)

            # TCP (TLS 1.3): Plot a line for each file in the region
            tcp_region_13_data = tcp_data[
                (tcp_data["Workload"] == workload)
                & (tcp_data["Region"].str.lower() == region.lower())
                & (tcp_data["TLS Version"] == 1.3)
            ]
            for filename in tcp_region_13_data["Filename"].unique():
                tcp_13_values = tcp_region_13_data[
                    (tcp_region_13_data["Filename"] == filename)
                ][metric].sort_values().to_numpy()
                if len(tcp_13_values) > 0:
                    tcp_13_cdf = np.linspace(0, 1, len(tcp_13_values))
                    plt.plot(
                        tcp_13_values,
                        tcp_13_cdf,
                        label=f"TCP (TLS 1.3) - {filename}",
                        linestyle="--",
                        linewidth=2,
                    )

            # TCP (TLS 1.2): Plot a line for each file in the region
            tcp_region_12_data = tcp_data[
                (tcp_data["Workload"] == workload)
                & (tcp_data["Region"].str.lower() == region.lower())
                & (tcp_data["TLS Version"] == 1.2)
            ]
            for filename in tcp_region_12_data["Filename"].unique():
                tcp_12_values = tcp_region_12_data[
                    (tcp_region_12_data["Filename"] == filename)
                ][metric].sort_values().to_numpy()
                if len(tcp_12_values) > 0:
                    tcp_12_cdf = np.linspace(0, 1, len(tcp_12_values))
                    plt.plot(
                        tcp_12_values,
                        tcp_12_cdf,
                        label=f"TCP (TLS 1.2) - {filename}",
                        linestyle="-.",
                        linewidth=2,
                    )

            # Customize and save the plot
            plt.title(f"{metric} CDF for {workload.capitalize()} Workload - Region: {region}")
            plt.xlabel(f"{metric} (milliseconds)")
            plt.ylabel("CDF")
            plt.legend(loc="best")
            plt.grid()
            plt.tight_layout()

            # Save the plot
            plot_filename = f"plots/{workload}/region/{region}_{metric}_cdf.png".replace(" ", "_")
            plt.savefig(plot_filename)
            print(f"Saved plot to {plot_filename}")
            plt.close()
