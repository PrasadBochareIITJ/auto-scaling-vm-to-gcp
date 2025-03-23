# monitor.py
# This script reads CPU and RAM usage from the Alpine Linux system and prints it

import time

# Function to read CPU usage from /proc/stat
def get_cpu_usage():
    # First snapshot
    with open("/proc/stat", "r") as f:
        cpu_line = f.readline()
    cpu_parts = list(map(int, cpu_line.strip().split()[1:]))
    idle1 = cpu_parts[3]
    total1 = sum(cpu_parts)

    # Wait 0.5 second before next snapshot
    time.sleep(0.5)

    # Second snapshot
    with open("/proc/stat", "r") as f:
        cpu_line2 = f.readline()
    cpu_parts2 = list(map(int, cpu_line2.strip().split()[1:]))
    idle2 = cpu_parts2[3]
    total2 = sum(cpu_parts2)

    # Calculate CPU usage percentage
    idle_delta = idle2 - idle1
    total_delta = total2 - total1
    usage_percent = 100 * (1 - idle_delta / total_delta)
    return round(usage_percent, 1)

# Function to read RAM usage from /proc/meminfo
def get_ram_usage():
    with open("/proc/meminfo", "r") as f:
        lines = f.readlines()
    mem_total = int([line for line in lines if "MemTotal" in line][0].split()[1])
    mem_available = int([line for line in lines if "MemAvailable" in line][0].split()[1])
    usage_percent = 100 * (1 - (mem_available / mem_total))
    return round(usage_percent, 1)

# Run both functions and print the results
if __name__ == "__main__":
    cpu = get_cpu_usage()
    ram = get_ram_usage()
    print(f"CPU Usage: {cpu}%")
    print(f"RAM Usage: {ram}%")
