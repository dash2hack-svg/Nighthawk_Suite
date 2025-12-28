<p align="center"> <strong>A cross‑platform security suite for modern operators</strong> </p>

<p align="center"> <img src="assets/logo.png" width="180" alt="Nighthawk Suite Logo"/> </p>

<p align="center"> <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge"/> <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/> <img src="https://img.shields.io/badge/Platforms-Linux%20%7C%20macOS%20%7C%20WSL-orange?style=for-the-badge"/> <img src="https://img.shields.io/github/stars/dash2hack-svg/Nighthawk_Suite?style=for-the-badge"/> <img src="https://img.shields.io/github/last-commit/dash2hack-svg/Nighthawk_Suite?style=for-the-badge"/> <img src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge"/> </p>

🎯 Overview

Nighthawk Suite is a cinematic, operator‑grade network reconnaissance toolkit designed for modern security professionals.Built with a focus on clarity, speed, and visual immersion, Nighthawk Suite provides a streamlined interface for network scanning, packet sniffing, and device discovery across supported platforms.

⚡ Features

🔍 Network Scanning

Identify active hosts, open ports, and network topology with precision.

📡 Packet Sniffing

Capture and analyze packets in real time (Linux/macOS only).

🛰 Device Discovery

Enumerate devices, interfaces, and network metadata with clarity.

🎨 Cinematic UI

Rich‑powered terminal interface with animations, themes, and operator‑grade visuals.

🧩 Modular Architecture

Easily extend or customize modules for your workflow.

🛠 Installation

Linux (Recommended)

git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

macOS

git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo python main.py

Windows (WSL Required)

Native Windows networking does not support raw sockets or packet injection.

To run Nighthawk Suite on Windows:

wsl --install
# Install Ubuntu or Kali
git clone https://github.com/dash2hack-svg/Nighthawk_Suite.git
cd Nighthawk_Suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🚀 Usage

python main.py

Once launched, navigate the cinematic UI to select modules such as:

Network Scan

Packet Sniffer

Device Discovery

Interface Overview

🌍 Platform Support

Platform

Support Level

Notes

Linux

✅ Full

All features supported

macOS

⚠️ Partial

Raw sockets limited; monitor mode varies

Windows

❌ Native support unavailable

Use WSL for full functionality


📜 License (MIT)

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...

⚠ Disclaimer

This tool is for authorized security testing only.Do not use without explicit permission.

Unauthorized use may violate local, state, or federal laws.

🦅 Nighthawk Suite

Precision. Clarity. Operator‑grade performance.
