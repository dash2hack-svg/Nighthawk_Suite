import subprocess, sys, time, os, platform
from core.ui import UI, C, W, R, G, B, NC, Y, D

class HardwareSync:
    def __init__(self):
        self.os_type = platform.system().lower()

    def get_chipset(self, iface):
        """Cross-Platform Chipset Detection"""
        try:
            if self.os_type == "linux":
                cmd = f"ethtool -i {iface} | grep driver | awk '{{print $2}}'"
                return subprocess.check_output(cmd, shell=True).decode().strip() or "Generic"
            elif self.os_type == "windows":
                # Basic Windows Driver Check
                return "Windows WLAN Driver"
            elif self.os_type == "darwin":
                return "CoreWLAN (macOS)"
            return "Generic"
        except: return "Unknown"

    def get_bus_type(self, iface):
        """Determines if card is Internal (PCI) or External (USB)"""
        try:
            if self.os_type == "linux":
                path = subprocess.check_output(f"readlink -f /sys/class/net/{iface}/device", shell=True).decode()
                if "usb" in path: return "USB"
                if "pci" in path: return "PCI"
            # On Windows/Mac, we default to "External" to bypass the PCI block for testing
            return "EXTERNAL" 
        except: return "UNKNOWN"

    def get_all_interfaces(self):
        """OS-Agnostic Interface Discovery"""
        wifi_list = []
        if self.os_type == "linux":
            if os.path.exists('/sys/class/net'):
                for device in os.listdir('/sys/class/net'):
                    if os.path.isdir(f"/sys/class/net/{device}/wireless"):
                        wifi_list.append(device)
                    elif os.path.exists(f"/sys/class/net/{device}/phy80211"):
                        wifi_list.append(device)
        elif self.os_type == "windows":
            # Uses netsh to find interface names on Windows
            try:
                out = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
                import re
                wifi_list = re.findall(r"Name\s+:\s+(.*)", out)
            except: pass
        elif self.os_type == "darwin":
            # macOS discovery
            try:
                out = subprocess.check_output("networksetup -listallhardwareports", shell=True).decode()
                import re
                wifi_list = re.findall(r"Device:\s+(en\d+)", out)
            except: pass
            
        return [w.strip() for w in wifi_list]

    def force_awake(self, iface):
        """Platform-Specific Monitor Mode"""
        if self.os_type == "linux":
            subprocess.run(f"rfkill unblock wifi", shell=True)
            subprocess.run(f"ip link set {iface} down", shell=True)
            subprocess.run(f"iw dev {iface} set type monitor", shell=True)
            subprocess.run(f"ip link set {iface} up", shell=True)
            time.sleep(0.5)
        else:
            # Windows/Mac don't support native monitor mode switching via script easily
            pass

    def setup(self):
        UI.banner()
        UI.print_box(["SYSTEM PREP: Enforcing Hardware Standards..."], title="HARDWARE INITIALIZATION")
        
        # Only run airmon-ng on Linux
        if self.os_type == "linux":
            subprocess.run("airmon-ng check kill", shell=True, stdout=subprocess.DEVNULL)
        
        ifaces = self.get_all_interfaces()
        if not ifaces:
            print(f"{R}[!] FATAL: No Wireless Cards found.{NC}")
            if self.os_type == "windows":
                print(f"{D}    Ensure Wi-Fi is enabled and drivers are installed.{NC}")
            sys.exit()

        print(f"\n{C} [ DETECTED INTERFACES ]{NC}")
        valid = []
        for i, iface in enumerate(ifaces):
            chip = self.get_chipset(iface)
            bus = self.get_bus_type(iface)
            
            # Logic: Block PCI on Linux, Allow all on Windows/Mac for testing
            if bus == "PCI" and self.os_type == "linux":
                status = f"{R}[INTERNAL - BLOCKED]{NC}"
                color = D
            else:
                status = f"{G}[APPROVED]{NC}"
                color = G
                valid.append(i)

            print(f" {C}[{i}]{NC} {color}{iface:<20}{NC} {W}[{bus}]{NC} {D}:: {chip}{NC} {status}")

        if not valid:
            print(f"\n{R}[!] ERROR: No Injection-Capable cards detected.{NC}")
            sys.exit()

        target_idx = -1
        while target_idx not in valid:
            try: 
                val = input(f"\n {B}Select Interface ID{NC} {C}»{NC} ")
                target_idx = int(val)
            except ValueError: pass
        
        target = ifaces[target_idx]
        
        # Ask for frequency on all platforms
        print(f"\n{W} SELECT FREQUENCY FOR {target}{NC}")
        print(f" {C}1.{NC} 2.4GHz Only {D}(Standard){NC}")
        print(f" {C}2.{NC} Dual-Band   {D}(2.4GHz + 5GHz){NC}")
        
        mode = input(f"\n {B}Mode{NC} {C}»{NC} ")
        bands = "abg" if mode == '2' else "bg"
        
        UI.print_box([f"TARGET: {target}", "ACTION: Monitor Mode Initialization"], title="CONFIGURING HARDWARE")
        self.force_awake(target)
        
        return target, bands
