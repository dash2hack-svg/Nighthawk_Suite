#!/usr/bin/env python3
import os, sys, subprocess, time, shutil
from pathlib import Path

# v62.0 Path Standardization
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from core.hardware import HardwareSync
from core.ui import UI, C, W, B, NC, R, G, Y, D
from core.config import load_config, save_config

# Import All Engines
from modules.encryption import EncryptionAttack
from modules.cracking import HandshakeCracker
from modules.bluetooth import BluetoothAttack
from modules.recon import NetworkRecon
from modules.loot import LootManager
from modules.ble import BLEAttack
from modules.evil_twin import EvilTwin
from modules.enterprise import EnterpriseAttack

class Nighthawk:
    def __init__(self):
        # Universal Path Handling (Windows/Mac/Linux safe)
        self.proj_dir = Path.home() / "Nighthawk_Suite" / "Loot"
        self.proj_dir.mkdir(parents=True, exist_ok=True)
        
        self.hw = HardwareSync()
        self.iface = None
        self.bands = "bg"
        self.config = load_config()

    def check_admin(self):
        """Cross-Platform Root/Admin Check"""
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def clean_input(self):
        """Cross-Platform Input Flush"""
        try:
            import msvcrt
            while msvcrt.kbhit(): msvcrt.getch()
        except ImportError:
            import termios, tty
            sys.stdin.flush()
        except: pass

    def safe_exec(self, func):
        try: func()
        except KeyboardInterrupt: pass
        except Exception as e: print(f"\n{R}[!] Error: {e}{NC}"); time.sleep(2)

    def check_dependencies(self):
        # Platform-Specific Toolchain Verification
        tools = ["nmap"]
        if sys.platform == "linux":
            # Added hostapd and dnsmasq for Evil Twin support
            tools.extend(["aircrack-ng", "airodump-ng", "macchanger", "hcitool", "hostapd", "dnsmasq"])
        
        missing = [t for t in tools if not shutil.which(t)]
        if missing and sys.platform == "linux":
            print(f"\n{Y}[!] Installing Missing Tools: {', '.join(missing)}{NC}")
            subprocess.run(f"sudo apt update && sudo apt install -y {' '.join(missing)}", shell=True)

    def main_menu(self):
        if self.config.get("handle") == "UNKNOWN OPERATOR":
             save_config("dash")
             self.config = load_config()

        while True:
            UI.banner()
            
            # Dynamic Status Indicator
            iface_display = f"{G}{self.iface}{NC}" if self.iface else f"{R}DISCONNECTED{NC}"
            
            # Bluetooth Mode Detection
            bt_mode = "Classic" if sys.platform == "linux" else "BLE-Only"

            UI.print_box([
                f"OPERATOR  : {self.config.get('handle')}",
                f"INTERFACE : {iface_display}",
                f"BAND MODE : {self.bands.upper()}"
            ], title="v62.0 OPERATIONAL STATUS")
            
            print(f"\n{C} [ AUTONOMOUS DOMAINS ]{NC}")
            print(f" {C}1.{NC} {W}Wireless Warfare{NC}     {D}:: God Mode & Kill Chain{NC}")
            print(f" {C}2.{NC} {W}Bluetooth Arsenal{NC}    {D}:: {bt_mode} Scanning & Jamming{NC}")
            print(f" {C}3.{NC} {W}Network Recon{NC}        {D}:: LAN Mapping & OS Detection{NC}")
            print(f" {C}4.{NC} {W}Offline War Room{NC}     {D}:: Hashcat & Bruteforce{NC}")
            print(f" {C}5.{NC} {W}Loot Repository{NC}      {D}:: HTML Reports & Captures{NC}")
            print(f" {C}6.{NC} {W}Evil Twin Attack{NC}     {D}:: Phishing & Captive Portal{NC}")
            print(f" {C}7.{NC} {W}Enterprise WPE{NC}       {D}:: RADIUS/MGT Harvest{NC}")
            print(f" {C}8.{NC} {Y}Re-Arm Hardware{NC}      {D}:: Switch Wi-Fi Card / Mode{NC}")
            print(f" {C}9.{NC} {W}System Exit{NC}          {D}:: Restore & Shutdown{NC}")
            
            try: c = input(f"\n {B}nighthawk{NC} {C}»{NC} ").strip()
            except EOFError: continue
            
            if c == '1':
                def launch():
                    if not self.iface: self.iface, self.bands = self.hw.setup()
                    EncryptionAttack(self.iface, self.bands, self.proj_dir).run()
                self.safe_exec(launch)
            elif c == '2': 
                # Smart Switching for Bluetooth Modules
                if sys.platform == "linux":
                    self.safe_exec(BluetoothAttack().run)
                else:
                    self.safe_exec(BLEAttack(self.proj_dir).run)
            elif c == '3': 
                if self.iface and "mon" in self.iface and sys.platform == "linux":
                    print(f"\n{R}[!] Interface in Monitor Mode. Connect to LAN first.{NC}"); time.sleep(2)
                else: 
                    self.safe_exec(NetworkRecon(self.iface).run)
            elif c == '4': self.safe_exec(lambda: HandshakeCracker(self.proj_dir).run())
            elif c == '5': self.safe_exec(lambda: LootManager(self.proj_dir).run())
            elif c == '6':
                def launch_et():
                    if not self.iface: self.iface, self.bands = self.hw.setup()
                    EvilTwin(self.iface, self.proj_dir).launch()
                self.safe_exec(launch_et)
            elif c == '7':
                def launch_ent():
                    if not self.iface: self.iface, self.bands = self.hw.setup()
                    EnterpriseAttack(self.iface, self.proj_dir).launch()
                self.safe_exec(launch_ent)
            elif c == '8':
                self.iface = None; self.hw.setup()
            elif c == '9': 
                print(f"\n{Y}[*] Shutting down Nighthawk Autonomous Suite...{NC}")
                sys.exit()

    def run(self):
        if sys.platform == "linux":
            os.system("xhost +local:root > /dev/null 2>&1")
        self.check_dependencies()
        try: self.main_menu()
        except KeyboardInterrupt: sys.exit()

if __name__ == "__main__":
    app = Nighthawk()
    if not app.check_admin():
        print(f"{R}[!] FATAL: Administrator/Root privileges required.{NC}")
        if sys.platform == "win32":
            print(f"{D}    Right-click -> Run as Administrator{NC}")
        else:
            print(f"{D}    Try: sudo python3 nighthawk.py{NC}")
        sys.exit(1)
    app.run()
