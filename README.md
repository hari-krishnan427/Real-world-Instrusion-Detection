# 📡 Nighthawk IDS — Real-World Network Intrusion Detection System

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Vercel-black?style=for-the-badge&logo=vercel)](https://real-world-intrusion-detection.vercel.app)
[![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=for-the-badge&logo=python)](https://flask.palletsprojects.com)
[![Scapy](https://img.shields.io/badge/Network-Scapy-red?style=for-the-badge)](https://scapy.net)

An active, real-time **Network Intrusion Detection & Prevention System (NIDPS)** featuring live packet inspection, automated threat mitigation, host tracking, firewall rule injection, and an interactive cybersecurity matrix dashboard.

🔗 **Live Web Dashboard:** [https://real-world-intrusion-detection.vercel.app](https://real-world-intrusion-detection.vercel.app)

---

## 📁 Architecture Overview

```
Real-world-Intrusion-Detection/
├── backend/                        # Real-Time IDS Engine & REST API
│   └── app.py                      # Multi-threaded packet sniffer, detection rules & firewall blocker
├── templates/                      # Monitoring Dashboard UI
│   └── index.html                  # Real-time threat matrix & live network feed
├── vercel.json                     # Vercel Deployment Config
├── requirements.txt                # Dependencies (Flask, Scapy, etc.)
├── .gitignore
└── README.md
```

---

## 🛠️ Key Capabilities

- ⚡ **Real-Time Packet Inspection**: Sniffs TCP, UDP, ICMP, ARP, and Ether packets asynchronously.
- 🎯 **Automated Threat Engine**:
  - **Port Scanning**: Detects SYN scans and NULL/FIN stealth scans.
  - **DoS & Flooding**: Detects SYN flooding and ICMP ping sweeps exceeding defined packet thresholds.
- 🛡️ **Automated Active Defense**: Automatically injects firewall rules to block malicious attacker IPs instantly.
- 📊 **Cybersecurity Dashboard**: Interactive matrix displaying threat distribution, local network nodes, traffic anomalies, and active IP blocklists.

---

## 🚀 Setup & Execution

### 1. Live Cloud Web Dashboard
Visit the live dashboard on Vercel: [https://real-world-intrusion-detection.vercel.app](https://real-world-intrusion-detection.vercel.app)

### 2. Local Real-Time Packet Sniffing Mode
```bash
git clone https://github.com/hari-krishnan427/Real-world-Intrusion-Detection.git
cd Real-world-Intrusion-Detection
pip install -r requirements.txt
python backend/app.py
```
Access the local monitoring dashboard at `http://localhost:5000`.
