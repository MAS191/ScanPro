"""
TCP Connect Scanner Implementation
"""

import socket
import threading
import time
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..core.models import ScanResult, PortState, ScanConfig


class TCPConnectScanner:
    """TCP Connect Scanner using full three-way handshake"""
    
    def __init__(self, config: ScanConfig):
        self.config = config
        self.results = []
        self.lock = threading.Lock()
    
    def scan_port(self, host: str, port: int) -> ScanResult:
        """Scan a single port on a host"""
        start_time = time.time()
        
        try:
            # Resolve hostname if needed
            if not self._is_ip_address(host):
                resolved_ip = socket.gethostbyname(host)
                if self.config.verbose:
                    print(f"Resolved {host} to {resolved_ip}")
                host = resolved_ip
            
            # Create socket and attempt connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.config.timeout)
            
            result = sock.connect_ex((host, port))
            scan_time = time.time() - start_time
            
            if result == 0:
                # Connection successful - port is open
                banner = self._grab_banner(sock, port)
                sock.close()
                
                return ScanResult(
                    host=host,
                    port=port,
                    state=PortState.OPEN,
                    service=self._get_service_name(port),
                    banner=banner,
                    scan_time=scan_time
                )
            else:
                # Connection failed - port is closed
                sock.close()
                return ScanResult(
                    host=host,
                    port=port,
                    state=PortState.CLOSED,
                    scan_time=scan_time
                )
                
        except socket.timeout:
            return ScanResult(
                host=host,
                port=port,
                state=PortState.FILTERED,
                scan_time=time.time() - start_time,
                error="Timeout"
            )
        except Exception as e:
            return ScanResult(
                host=host,
                port=port,
                state=PortState.UNKNOWN,
                scan_time=time.time() - start_time,
                error=str(e)
            )
    
    def scan_host(self, host: str, ports: List[int]) -> List[ScanResult]:
        """Scan multiple ports on a single host"""
        host_results = []
        
        with ThreadPoolExecutor(max_workers=self.config.threads) as executor:
            # Submit all port scan tasks
            future_to_port = {
                executor.submit(self.scan_port, host, port): port 
                for port in ports
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_port):
                try:
                    result = future.result()
                    host_results.append(result)
                    
                    if self.config.verbose and result.state == PortState.OPEN:
                        print(f"[+] {result.host}:{result.port} - {result.state.value}")
                    
                    # Add delay if specified
                    if self.config.delay > 0:
                        time.sleep(self.config.delay)
                        
                except Exception as e:
                    port = future_to_port[future]
                    print(f"Error scanning {host}:{port} - {e}")
        
        return host_results
    
    def _grab_banner(self, sock: socket.socket, port: int) -> Optional[str]:
        """Attempt to grab banner from open port"""
        try:
            # Send appropriate probe based on port
            if port == 80:
                sock.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            elif port == 21:
                pass  # FTP sends banner immediately
            elif port == 22:
                pass  # SSH sends banner immediately
            elif port == 25:
                pass  # SMTP sends banner immediately
            else:
                sock.send(b"\r\n")
            
            # Try to receive banner
            sock.settimeout(2.0)
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner[:200] if banner else None  # Limit banner length
            
        except:
            return None
    
    def _get_service_name(self, port: int) -> Optional[str]:
        """Get common service name for port"""
        common_ports = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
            53: "dns", 80: "http", 110: "pop3", 135: "msrpc",
            139: "netbios-ssn", 143: "imap", 443: "https",
            993: "imaps", 995: "pop3s", 1433: "mssql",
            3306: "mysql", 3389: "rdp", 5432: "postgresql",
            5900: "vnc", 8080: "http-proxy"
        }
        return common_ports.get(port)
    
    def _is_ip_address(self, host: str) -> bool:
        """Check if host is an IP address"""
        try:
            socket.inet_aton(host)
            return True
        except socket.error:
            return False
