#!/usr/bin/env python3
"""
ScanPro Web Interface Launcher
"""

import sys
import os

# Add the scanpro directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from scanpro.web.app import ScanProWeb
except ImportError as e:
    print("Error: Flask is required for the web interface")
    print("Install Flask with: pip install flask")
    print(f"Import error: {e}")
    sys.exit(1)

def main():
    """Main entry point for web interface"""
    print("ScanPro Web Interface")
    print("=" * 40)
    print("Professional TCP Port Scanner")
    print("CLI + Web Dashboard | VM Support | Auto-Refresh")
    print()
    
    # Create web application
    web_app = ScanProWeb()
    
    # Run the server
    try:
        web_app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 ScanPro Web Interface stopped")
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        print("Make sure Flask is installed: pip install flask")

if __name__ == "__main__":
    main()
