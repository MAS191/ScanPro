#!/usr/bin/env python3
"""
ScanPro Main Entry Point
"""

import sys
import os

# Add the scanpro directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanpro.cli.main import main

if __name__ == "__main__":
    main()
