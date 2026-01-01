import subprocess
import time
import os
import sys
import shutil

from core.ui import UI, C, W, R, G, B, NC, Y, D


class NetworkRecon:
    def __init__(self, interface="wlan1"):
        """
        NetworkRecon: Safe, interactive network reconnaissance helper.

        interface: Network interface to use for ARP/Scapy-based discovery
                   where applicable (primarily on Linux).
        """
        self.interface = interface

    def _authorized_use_notice(self):
        """
        Print a brief reminder about authorized use and scope.

        Called at the start of recon mode to set expectations.
        """
        UI.print_box(
            [
                "This module is intended for authorized network assessment only.",
                "Use it only on networks and systems you own or have explicit",
                "written permission to test. Misuse may be illegal.",
            ],
            title="SCOPE & AUTHORIZATION",
        )
        time.sleep(1.5)

    def autonomous_scan(self, target_range="192.168.1.0/24"):
        """
        ARP-based LAN discovery using Scapy.

        Tries to map active hosts on the given target_range using ARP.
        Primarily useful for local subnet mapping on LANs.
        """
        UI.print_box(
            [f"Probing local range: {target_range}"],
            title="ARP DISCOVERY (SCAPY)",
        )

        try:
            from scapy.all import ARP, Ether, srp
        except ImportError:
            print(f"\n{R}[!] Error: Scapy library not installed.{NC}")
            print(f"{D}    Install it via: pip install scapy{NC}")
            return []

        try:
            ans, _ = srp(
                Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_range),
                timeout=2,
                iface=self.interface,
                verbose=False,
            )
            results = []
            for snd, rcv in ans:
                results.append([rcv.psrc, rcv.hwsrc, "Active"])

            if results:
                UI.draw_table(["IP ADDRESS", "MAC ADDRESS", "STATUS"], results)
            else:
                print(f"\n{Y}[!] No active hosts discovered in range.{NC}")
            return results
        except Exception as e:
            print(f"{R}[!] Scapy Error: {e}{NC}")
            return []

    def _run_arp_scan_linux(self):
        """
        Linux ARP scan using system tools (arp-scan or netdiscover).
        """
        print(f"\n{C}[*] Mapping LAN using system tools...{NC}")

        # Prefer arp-scan if available
        if shutil.which("arp-scan"):
            try:
                subprocess.run(
                    ["arp-scan", "-l"],
                    check=False,
                )
                return
            except Exception as e:
                print(f"{Y}[!] arp-scan encountered an issue: {e}{NC}")

        # Fallback to netdiscover if available
        if shutil.which("netdiscover"):
            try:
                # Defaulting to a common private range; user can refine later
                os.system("netdiscover -r 192.168.1.0/24")
                return
            except Exception as e:
                print(f"{Y}[!] netdiscover encountered an issue: {e}{NC}")

        print(
            f"{R}[!] No supported ARP scan tools found "
            f"(arp-scan / netdiscover).{NC}"
        )

    def _run_nmap_scan(self, ip):
        """
        Run a basic Nmap scan (if available) against a target IP.
        """
        if not ip:
            print(f"{Y}[!] No target provided.{NC}")
            return

        if not shutil.which("nmap"):
            print(f"{R}[!] Nmap not found in PATH.{NC}")
            print(f"{D}    Install it or adjust your PATH to use this feature.{NC}")
            return

        print(f"\n{C}[*] Running Nmap scan against {ip}...{NC}")
        try:
            # -sS (SYN scan), -O (OS detection), -T4 (faster timing)
            os.system(f"nmap -sS -O -T4 {ip}")
        except Exception as e:
            print(f"{R}[!] Nmap encountered an error: {e}{NC}")

    def run(self):
        """
        Interactive Recon Mode.

        Provides:
        1. LAN discovery (ARP-based)
        2. Targeted host scanning via Nmap
        3. Scapy-based ARP discovery
        """
        # One-time authorization reminder when entering recon mode
        self._authorized_use_notice()

        while True:
            UI.banner()
            UI.print_box(
                [
                    "1. ARP Discovery (LAN)",
                    "2. Nmap Scan (Target Host)",
                    "3. Scapy ARP Discovery (Autonomous Scan)",
                    "4. Exit",
                ],
                title="NETWORK RECON",
            )

            try:
                c = input(f"\n {B}Select{NC} {C}»{NC} ").strip()
            except EOFError:
                continue
            except KeyboardInterrupt:
                print(f"\n{Y}[*] Exiting recon module...{NC}")
                break

            if c == "1":
                # ARP discovery using OS tools (Linux) or Scapy (other OS)
                if sys.platform == "linux":
                    self._run_arp_scan_linux()
                else:
                    # Fallback for Windows/macOS
                    self.autonomous_scan()
                input(f"\n{W}Press Enter to continue...{NC}")

            elif c == "2":
                ip = input(f"\n{W}Target IP > {NC}").strip()
                self._run_nmap_scan(ip)
                input(f"\n{W}Press Enter to continue...{NC}")

            elif c == "3":
                # Scapy-based ARP / autonomous scan
                # Uses default 192.168.1.0/24 unless you later extend this
                self.autonomous_scan()
                input(f"\n{W}Press Enter to continue...{NC}")

            elif c == "4":
                break

            else:
                print(f"{Y}[!] Invalid selection. Please choose a valid option.{NC}")
                time.sleep(1)
