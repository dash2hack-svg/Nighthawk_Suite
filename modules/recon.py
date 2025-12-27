import subprocess, time, os, sys
from core.ui import UI, C, W, R, G, B, NC, Y, D

class NetworkRecon:
    def __init__(self, interface="wlan1"):
        self.interface = interface

    def autonomous_scan(self, target_range="192.168.1.0/24"):
        """
        State-of-the-Art Autonomous Mapping.
        Uses Scapy for cross-platform hardware-agnostic discovery.
        """
        UI.print_box([f"AUTO-RECON: Probing {target_range}"], title="STATE MACHINE ACTION")
        
        try:
            from scapy.all import ARP, Ether, srp
        except ImportError:
            print(f"\n{R}[!] Error: Scapy library not installed.{NC}")
            print(f"{D}    Install it via: pip install scapy{NC}")
            return []

        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target_range), 
                         timeout=2, iface=self.interface, verbose=False)
            results = []
            for snd, rcv in ans:
                results.append([rcv.psrc, rcv.hwsrc, "Active"])
            
            if results:
                UI.draw_table(["IP ADDRESS", "MAC ADDRESS", "STATUS"], results)
            return results
        except Exception as e:
            print(f"{R}[!] Scapy Error: {e}{NC}")
            return []

    def run(self):
        """Interactive Recon Mode."""
        while True:
            UI.banner()
            UI.print_box(["1. ARP Discovery (LAN)", "2. Nmap Stealth (Target)", "3. Autonomous Evolution Mode", "4. Exit"], title="NETWORK RECON")
            
            c = input(f"\n {B}Select{NC} {C}»{NC} ")
            
            if c == '1':
                print(f"\n{C}[*] Mapping LAN...{NC}")
                if sys.platform == "linux":
                    try:
                        subprocess.run("arp-scan -l", shell=True, check=True)
                    except:
                        print(f"{Y}[!] arp-scan failed. Using fallback...{NC}")
                        os.system("netdiscover -r 192.168.1.0/24")
                else:
                    self.autonomous_scan() # Fallback for Windows/Mac
                input(f"\n{W}Press Enter...{NC}")

            elif c == '2':
                ip = input(f"\n{W}Target IP > {NC}")
                if ip: 
                    # Cross-platform check for Nmap
                    try:
                        os.system(f"nmap -sS -O -T4 {ip}")
                    except:
                        print(f"{R}[!] Nmap not found in PATH.{NC}")
                    input(f"\n{W}Press Enter...{NC}")

            elif c == '3':
                # Link to the new v62.0 Autonomous logic
                self.autonomous_scan()
                input(f"\n{W}Press Enter...{NC}")

            elif c == '4':
                break
