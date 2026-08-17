from flask import Flask, render_template_string, jsonify, request
import subprocess
import socket
import threading

app = Flask(__name__)

attacker = {"ip": None, "blocked": False, "detected": False}

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8888))
    sock.listen(10)
    print("👀 Listening on port 8888...")
    
    while True:
        try:
            conn, addr = sock.accept()
            src_ip = addr[0]
            print(f"📥 Connection from: {src_ip}")
            
            if src_ip != '127.0.0.1' and not attacker["detected"]:
                attacker["ip"] = src_ip
                attacker["detected"] = True
                print(f"⚠️ ATTACKER DETECTED: {src_ip}")
            
            conn.close()
        except:
            pass

threading.Thread(target=start_server, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Defender</title>
    <style>
        body { 
            background: linear-gradient(135deg, #0f0c29, #302b63); 
            color: white; display: flex; justify-content: center; 
            align-items: center; height: 100vh; margin: 0; font-family: sans-serif;
        }
        .box { text-align: center; padding: 50px; border-radius: 25px;
            background: rgba(255,255,255,0.1); backdrop-filter: blur(15px); }
        h1 { font-size: 3rem; }
        .status { padding: 25px; border-radius: 15px; margin: 20px 0; font-size: 1.5rem; }
        .safe { background: linear-gradient(135deg, #11998e, #38ef7d); }
        .danger { background: linear-gradient(135deg, #eb3349, #f45c43); animation: pulse 1s infinite; }
        .blocked { background: linear-gradient(135deg, #f2994a, #f2c94c); }
        @keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.02)} }
        .btn { padding: 18px 50px; font-size: 1.2rem; border: none; 
            border-radius: 50px; cursor: pointer; margin: 10px; font-weight: bold; }
        .block-btn { background: #c0392b; color: white; }
        .unblock-btn { background: #2980b9; color: white; }
        .ip { font-size: 2rem; color: #ff6b6b; font-weight: bold; }
        .hide { display: none; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🛡️ Network Defender</h1>
        <div id="status" class="status safe">✅ Network Secure</div>
        
        <div id="attacker" class="hide">
            <p>⚠️ <strong>ATTACKER DETECTED!</strong></p>
            <p>IP: <span id="attacker-ip" class="ip">-</span></p>
            <button class="btn block-btn" onclick="block()">🚫 BLOCK ATTACKER</button>
        </div>
        
        <div id="blocked" class="hide">
            <p style="font-size:4rem">🚫</p>
            <p><strong>ATTACKER BLOCKED!</strong></p>
            <p>Blocked IP: <span id="blocked-ip" class="ip">-</span></p>
            <button class="btn unblock-btn" onclick="unblock()">🔓 UNBLOCK</button>
        </div>
    </div>
    <script>
        function update() {
            fetch('/status').then(r => r.json()).then(d => {
                s=document.getElementById('status'); 
                a=document.getElementById('attacker'); 
                b=document.getElementById('blocked');
                
                if(d.blocked){
                    s.className='status blocked';
                    s.textContent='🚫 ATTACKER BLOCKED';
                    document.getElementById('blocked-ip').textContent=d.ip;
                    a.classList.add('hide');
                    b.classList.remove('hide');
                }
                else if(d.detected){
                    s.className='status danger';
                    s.textContent='⚠️ INTRUDER DETECTED!';
                    document.getElementById('attacker-ip').textContent=d.ip;
                    a.classList.remove('hide');
                    b.classList.add('hide');
                }
                else{
                    s.className='status safe';
                    s.textContent='✅ Network Secure';
                    a.classList.add('hide');
                    b.classList.add('hide');
                }
            });
        }
        function block(){fetch('/block',{method:'POST'})}
        function unblock(){fetch('/unblock',{method:'POST'})}
        setInterval(update,500);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/status')
def status():
    return jsonify(attacker)

@app.route('/block', methods=['POST'])
def block():
    if attacker["ip"]:
        subprocess.run(['netsh','advfirewall','firewall','add','rule','name=Block','dir=in','action=block','remoteip='+attacker["ip"]], check=False)
        attacker["blocked"] = True
    return jsonify({"ok":True})

@app.route('/unblock', methods=['POST'])
def unblock():
    if attacker["ip"]:
        subprocess.run(['netsh','advfirewall','firewall','delete','rule','name=Block'], check=False)
        attacker["blocked"] = False
    return jsonify({"ok":True})

if __name__ == '__main__':
    print("\n🌐 Browser: http://localhost:5000")
    print("🔍 Waiting for connections on port 8888...\n")
    app.run(host='0.0.0.0', port=5000, debug=False)