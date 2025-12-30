<h1 align="center">🦅 Nighthawk Suite</h1>
<p align="center"><strong>Precision. Clarity. Operator‑grade performance.</strong></p>

<p align="center">
  <img src="assets/logo.png" width="180" alt="Nighthawk Suite Logo"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/github/v/release/dash2hack-svg/Nighthawk_Suite?style=for-the-badge"/>
</p>

---

### 🎯 Overview
Nighthawk Suite is a **cinematic, operator‑grade network reconnaissance toolkit** designed for modern security professionals. It’s built with clarity, speed, and visual immersion to help you master network reconnaissance like never before.

---

### ⚡ Features
- 🔍 **Network Scanning**: Identify active hosts, open ports, and network topology with precision.
- 📡 **Packet Sniffing**: Capture and analyze packets in real time (*Linux/macOS only*).
- 🛰 **Device Discovery**: Enumerate devices, interfaces, and network metadata with clarity.
- 🎨 **Cinematic UI**: Rich terminal interface with animations, themes, and operator‑grade visuals.
- 🧩 **Modular Architecture**: Easily extend or customize modules for your workflow.

---

### 🛠 Installation
#### Linux (Recommended)
```bash
git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo ./nighthawk.py
```

#### macOS
```bash
git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo python main.py
```

#### Windows (WSL Required)
> **Note:** Native Windows networking does not support raw sockets or packet injection. Use WSL for full functionality.

```bash
wsl --install
# Install Ubuntu or Kali
git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Navigate through the cinematic UI to access modules like:
- **Network Scan**
- **Packet Sniffer**
- **Device Discovery**
- **Interface Overview**

---

### 🌍 Platform Support
| Platform | Support Level | Notes |
|----------|---------------|-------|
| **Linux**  | ✅ Full          | All features supported. |
| **macOS**  | ⚠️ Partial       | Limitations with raw sockets; monitor mode varies. |
| **Windows**| ❌ Unsupported   | Use WSL for full functionality. |

---

### 📜 License
This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

### ⚠ Disclaimer
This tool is for **authorized security testing only**. Do not use without explicit permission. Unauthorized use may violate local, state, or federal laws.

---
