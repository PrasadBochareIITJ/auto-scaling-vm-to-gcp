# Auto-Scaling Compute Resources with Local VM and GCP

This project demonstrates a real-world use case of local-to-cloud auto-scaling. A lightweight Alpine Linux VM monitors its own CPU and RAM usage. When resource usage exceeds a defined threshold (75%), the system automatically triggers the launch of a more powerful virtual machine on Google Cloud Platform (GCP).

---

## Features

- Lightweight Alpine VM created using VirtualBox
- Real-time resource monitoring via Python
- Matrix-based CPU load simulation
- Host-side trigger script using SSH and GCP CLI
- GCP instance starts only when needed
- Automated cleanup after scale-up (CPU load stopped)

---

## Architecture Overview

```
+-----------------------+      SSH + monitor.py       +------------------------+
|     Windows Host      | -------------------------> |   Alpine Linux VM       |
| (trigger_gcp_vm.py)   |                             |   (monitor + load app)  |
+-----------------------+                             +-----------+------------+
                                                              |
                                            CPU > 75%         |
                                                              v
                                                    +---------+----------+
                                                    | GCP VM Instance    |
                                                    | Auto-start via CLI |
                                                    +--------------------+
```

---

## Setup

### 1. Local VM

- Install VirtualBox and create an Alpine Linux VM
- Enable SSH and Python3
- Use `scp` to transfer scripts

### 2. GCP Configuration

- Create a VM named `my-vm-instance` in `us-central1-c`
- Install and configure Google Cloud SDK
- Authenticate using `gcloud init`

---

## File Structure

```
.
├── monitor.py              # Runs inside Alpine, monitors CPU & RAM
├── matrix_cpu_load.py      # Simulates CPU load (NumPy matrix loop)
├── trigger_gcp_vm.py       # Host-side trigger and auto-scale logic
```

---

## Demo Instructions

1. **Start CPU load remotely**:
   ```bash
   ssh root@<VM-IP> "nohup python3 ~/matrix_cpu_load.py > /dev/null 2>&1 &"
   ```

2. **Run auto-scale trigger**:
   ```bash
   python trigger_gcp_vm.py
   ```

3. **Watch GCP Console**:
   - Navigate to Compute Engine > VM Instances
   - Observe `my-vm-instance` change from `TERMINATED` to `RUNNING`

4. **Stop GCP VM after demo**:
   ```bash
   gcloud compute instances stop my-vm-instance --zone=us-central1-c
   ```

---

## Example Output

```
CPU Usage: 92.7%
RAM Usage: 40.5%
Triggering GCP scale-up...
✅ GCP VM started
✅ Matrix CPU load stopped
```

---


