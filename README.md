# ScanPro - Professional Port Scanner

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Interface-green?style=for-the-badge&logo=flask)
![Security](https://img.shields.io/badge/Security-Ethical%20Scanning-red?style=for-the-badge&logo=security)
![License](https://img.shields.io/badge/License-Educational-yellow?style=for-the-badge)

> **A modular, ethical TCP port scanner with both CLI and web interfaces, designed for security professionals and network administrators.**

## 🎯 **Key Highlights**
- 🔍 **Interactive CLI** with step-by-step guidance
- 🌐 **Modern Web Dashboard** with real-time updates
- 🛡️ **Built-in Safety Controls** and legal compliance
- ⚡ **Multi-threaded Performance** with configurable profiles
- 📊 **Professional Reporting** in JSON and text formats

## 📸 **Demo**

### Interactive CLI Experience
```
============================================================
    ____                  ____            
   / __/_______  ____    / __ \_________  
  _\ \/ ___/ __ \/ __ \  / /_/ / ___/ __ \ 
 /___/ /__/ /_/ / / / / / ____/ /  / /_/ / 
/____/\___/\____/_/ /_/ /_/   /_/   \____/  

   Professional Port Scanner v1.0.0
   For Cybersecurity Professionals
============================================================

📍 TARGET SELECTION → 🔍 PORT SELECTION → ⚙️ SCAN PROFILE → 🚀 EXECUTE
```

### Web Dashboard Features
- **Real-time Progress Tracking** - Watch scans execute live
- **Interactive Target Input** - Point-and-click configuration  
- **Auto-Refresh Results** - No manual page reloading needed
- **JSON Export** - Professional reporting capabilities
- **Safety Warnings** - Built-in ethical scanning guidelines

## ✨ Features

### Core Functionality
- **TCP Connect Scanning** - Fast, reliable port scanning
- **Multi-threaded Engine** - Concurrent scanning for performance
- **Target Parsing** - Support for IPs, ranges, and hostnames
- **Port Presets** - Quick scanning of common service ports
- **Scan Profiles** - Optimized settings (fast, stealth, aggressive)

### Web Interface
- **Modern Dashboard** - Intuitive web-based scanning
- **Real-time Updates** - Auto-refreshing results
- **VM/Lab Support** - Safe scanning of local virtual machines
- **Progress Tracking** - Live scan progress and status
- **Export Options** - JSON download and detailed reports

### Safety & Ethics
- **Built-in Safety Checks** - Prevents accidental external scanning
- **VM Network Support** - Pre-approved ranges for common virtualization
- **Legal Warnings** - Clear guidance on ethical usage
- **Confirmation Dialogs** - User verification for non-localhost targets

## 🚀 **Quick Start**

### 📦 Installation
```bash
# Clone the repository
git clone https://github.com/MAS191/ScanPro
cd ScanPro

# Install dependencies
pip install -r requirements.txt
```

### 🎮 Usage

**Interactive CLI (Recommended for Learning):**
```bash
python main.py
```

**Web Dashboard (Recommended for Regular Use):**
```bash
python web_server.py
# Open browser to: http://127.0.0.1:5000
```

### 🔧 Example Commands
```bash
# Quick localhost scan
python main.py
# Follow prompts: 127.0.0.1 → top20 ports → fast profile

# Web interface with real-time updates
python web_server.py
# Navigate to dashboard for point-and-click scanning
```

### Command Line Interface
```bash
# Interactive CLI (Recommended)
python main.py

# Web Interface
python web_server.py
# Open: http://127.0.0.1:5000
```

The interactive CLI will guide you through:
- Target selection (IP, hostname, range, CIDR)
- Port selection (presets or custom)
- Scan profile configuration
- Output options and formatting

## Safe Target Examples

**✅ Localhost:**
- `127.0.0.1`, `localhost`

**✅ Virtual Machines:**
- `192.168.56.x` (VirtualBox Host-Only)
- `192.168.1.x` (VMware NAT)
- `172.17.x.x` (Docker containers)

**⚠️ External targets require explicit confirmation**

## Project Structure

```
scanpro/
├── cli/              # Command line interface
├── config/           # Scan profiles and port presets
├── controller/       # Scan orchestration and control
├── core/             # Core models and utilities
├── reporting/        # Output formatting and reports
├── scanners/         # Scanning engine implementations
└── web/              # Web interface (Flask app)
```

## Documentation

See `USAGE.md` for detailed usage instructions and examples.

## Legal Notice

**⚠️ IMPORTANT:** Only scan systems you own or have explicit written permission to test. This tool is designed for legitimate security testing, network administration, and educational purposes only.

## License

This project is for educational and authorized security testing purposes only.

