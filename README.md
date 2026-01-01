# Nighthawk Suite

**Cross-platform wireless assessment framework for authorized security testing (Linux / Windows / macOS).**

Nighthawk Suite is a Python-based framework designed to help security professionals and network owners perform **authorized wireless security assessments** in a controlled, auditable way. It provides automation around common defensive and offensive techniques used in Wi‑Fi and network security testing while emphasizing **safety, scoping, and explicit permission** at every step.

> **Important:** Nighthawk Suite is intended **only** for networks and systems you own or are explicitly authorized in writing to assess. Misuse may be illegal and is strictly discouraged.

---

## Key capabilities

### Wireless assessment (Linux focus)

- **Handshake capture (WPA2/WPA3 where supported)**  
  - Automates discovery of nearby access points and attempts to capture 4‑way handshakes for offline password strength testing.
- **Attack orchestration**  
  - Integrates with tools like `aircrack-ng` and `hcxtools` for end‑to‑end workflows (capture → convert → offline crack).
- **Interface / driver health checks**  
  - Helps avoid unstable configurations by checking adapter and driver capabilities before attempting injection‑heavy operations.

> **Note:** Some features (such as injection) depend on specific chipsets and drivers and may only work on Linux distributions such as Kali, Parrot, or Ubuntu.

### Enterprise / EAP testing (authorized lab environments only)

- **RADIUS / EAP test harness (WPE‑style behavior)**  
  - Helps test whether enterprise Wi‑Fi clients properly validate certificates and are resistant to credential phishing in **authorized lab or test environments**.
- **Rogue AP scenarios (Evil Twin)**  
  - Spins up controlled, clearly marked test access points and captive portals for social engineering awareness training and security assessments.

> These features are **only for environments where you have explicit authorization** (for example: internal red team, defensive lab setups, or training ranges). Do not deploy against production networks without written approval and well‑defined scope.

### Cross-platform support

- **Linux (Kali / Parrot / Ubuntu recommended)**  
  - Full feature set, including active wireless testing modules (where hardware and drivers support it).
- **Windows (Auditor mode)**  
  - Focus on passive recon, loot management, and offline cracking.
- **macOS (Recon mode)**  
  - Passive recon, limited BLE scanning, and loot management where system APIs and drivers allow.

Nighthawk Suite attempts to detect host OS and hardware capabilities and enables only the features that are safe and supported on that platform.

---

## Installation and usage

### 1. Clone the repository

```bash
git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
