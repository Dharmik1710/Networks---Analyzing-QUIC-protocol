import re

log_file = 'data/Webtimestamp.log'
# For QUIC
# result_file = 'data/quicWebResult.log'
# For TCP
result_file = 'data/tcpWebResult.log'

# Data storage for averages
times = {}

# Parse the log file
with open(log_file, 'r') as file:
    for line in file:
        match = re.match(r"(.*) : Connection Time=(\d+)ms, TTFB=(\d+\.\d+)ms, Total Download Time=(\d+\.\d+)ms", line)
        if match:
            website, conn_time, ttfb, total_time = match.groups()
            conn_time, ttfb, total_time = int(conn_time), float(ttfb), float(total_time)
            
            if website not in times:
                times[website] = {"conn_time": [], "ttfb": [], "total_time": []}
                
            times[website]["conn_time"].append(conn_time)
            times[website]["ttfb"].append(ttfb)
            times[website]["total_time"].append(total_time)

# Calculate averages and write to result file
with open(result_file, 'w') as result:
    result.write("Website,AvgConnectionTime(ms),AvgTTFB(ms),AvgTotalDownloadTime(ms)\n")
    for website, metrics in times.items():
        avg_conn_time = sum(metrics["conn_time"]) / len(metrics["conn_time"])
        avg_ttfb = sum(metrics["ttfb"]) / len(metrics["ttfb"])
        avg_total_time = sum(metrics["total_time"]) / len(metrics["total_time"])
        
        result.write(f"{website},{avg_conn_time:.2f},{avg_ttfb:.2f},{avg_total_time:.2f}\n")

print("Averages have been calculated and written to", result_file)
