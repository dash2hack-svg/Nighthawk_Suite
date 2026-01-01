# Nighthawk Suite

**Cross-platform wireless assessment framework for authorized security testing (Linux / Windows / macOS).**

Nighthawk Suite is a Python-based framework designed to help security professionals and network owners perform **authorized wireless security assessments** in a controlled, auditable way. It provides tooling for reconnaissance, capture, conversion, and reporting workflows.

> **Important:** Nighthawk Suite is intended **only** for networks and systems you own or are explicitly authorized in writing to assess. Misuse may be illegal and is strictly discouraged.

---

## Key capabilities

### Wireless assessment (Linux focus)

- **Handshake capture (WPA2/WPA3 where supported)**  
  Automates discovery of nearby access points and attempts to capture 4‑way handshakes for offline password strength testing.
- **Attack orchestration**  
  Integrates with tools like `aircrack-ng` and `hcxtools` for end‑to‑end workflows (capture → convert → offline crack).
- **Interface / driver health checks**  
  Helps avoid unstable configurations by checking adapter and driver capabilities before attempting injection‑heavy operations.

> **Note:** Some features (such as injection) depend on specific chipsets and drivers and may only work on Linux distributions such as Kali, Parrot, or Ubuntu.

### Enterprise / EAP testing (authorized lab environments only)

- **RADIUS / EAP test harness (WPE‑style behavior)**  
  Helps test whether enterprise Wi‑Fi clients properly validate certificates and are resistant to credential phishing in **authorized lab or test environments**.
- **Rogue AP scenarios (Evil Twin)**  
  Spins up controlled, clearly marked test access points and captive portals for social engineering awareness training and security assessments.

> These features are **only for environments where you have explicit authorization** (for example: internal red team exercises, defensive lab setups, or training ranges). Do not deploy these features against production networks or systems you are not authorized to test.

### Cross-platform support

- **Linux (Kali / Parrot / Ubuntu recommended)**  
  Full feature set, including active wireless testing modules (where hardware and drivers support it).
- **Windows (Auditor mode)**  
  Focus on passive recon, loot management, and offline cracking (raw injection typically unavailable).
- **macOS (Recon mode)**  
  Passive recon, limited BLE scanning, and loot management where system APIs and drivers allow.

Nighthawk Suite attempts to detect host OS and hardware capabilities and enables only the features that are safe and supported on that platform.

---

## Installation and usage

### 1. Clone the repository

```bash
git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
```

### 2. Linux setup (recommended for full functionality)

On a Debian-based system (Kali, Parrot, Ubuntu):

```bash
sudo apt update
sudo apt install -y aircrack-ng hostapd dnsmasq hcxtools macchanger
```

Install Python dependencies:

```bash
pip3 install -r requirements.txt
```

Run Nighthawk Suite (root is typically required for wireless interfaces):

```bash
sudo python3 nighthawk.py
```

### 3. Windows (auditor mode)

Supported features: passive recon, loot management, and offline cracking (no raw injection).

- Install Npcap (during install, ensure “Install Npcap in WinPcap API-compatible Mode” is checked).
- Install Python 3.x from python.org.
- Open an elevated PowerShell (Run as Administrator):

```powershell
cd path\to\Nighthawk_Suite
pip install -r requirements.txt
python nighthawk.py
```

### 4. macOS (recon mode)

Supported features: passive recon, some Bluetooth scanning, loot management.

- Install Homebrew (if not already installed).
- Install dependencies:

```bash
brew install nmap
pip3 install -r requirements.txt
sudo python3 nighthawk.py
```

Note: macOS wireless APIs and driver restrictions can limit low‑level functionality. Nighthawk Suite will automatically restrict features to those that are safe and supported on the platform.

---

## Module overview

| Module            | Purpose                                                                 |
|-------------------|-------------------------------------------------------------------------|
| Encryption        | Automates WPA2/WPA3 handshake capture and integrates with cracking tools. |
| Enterprise WPE    | Simulated RADIUS/WPE server for testing enterprise Wi‑Fi configurations in authorized labs. |
| Evil Twin         | Rogue AP + captive portal for awareness training and controlled phishing simulations. |
| Loot Repository   | Organizes captured data, credentials, and generates HTML reports (“trophy room”). |
| Recon             | Network mapping, OS detection, and environmental telemetry (where supported). |
| Bluetooth Arsenal | BLE scanning and basic tests (Linux) where hardware permits. |

All modules are designed to be modular and extensible, so new capabilities can be added without modifying the core framework.

---

## Design philosophy

Nighthawk Suite is built with three priorities:

1. Safety and scope awareness  
   - Features are explicitly designed to be used only on in‑scope targets with written authorization.  
   - Where possible, Nighthawk checks OS and interface capabilities to avoid unstable or undefined behavior.

2. Automation with transparency  
   - Automates tedious workflows (recon → capture → conversion → reporting) while keeping steps visible and controllable.  
   - Encourages users to understand the actions being performed rather than treat it as a “black box.”

3. Modularity and maintainability  
   - Clear separation between core engine and modules.  
   - Easier debugging, customization, and extension by security teams and researchers.

---

## Ethics and legal disclaimer

This project is intended for:

- Security professionals performing authorized assessments
- Network owners testing the resilience of their own infrastructure
- Students in controlled lab environments learning about wireless security

You are solely responsible for complying with all applicable laws and regulations in your jurisdiction. Using this tool against networks or systems without explicit, written permission may violate the law.

The authors and contributors do not assume any responsibility or liability for misuse, damage, legal issues, or any other consequences arising from the use of this software.

---

## License

Nighthawk Suite is distributed under the MIT License. See the [LICENSE](LICENSE) file for full details.
