import os
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
import subprocess
import socket
from flask import Flask, render_template, jsonify, request

# Absolute path resolution for templates and static folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../templates"))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../static"))

if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "templates"))
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "static"))

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Safe Scapy import for cloud serverless compatibility
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, Ether, srp
    SCAPY_AVAILABLE = True
except Exception as e:
    print("Scapy not available in cloud environment, using simulated packet mode:", e)
    SCAPY_AVAILABLE = False

# ---------------- CONFIG ----------------
TIME_WINDOW = 5
SCAN_THRESHOLD = 10
FLOOD_THRESHOLD = 100
ICMP_THRESHOLD = 20

local_ip = "192.168.1.10"

# ---------------- STATE ----------------
state_lock = threading.Lock()
traffic_data = defaultdict(list)
icmp_data = defaultdict(list)
udp_data = defaultdict(list)

detected_attackers = {
    "192.168.1.45": {
        "type": "Port Scan",
        "count": 14,
        "first_seen": "20:15:02",
        "last_seen": "20:18:44"
    },
    "10.0.0.88": {
        "type": "SYN Flood",
        "count": 105,
        "first_seen": "20:20:11",
        "last_seen": "20:22:19"
    }
}
alerts = [
    {"time": "20:15:02", "ip": "192.168.1.45", "type": "Port Scan", "detail": "Target Port 80, 443, 22, 8080"},
    {"time": "20:20:11", "ip": "10.0.0.88", "type": "SYN Flood", "detail": "High frequency SYN packets detected"}
]

# ---------------- NETWORK ALERT ----------------
def send_network_alert(msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(msg.encode(), ("255.255.255.255", 9999))
        s.close()
    except Exception:
        pass

# ---------------- BLOCK ----------------
def block_ip(ip):
    try:
        subprocess.run([
            "netsh", "advfirewall", "firewall",
            "add", "rule",
            f"name=Block_{ip}",
            "dir=in", "action=block",
            f"remoteip={ip}"
        ], check=False)
        print("BLOCKED:", ip)
    except Exception:
        pass

def unblock_ip(ip):
    try:
        subprocess.run([
            "netsh", "advfirewall", "firewall",
            "delete", "rule",
            f"name=Block_{ip}"
        ], check=False)
    except Exception:
        pass

# ---------------- ALERT ----------------
def add_alert(ip, typ, detail):
    now = datetime.now().strftime("%H:%M:%S")
    with state_lock:
        if ip not in detected_attackers:
            detected_attackers[ip] = {
                "type": typ,
                "count": 1,
                "first_seen": now,
                "last_seen": now
            }
            block_ip(ip)
            send_network_alert(f"⚠️ ATTACKER: {ip}")
        else:
            detected_attackers[ip]["count"] += 1
            detected_attackers[ip]["last_seen"] = now
            detected_attackers[ip]["type"] = typ

        alerts.append({
            "time": now,
            "ip": ip,
            "type": typ,
            "detail": detail
        })

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify({
        "attackers": [{"ip": ip, **d} for ip, d in detected_attackers.items()],
        "alerts": alerts[-50:]
    })

@app.route("/block/<ip>", methods=["POST"])
def block(ip):
    block_ip(ip)
    add_alert(ip, "Manual Block", "Administrator blocked IP")
    return jsonify({"ok": True})

@app.route("/unblock/<ip>", methods=["POST"])
def unblock(ip):
    unblock_ip(ip)
    with state_lock:
        if ip in detected_attackers:
            del detected_attackers[ip]
    return jsonify({"ok": True})

@app.route("/network")
def network():
    return jsonify([
        {"ip": "192.168.1.1", "mac": "00:11:22:33:44:55"},
        {"ip": "192.168.1.10", "mac": "AA:BB:CC:DD:EE:FF"},
        {"ip": "192.168.1.45", "mac": "12:34:56:78:90:AB"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
