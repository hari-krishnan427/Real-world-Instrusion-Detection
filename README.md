# 📡 Real-World Network Intrusion Detection System (IDS)

An active, real-time **Network Intrusion Detection & Prevention System (NIDPS)** built with **Python**, **Scapy**, **Flask**, and **Windows Firewall Automation**. Features live packet inspection, automated threat mitigation, firewall IP blocking, and an interactive web monitoring dashboard.

---

## 📁 Architecture Overview

```
Real-world-Intrusion-Detection/
├── backend/                        # Real-Time IDS Engine & REST API
│   └── app.py                      # Multi-threaded packet sniffer, detection rules & firewall blocker
├── templates/                      # Monitoring Dashboard UI
│   └── index.html                  # Real-time threat matrix & live network feed
├── requirements.txt                # Dependencies (Flask, Scapy, etc.)
├── .gitignore
└── README.md
```

---

## 🛠️ Key Capabilities

- **Real-Time Packet Inspection**: Sniffs TCP, UDP, ICMP, ARP, and Ether packets asynchronously.
- **Automated Threat Detection Engine**:
  - **Port Scanning**: Detects SYN scans and NULL/FIN stealth scans.
  - **DoS & Flooding**: Detects SYN flooding and ICMP ping sweeps exceeding defined packet thresholds.
- **Automated Active Defense**: Automatically injects Windows Firewall rules (`netsh advfirewall`) to block malicious attacker IPs instantly.
- **Interactive Security Dashboard**: Live updating matrix of active threats, IP block lists, and network devices.

---

## 🚀 Setup & Execution

### 1. Prerequisites
- Python 3.9+
- Npcap (on Windows) or libpcap (on Linux) for Scapy raw packet sniffing.
- Administrative / Root privileges (required for packet capturing and firewall manipulation).

### 2. Installation & Running

Navigate to the project root and install requirements:
```bash
pip install -r requirements.txt
```

Launch the NIDS engine with administrative privileges:
```bash
python backend/app.py
```

Access the Live Dashboard at `http://localhost:5000`.
