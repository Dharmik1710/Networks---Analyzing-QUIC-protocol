import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def time_to_milliseconds(time_str):
    h, m, s = map(float, time_str.split(":"))
    total_seconds = h * 3600 + m * 60 + s
    return total_seconds * 1000 

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

metrics = ["Total Connection Time", "Time to First Byte", "Download Time", "Total Time"]
workloads = ["WEB", "VIDEO"]

for workload in workloads:
    for metric in metrics:
        plt.figure(figsize=(8, 6))

        quic_values = quic_data[quic_data["Workload"] == workload][metric].sort_values().to_numpy()
        quic_cdf = np.linspace(0, 1, len(quic_values))
        plt.plot(quic_values, quic_cdf, label="QUIC", color="purple", linestyle="-")

        tcp_13_values = tcp_data[(tcp_data["Workload"] == workload) & (tcp_data["TLS Version"] == 1.3)][metric].sort_values().to_numpy()
        tcp_13_cdf = np.linspace(0, 1, len(tcp_13_values))
        plt.plot(tcp_13_values, tcp_13_cdf, label="TCP (TLS 1.3)", color="blue", linestyle="--")

        tcp_12_values = tcp_data[(tcp_data["Workload"] == workload) & (tcp_data["TLS Version"] == 1.2)][metric].sort_values().to_numpy()
        tcp_12_cdf = np.linspace(0, 1, len(tcp_12_values))
        plt.plot(tcp_12_values, tcp_12_cdf, label="TCP (TLS 1.2)", color="black", linestyle="-")

        plt.title(f"{metric} CDF for {workload} Workload")
        plt.xlabel(f"{metric} (milliseconds)")
        plt.ylabel("CDF")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

