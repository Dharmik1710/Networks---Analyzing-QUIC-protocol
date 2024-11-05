# Networks---Analyzing-QUIC-protocol
Reproducing the results from paper "Evaluating QUIC Performance Over Web, Cloud Storage, and Video Workloads"


# TO-DO List

## Team Members
- **Member 1**: [Name]
- **Member 2**: [Name]
- **Member 3**: [Name]
- **Member 4**: [Name]
- **Member 5**: [Name]
- **Member 6**: [Name]

---

## Project Overview
This project aims to reproduce the results from *Evaluating QUIC Performance Over Web, Cloud Storage, and Video Workloads*. The experiments will assess QUIC’s performance across web, cloud storage, and video workloads, comparing it to TLS/TCP. Below is the task breakdown.

---

### 1. **Project Setup**
- [ ] **Set up repositories**: Create GitHub repository, structure folders for `scripts`, `data`, `results`, and `documentation`.
  - **Assigned to**: Member 1
- [ ] **Install dependencies**: Set up required libraries (`lsquic`, `libcurl`, etc.) and document setup instructions in `README.md`.
  - **Assigned to**: Member 2
- [ ] **Network Configuration**: Ensure setup for both low-latency and high-latency networks. Use emulation tools if necessary.
  - **Assigned to**: Member 3 and Member 4

---

### 2. **Experiment Development**
- [ ] **Web Workloads Experiment (quic_perf and tls_perf)**
  - [ ] Configure `quic_perf` and `tls_perf` to measure connection times, TTFB, and download times for selected websites.
  - [ ] Create sample data collection script to test configurations.
  - **Assigned to**: Member 1 and Member 2

- [ ] **Cloud Storage Workloads Experiment**
  - [ ] Configure file download experiments over Google Drive with `quic_perf` and `tls_perf`.
  - [ ] Set up file size variations and script to automatically record throughput and CPU usage.
  - **Assigned to**: Member 3 and Member 4

- [ ] **Video Workloads Experiment (video_download and video_streaming)**
  - [ ] Configure `video_download` test to measure connection times, throughput, and stall events.
  - [ ] Configure `video_streaming` with adaptive streaming to record QoE metrics (e.g., startup delay, stalls, quality switches).
  - **Assigned to**: Member 5 and Member 6

---

### 3. **Data Collection and Logging**
- [ ] **Automated Data Collection**: Create scripts to automate data collection and ensure periodic execution (e.g., every 3 hours).
  - **Assigned to**: Member 1 and Member 2
- [ ] **Network Loss Simulation**: Implement packet loss simulation using `tc` utility for video streaming tests and log results for each loss level.
  - **Assigned to**: Member 3 and Member 5
- [ ] **Log Processing**: Write scripts to clean and format log files for further analysis.
  - **Assigned to**: Member 6

---

### 4. **Data Analysis and Visualization**
- [ ] **Statistical Analysis**: Perform CDF analysis on connection times, TTFB, download times, and stall durations.
  - **Assigned to**: Member 4 and Member 5
- [ ] **Visualization**: Create CDF plots, throughput comparison charts, and stall duration graphs.
  - **Assigned to**: Member 3 and Member 6
- [ ] **Flame Graphs for CPU Usage**: Generate flame graphs for CPU utilization in different workloads.
  - **Assigned to**: Member 2 and Member 5

---

### 5. **Documentation**
- [ ] **Experiment Guide**: Document steps for each experiment, including commands and configurations.
  - **Assigned to**: Member 1
- [ ] **Data Analysis Report**: Summarize findings for each workload with graphs and statistical insights.
  - **Assigned to**: Member 6
- [ ] **Project Report**: Create a final report summarizing methodology, results, and conclusions.
  - **Assigned to**: Member 5

---

### 6. **Final Review and Submission**
- [ ] **Review Code and Documentation**: Conduct a team review session to finalize code and documentation.
  - **Assigned to**: All Members
- [ ] **Submit Results and Code**: Package results, code, and documentation for submission.
  - **Assigned to**: Member 1

---

### Optional Tasks
- [ ] **Automate Kernel Version Check**: Verify if the latest kernel updates support QUIC enhancements.
  - **Assigned to**: Member 4
- [ ] **Explore Additional QUIC Versions**: If time permits, test additional versions of QUIC for extended results.
  - **Assigned to**: Member 2 and Member 3

---

**Note**: Each member should update their task status on GitHub to reflect progress.
