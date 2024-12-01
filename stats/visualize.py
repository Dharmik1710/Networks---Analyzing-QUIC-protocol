import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the tcp and quic data CSV files
tcp_df = pd.read_csv('tcp_log_data.csv')
quic_df = pd.read_csv('quic_log_data.csv')

# Add a 'protocol' column to distinguish between TCP and QUIC
tcp_df['protocol'] = 'TCP'
quic_df['protocol'] = 'QUIC'

# Combine the two DataFrames into a single one
combined_df = pd.concat([tcp_df, quic_df], ignore_index=True)

# Ensure the 'protocol' column is categorical for easier plotting
combined_df['protocol'] = pd.Categorical(combined_df['protocol'], categories=['TCP', 'QUIC'])

# Create a function to plot comparisons
def plot_performance(data, x_column, y_column, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='protocol', y=y_column, data=data, palette="Set2")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)
    plt.show()

# CDF graphs
# Separate connection times for TCP and QUIC

def plot_cdf_of_connection_times(df, filename):
    """
    Plots the CDF of connection times for TCP and QUIC from the provided DataFrame.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing 'protocol' and 'connection_time' columns.
    """
    # Separate connection times for TCP and QUIC
    tcp_connection_times = df[df['protocol'] == 'TCP']['connection_time']
    quic_connection_times = df[df['protocol'] == 'QUIC']['connection_time']

    # Sort the data
    tcp_sorted = np.sort(tcp_connection_times)
    quic_sorted = np.sort(quic_connection_times)

    # Calculate the CDF for TCP and QUIC
    tcp_cdf = np.arange(1, len(tcp_sorted) + 1) / len(tcp_sorted)
    quic_cdf = np.arange(1, len(quic_sorted) + 1) / len(quic_sorted)

    # Plotting the CDFs
    plt.figure(figsize=(8, 6))
    plt.plot(tcp_sorted, tcp_cdf, label='TCP', color='blue')
    plt.plot(quic_sorted, quic_cdf, label='QUIC', color='red')

    plt.xlabel('Connection Time (ms)')
    plt.ylabel('CDF')
    plt.title('CDF of Connection Times for QUIC and TCP over IPv4')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()


# Plot boxplots for the various time-related metrics

# Connection time comparison
plot_performance(combined_df, 'protocol', 'connection_time', 
                 'Connection Time Comparison (TCP vs QUIC)', 'Protocol', 'Connection Time (ms)', 'plots/connection_time_comparison.png')

# Total time comparison (Proxy for download time)
plot_performance(combined_df, 'protocol', 'total_time', 
                 'Download Time (Total Time) Comparison (TCP vs QUIC)', 'Protocol', 'Download Time (ms)', 'plots/download_time_comparison.png')

# Time to first byte comparison
plot_performance(combined_df, 'protocol', 'time_to_first_byte', 
                 'Time to First Byte Comparison (TCP vs QUIC)', 'Protocol', 'Time to First Byte (ms)', 'plots/time_to_first_byte_comparison.png')

plot_cdf_of_connection_times(combined_df, 'plots/connection_time_CDF.png')