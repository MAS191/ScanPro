"""
Core utilities and shared types for ScanPro
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
import ipaddress
import re

class ScanType(Enum):
    """Enumeration of available scan types"""
    TCP_CONNECT = "tcp_connect"
    TCP_SYN = "tcp_syn"
    UDP = "udp"
    ICMP = "icmp"

class PortState(Enum):
    """Port state enumeration"""
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"
    UNKNOWN = "unknown"

@dataclass
class ScanResult:
    """Data class for individual port scan results"""
    host: str
    port: int
    state: PortState
    service: Optional[str] = None
    banner: Optional[str] = None
    scan_time: Optional[float] = None
    error: Optional[str] = None

@dataclass
class HostResult:
    """Data class for host scan results"""
    host: str
    ports: List[ScanResult]
    scan_start: float
    scan_end: float
    is_alive: bool = True

@dataclass
class ScanConfig:
    """Configuration for scan parameters"""
    targets: List[str]
    ports: List[int]
    scan_type: ScanType = ScanType.TCP_CONNECT
    timeout: float = 3.0
    threads: int = 100
    delay: float = 0.0
    verbose: bool = False
    output_format: str = "json"
    output_file: Optional[str] = None

class NetworkUtils:
    """Utility functions for network operations"""
    
    @staticmethod
    def parse_targets(target_str: str) -> List[str]:
        """Parse target string into list of IP addresses"""
        targets = []
        
        for target in target_str.split(','):
            target = target.strip()
            
            if '/' in target:  # CIDR notation
                try:
                    network = ipaddress.ip_network(target, strict=False)
                    targets.extend([str(ip) for ip in network.hosts()])
                except ValueError:
                    print(f"Invalid CIDR notation: {target}")
                    continue
            
            elif '-' in target and target.count('.') == 3:  # IP range
                try:
                    start_ip, end_ip = target.split('-')
                    start = ipaddress.IPv4Address(start_ip.strip())
                    end = ipaddress.IPv4Address(end_ip.strip())
                    
                    current = start
                    while current <= end:
                        targets.append(str(current))
                        current += 1
                except ValueError:
                    print(f"Invalid IP range: {target}")
                    continue
            
            else:  # Single IP or hostname
                targets.append(target)
        
        return targets
    
    @staticmethod
    def parse_ports(port_str: str) -> List[int]:
        """Parse port string into list of port numbers"""
        ports = []
        
        # Common port presets
        presets = {
            'top100': [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080],
            'top1000': list(range(1, 1001)),
            'all': list(range(1, 65536))
        }
        
        if port_str.lower() in presets:
            return presets[port_str.lower()]
        
        for port_range in port_str.split(','):
            port_range = port_range.strip()
            
            if '-' in port_range:
                try:
                    start, end = map(int, port_range.split('-'))
                    ports.extend(range(start, end + 1))
                except ValueError:
                    print(f"Invalid port range: {port_range}")
                    continue
            else:
                try:
                    ports.append(int(port_range))
                except ValueError:
                    print(f"Invalid port number: {port_range}")
                    continue
        
        return sorted(list(set(ports)))  # Remove duplicates and sort
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Check if string is a valid IP address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def resolve_hostname(hostname: str) -> Optional[str]:
        """Resolve hostname to IP address"""
        import socket
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
