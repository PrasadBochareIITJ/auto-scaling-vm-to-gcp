# trigger_gcp_vm.py
# This script connects to Alpine VM, checks CPU/RAM via monitor.py,
# and starts a GCP VM if usage exceeds 75%. It also stops the CPU load afterward.

import paramiko              # For SSH into Alpine VM
import subprocess            # For calling gcloud CLI from Windows

# ---------------------------
# SSH Credentials for Alpine VM
# ---------------------------
host = "192.168.56.110"      # Alpine VM IP
user = "root"                # Alpine VM username
password = "alpine123"       # Alpine VM password

# ---------------------------
# Remote command to run monitor script in VM
# ---------------------------
monitor_command = "python3 ~/monitor.py"

# ---------------------------
# Remote command to stop matrix CPU load script in VM
# ---------------------------
stop_load_command = "pkill -f matrix_cpu_load.py"

# ---------------------------
# Function to run monitor.py remotely and collect CPU/RAM
# ---------------------------
def run_remote_monitor():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)

        stdin, stdout, stderr = client.exec_command(monitor_command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        client.close()
        return output, error

    except Exception as e:
        return None, f"VM Error: {str(e)}"

# ---------------------------
# Function to stop matrix load on Alpine VM
# ---------------------------
def stop_cpu_load():
    print("Stopping matrix load in Alpine VM...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)
        client.exec_command(stop_load_command)
        client.close()
        print("✅ CPU load stopped.")
    except Exception as e:
        print(f"Error stopping CPU load: {str(e)}")

# ---------------------------
# Function to trigger GCP scale-up
# ---------------------------
def trigger_gcp_scale_up():
    print("Triggering GCP scale-up...")
    try:
        result = subprocess.run(
            "gcloud compute instances start my-vm-instance --zone=us-central1-c",
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True  # Required for Windows PATH commands like gcloud
        )
        print("✅ GCP VM started:\n", result.stdout.decode())
    except FileNotFoundError:
        print("❌ gcloud not found. Is Google Cloud SDK installed and added to PATH?")
    except subprocess.CalledProcessError as e:
        print("❌ GCP start failed:\n", e.stderr.decode())

# ---------------------------
# Main Execution
# ---------------------------
output, error = run_remote_monitor()

print("\n--- Alpine VM Resource Report ---\n")
if error:
    print("Error:", error)
else:
    print(output)

    try:
        # Parse CPU and RAM usage lines
        lines = output.splitlines()
        cpu_line = next((line for line in lines if "CPU Usage" in line), None)
        ram_line = next((line for line in lines if "RAM Usage" in line), None)

        cpu = float(cpu_line.split(":")[1].strip().replace("%", ""))
        ram = float(ram_line.split(":")[1].strip().replace("%", ""))

        print(f"\nParsed Values → CPU: {cpu}%, RAM: {ram}%")

        # Trigger GCP if threshold exceeded
        if cpu > 75 or ram > 75:
            trigger_gcp_scale_up()
            stop_cpu_load()
        else:
            print("No scaling needed. Usage is normal.")

    except Exception as parse_error:
        print(f"❌ Parsing failed: {parse_error}")
