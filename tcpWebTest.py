import subprocess
import time
import os

iterations = 5
website_file = 'config/websites.txt'
log_file = 'data/Webtimestamp.log'

# Clear the log file at the start of each run
if os.path.exists(log_file):
    open(log_file, 'w').close()

websites = []
# Read websites from file
with open(website_file, 'r') as f:
    websites = [line.strip() for line in f if line.strip()]
    
# Run tests
for website in websites:
    for i in range(iterations):
        subprocess.run(['./tcpWebTestIndividual.sh', website], shell=False)
        time.sleep(1)
