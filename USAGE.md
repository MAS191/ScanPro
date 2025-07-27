# ScanPro Usage Guide

## ⚖️ LEGAL NOTICE

**🚨 IMPORTANT: Only scan systems you own or have explicit written permission to test!**

All examples in this guide use localhost (127.0.0.1) which is completely legal as it's your own machine. Never scan external systems, networks, or services without explicit authorization.

## Quick Start

### Installation
Install the required dependencies for the web interface:

```bash
git clone <repository-url>
cd portscanner
pip install flask
```

For basic CLI-only usage, no dependencies are required.

## 💻 Interactive CLI (Recommended for Learning)

ScanPro features a user-friendly interactive CLI that guides you through the scanning process step-by-step.

### Starting the Interactive CLI

```bash
python main.py
```

### Interactive Features

The CLI will guide you through:

1. **📍 Target Selection**
   - Single IP addresses
   - Multiple IPs (comma-separated)
   - IP ranges (e.g., 192.168.1.1-192.168.1.10)
   - CIDR notation (e.g., 192.168.1.0/24)
   - Hostnames
   - File input (one target per line)

2. **🔍 Port Selection**
   - Pre-configured port presets (top20, top100, web, mail, etc.)
   - Custom port ranges (e.g., 1-1000)
   - Individual ports (e.g., 80,443,8080)

3. **⚙️ Scan Profile Selection**
   - **default** - Balanced performance and accuracy
   - **fast** - Quick scans with reduced timeout
   - **slow** - Careful scanning to avoid detection
   - **stealth** - Delayed requests for stealth
   - **aggressive** - Maximum speed scanning
   - **custom** - Manual configuration

4. **🔧 Custom Configuration** (if custom profile selected)
   - Connection timeout (0.1-60.0 seconds)
   - Thread count (1-1000)
   - Request delay (0.0-10.0 seconds)

5. **💾 Output Options**
   - Verbosity level (Normal/Verbose/Quiet)
   - Save to file option
   - Output format (JSON/Text)

6. **🛡️ Safety Checks**
   - Automatic detection of localhost vs external targets
   - VM/lab network pre-approval
   - Confirmation prompts for external targets

### Example Interactive Session

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

⚠️  LEGAL WARNING AND DISCLAIMER:
   • Only scan systems you own or have explicit permission to test
   • Unauthorized scanning may be illegal in your jurisdiction
   • This tool is for authorized security testing only
   • The user is solely responsible for all activities

Press Enter to continue or Ctrl+C to exit...

📍 TARGET SELECTION
--------------------
Enter target(s) to scan:
  • Single IP: 192.168.1.1
  • Multiple IPs: 192.168.1.1,192.168.1.2
  • IP range: 192.168.1.1-192.168.1.10
  • CIDR notation: 192.168.1.0/24
  • Hostname: example.com
  • File path: targets.txt (one target per line)
  • Safe testing: 127.0.0.1 or localhost

Targets: 127.0.0.1
✅ Parsed 1 targets

🔍 PORT SELECTION
-----------------
Available port presets:
  1. top20      - 20 ports
  2. top100     - 87 ports
  3. web        - 10 ports
  4. mail       - 7 ports
  5. db         - 6 ports
  6. remote     - 6 ports
  7. all        - 65535 ports
  8. custom     - Enter custom ports

Select option (1-8): 3
✅ Selected web preset (10 ports)

⚙️  SCAN PROFILE
---------------
Available scan profiles:
  1. default      - Default balanced scan profile
  2. fast         - Fast scan with reduced timeout and high concurrency
  3. slow         - Slow, careful scan to avoid detection
  4. stealth      - Stealthy scan with delays between requests
  5. aggressive   - Aggressive scan for maximum speed
  6. custom       - Configure manually

Select profile (1-6): 2
✅ Selected fast profile

💾 OUTPUT OPTIONS
----------------
Select output verbosity:
  1. Normal  - Standard output
  2. Verbose - Detailed output
  3. Quiet   - Minimal output

Verbosity (1-3) [1]: 1

Save results to file? (y/n) [n]: n

📋 SCAN SUMMARY
--------------
Targets:      1 host(s)
              • 127.0.0.1
Ports:        10 port(s)
Timeout:      1.0s
Threads:      200
Delay:        0.0s
Output:       Normal

Estimated scan time: ~0.1s

🚀 Start scan? (y/n): y

🔍 Starting scan...
--------------------
[... scan results ...]
```

## 🌐 Web Interface

ScanPro also includes a modern web interface for easy scanning!

### Starting the Web Interface

```bash
python web_server.py
```

Then open your browser to: **http://127.0.0.1:5000**

### Web Interface Features

✅ **User-Friendly Dashboard** - Point-and-click scanning  
✅ **Real-time Progress** - Live scan status updates  
✅ **Auto-Refresh Results** - No manual refresh needed!  
✅ **Visual Results** - Beautiful, organized result display  
✅ **Scan History** - View and manage previous scans  
✅ **JSON Export** - Download results in JSON format  
✅ **VM/Lab Support** - Scan VirtualBox, VMware, Docker containers  
✅ **Safety Checks** - Built-in confirmation for external targets  
✅ **Toast Notifications** - Real-time scan completion alerts  
✅ **Smart Auto-Pause** - Pauses when browser tab is hidden  
✅ **Responsive Design** - Works on desktop and mobile  

### Supported Target Types

**✅ Safe Targets (No Confirmation Required):**
- `127.0.0.1`, `localhost` - Your local machine
- `192.168.56.x` - VirtualBox Host-Only network
- `192.168.1.x` - VMware NAT network
- `192.168.57.x` - VMware Host-Only network
- `172.17.x.x` - Docker bridge network
- `10.0.0.x`, `192.168.0.x` - Common lab networks

**⚠️ External Targets (Requires Confirmation):**
- Any IP outside the safe ranges above
- Public IP addresses (❌ **NEVER scan without permission!**)

### Using the Web Interface

1. **Start a Scan:**
   - Enter targets (e.g., 127.0.0.1, 192.168.56.101)
   - Choose port preset or custom ports
   - Select scan profile (fast, stealth, etc.)
   - Adjust timeout and threads if needed
   - Click "Start Scan"

2. **Monitor Progress:**
   - Real-time progress indicator with percentage
   - Live status updates (no refresh needed!)
   - Automatic result display when complete
   - Toast notifications for scan events
   - Smart pause when browser tab is hidden

3. **View Results:**
   - Summary statistics
   - Open ports with service detection
   - Banner information
   - Detailed timing information

4. **Export Data:**
   - Download JSON results
   - View detailed results page
   - Access scan history

## 💻 Command Line Interface

### Installation
No external dependencies required for basic TCP scanning. Simply clone or download the project:

```bash
git clone <repository-url>
cd portscanner
```

### Basic Usage (Localhost Only)

1. **Scan localhost:**
```bash
python main.py 127.0.0.1
```

2. **Scan specific ports on localhost:**
```bash
python main.py 127.0.0.1 -p 80,443,8080
```

3. **Scan port range on localhost:**
```bash
python main.py 127.0.0.1 -p 1-1000
```

4. **Scan using port presets on localhost:**
```bash
python main.py 127.0.0.1 -p top100
python main.py 127.0.0.1 -p web
python main.py 127.0.0.1 -p db
```

5. **Scan multiple localhost interfaces:**
```bash
python main.py 127.0.0.1,::1  # IPv4 and IPv6 localhost
```

### Scan Profiles

Use predefined profiles for different scenarios on localhost:

```bash
# Fast scan of localhost
python main.py 127.0.0.1 --profile fast

# Stealth scan of localhost
python main.py 127.0.0.1 --profile stealth

# Slow scan of localhost
python main.py 127.0.0.1 --profile slow

# Aggressive scan of localhost
python main.py 127.0.0.1 --profile aggressive
```

### Output Options

```bash
# Save localhost scan results to JSON file
python main.py 127.0.0.1 -o results.json

# Save localhost scan results to text file
python main.py 127.0.0.1 -o results.txt

# Verbose output
python main.py 127.0.0.1 -v

# Quiet mode
python main.py 127.0.0.1 -q
```

### Advanced Options

```bash
# Custom timeout and thread count for localhost
python main.py 127.0.0.1 --timeout 5.0 --threads 200

# Add delay between requests
python main.py 127.0.0.1 --delay 0.1
```

### Information Commands

```bash
# List available profiles
python main.py --list-profiles

# List available port presets
python main.py --list-presets

# Show version
python main.py --version

# Show help
python main.py -h
```

## Example Scenarios (Localhost Only)

### 1. Web Application Testing (Your Local Server)
```bash
python main.py 127.0.0.1 -p web --profile fast -o webapp_scan.json
```

### 2. Database Server Check (Your Local Database)
```bash
python main.py 127.0.0.1 -p db --timeout 10 -v
```

### 3. Quick Service Check (Your Local Services)
```bash
python main.py 127.0.0.1 -p 22,80,443 --profile fast
```

### 4. Comprehensive Scan (Your Local Machine)
```bash
python main.py 127.0.0.1 -p top1000 --profile default -o comprehensive_scan.json
```

## 🖥️ Scanning Virtual Machines

ScanPro is perfect for testing your VMs and lab environments! Here's how to scan common virtualization platforms:

### VirtualBox VMs

VirtualBox typically uses the `192.168.56.x` network for Host-Only adapters:

**Web Interface:**
```
Targets: 192.168.56.101, 192.168.56.102
Ports: top20 or web
```

**Command Line:**
```bash
python main.py 192.168.56.101 -p 22,80,443,3389
```

### VMware VMs

VMware commonly uses these networks:
- NAT: `192.168.1.x` 
- Host-Only: `192.168.57.x`

**Web Interface:**
```
Targets: 192.168.1.100
Ports: top100
```

**Command Line:**
```bash
python main.py 192.168.1.100 -p top20 --profile fast
```

### Docker Containers

Docker bridge network typically uses `172.17.x.x`:

**Web Interface:**
```
Targets: 172.17.0.2, 172.17.0.3
Ports: web
```

**Command Line:**
```bash
python main.py 172.17.0.2 -p 80,443,8080,9000
```

### Finding Your VM IPs

**VirtualBox:**
```bash
# In VM or host
ip addr show    # Linux/Mac
ipconfig        # Windows
```

**VMware:**
```bash
# Check VMware network settings
vmnetcfg.exe    # Windows
```

**Docker:**
```bash
docker inspect <container_name> | grep IPAddress
```

### Safety Notes for VM Scanning

✅ **Safe to scan:**
- Your own VMs on your computer
- Lab VMs you created
- Test environments you control
- Containers you deployed

❌ **Never scan:**
- Shared hosting VMs
- Cloud VMs you don't own
- Corporate VMs without permission
- Production systems

## File Formats

### Target File Format
Create a text file with localhost entries for testing:
```
127.0.0.1
::1
# You can add your own VMs or lab machines here
# 192.168.56.101  # Your VirtualBox VM
# 10.0.0.5        # Your Docker container
```

### JSON Output Format
```json
{
  "scanpro_version": "1.0.0",
  "scan_info": {
    "start_time": 1234567890.0,
    "end_time": 1234567900.0,
    "total_hosts": 1,
    "total_ports_scanned": 100
  },
  "hosts": [
    {
      "host": "127.0.0.1",
      "scan_duration": 5.23,
      "is_alive": true,
      "ports": [
        {
          "port": 80,
          "state": "open",
          "service": "http",
          "banner": "Apache/2.4.41",
          "scan_time": 0.05
        }
      ]
    }
  ]
}
```

## Performance Tips

1. **Thread Count**: Adjust based on your system and target network
   - Local network: 100-300 threads
   - Internet targets: 50-100 threads
   - Slow/unstable targets: 25-50 threads

2. **Timeout Values**: 
   - Fast scan: 1-2 seconds
   - Default: 3-5 seconds  
   - Careful scan: 10+ seconds

3. **Delays**: Add delays to avoid overwhelming targets or detection
   - Stealth: 0.1-1.0 seconds
   - Very careful: 1.0+ seconds

## Troubleshooting

### Common Issues

1. **"Permission denied" errors**: Some features may require elevated privileges
2. **High CPU usage**: Reduce thread count or add delays
3. **Network timeouts**: Increase timeout value or check connectivity
4. **Memory usage**: For large scans, scan smaller chunks or reduce threads

### Error Messages

- **"No targets specified"**: Provide targets via command line or file
- **"Invalid port range"**: Check port specification syntax
- **"Could not resolve hostname"**: Check DNS resolution
- **"Connection timed out"**: Target may be down or filtered

## Security and Legal Notice

⚠️ **IMPORTANT**: Use ScanPro responsibly and legally
- Only scan systems you own or have explicit permission to test
- Be aware of local laws and regulations
- Some scan types may be detected by intrusion detection systems
- Use appropriate delays and profiles to avoid overwhelming targets

## Extending ScanPro

ScanPro is designed to be modular and extensible. You can:

1. **Add new scan types** in the `scanners/` directory
2. **Create custom analyzers** in the `analyzers/` directory  
3. **Develop new report formats** in the `reporting/` directory
4. **Add scan profiles** in the `config/` directory

See the source code for examples and architecture details.
