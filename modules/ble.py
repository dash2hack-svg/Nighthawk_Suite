import subprocess, os, time, sys
from core.ui import UI, C, W, R, G, B, NC, Y, D

class BLEAttack:
    def __init__(self, proj_dir):
        self.path = proj_dir
        self.targets = []

    def scan_ble(self):
        UI.banner()
        print(f"{C}[*] Scanning for Bluetooth Low Energy devices...{NC}")
        
        # Windows/Mac Safety Check
        if sys.platform != "linux":
            return f"\n{Y}[!] BLE Scanning requires Linux BlueZ stack (hcitool).{NC}\n{D}    Feature unavailable on current OS.{NC}"

        try:
            # Linux Native Scan
            cmd = "sudo hcitool lescan --duplicates --timeout=10"
            output = subprocess.check_output(cmd, shell=True).decode()
            return output
        except Exception as e:
            return str(e)

    def run(self):
        results = self.scan_ble()
        
        if "Unavailable" in results:
            print(results)
            input(f"\n{W}Press Enter to return...{NC}")
            return

        if "Device or resource busy" in results:
            reason = "Bluetooth Interface (hci0) is locked."
            advice = "Run 'sudo hciconfig hci0 reset' and try again."
        elif not results or len(results) < 10:
            reason = "No BLE advertisements detected."
            advice = "Target may be out of range."
        else:
            print(results)
            input(f"\n{G}[+] Scan Complete.{NC} Press Enter...")
            return

        UI.print_box([
            f"{R}BLE MISSION FAILED{NC}",
            f"REASON: {reason}",
            f"ADVICE: {advice}"
        ], title="SIGNAL REPORT")
        
        input(f"\n{W}Press Enter to return to menu...{NC}")
