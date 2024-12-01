import re
import pandas as pd

# Define a function to parse log data from .txt file and convert it into a pandas DataFrame
def parse_log_to_dataframe(log_file):
    # Initialize lists to hold the parsed data
    workloads = []
    time_to_first_byte = []
    connection_time = []
    total_time = []
    
    # Open and read the log file
    with open(log_file, 'r') as file:
        # Read the content line by line
        lines = file.readlines()
        
        # Define regex patterns for extracting values
        workload_pattern = re.compile(r"Workload: (\w+)")
        time_pattern = re.compile(r"Time to First Byte: ([\d\.]+)s")
        conn_pattern = re.compile(r"Connection Time: ([\d\.]+)s")
        total_pattern = re.compile(r"Total Time: ([\d\.]+)s")
        
        # Temporary variables to hold the parsed values
        workload = None
        for i in range(0, len(lines), 4):  # Iterate in steps of 4 lines (Workload + 3 metrics)
            # Ensure we have at least 4 lines to read
            if i + 3 < len(lines):
                workload_match = workload_pattern.search(lines[i])
                time_match = time_pattern.search(lines[i + 1])
                conn_match = conn_pattern.search(lines[i + 2])
                total_match = total_pattern.search(lines[i + 3])

                # If all necessary fields are found, append the values to the lists
                if workload_match and time_match and conn_match and total_match:
                    workload = workload_match.group(1)
                    workloads.append(workload)
                    time_to_first_byte.append(float(time_match.group(1)) * 1000)  # Convert to milliseconds
                    connection_time.append(float(conn_match.group(1)) * 1000)  # Convert to milliseconds
                    total_time.append(float(total_match.group(1)) * 1000)  # Convert to milliseconds

    # Create a pandas DataFrame from the parsed data
    df = pd.DataFrame({
        'workload': workloads,
        'time_to_first_byte': time_to_first_byte,
        'connection_time': connection_time,
        'total_time': total_time
    })

    return df

# Parse both tcp and quic log files
tcp_df = parse_log_to_dataframe('logs/tcp_log.txt')
quic_df = parse_log_to_dataframe('logs/quic_log.txt')

# Save the individual DataFrames to CSV files
tcp_df.to_csv('tcp_log_data.csv', index=False)
quic_df.to_csv('quic_log_data.csv', index=False)

print("TCP and QUIC log data have been successfully converted to CSV!")
