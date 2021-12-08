#!/usr/bin/python3
import os
import re

containers = []
pids = []

std_out = os.popen('crictl ps')
lines = std_out.readlines()
std_out.close()
lines.pop(0) # Consume the header row

for line in lines:
    parts = re.split("\s{2,}", line)
    containers.append((parts[0], parts[4]))
    
for c in containers:
    std_out = os.popen(f'crictl inspect {c[0]} | grep /ns/ipc')
    lines = std_out.readlines()
    std_out.close()
    for line in lines:
        match = re.search(r'/proc/(\d+)/ns/ipc', line)
        pid = match.groups(1)[0]
        pids.append(pid)
        
for i in range(0, len(pids)):
    std_out = os.popen(f"nsenter -t {pids[i]} -n netstat -a --tcp --program")
    lines = std_out.readlines()
    std_out.close()
    print(f"Container {containers[i]} (pid {pids[i]} | entries: {len(lines)-2}):") # -2 accounts for header lines
    for line in lines:
        print(line, end='')
