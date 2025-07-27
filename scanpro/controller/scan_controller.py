"""
Scan Controller - Orchestrates scanning operations
"""

import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..core.models import ScanConfig, HostResult, ScanResult, ScanType, NetworkUtils
from ..scanners.tcp_scanner import TCPConnectScanner


class ScanController:
    """Main controller for orchestrating scans"""
    
    def __init__(self, config: ScanConfig):
        self.config = config
        self.results = []
    
    def execute_scan(self) -> List[HostResult]:
        """Execute the scan based on configuration"""
        print(f"[*] Starting ScanPro scan...")
        print(f"[*] Scan type: {self.config.scan_type.value}")
        print(f"[*] Targets: {len(self.config.targets)}")
        print(f"[*] Ports: {len(self.config.ports)}")
        print(f"[*] Threads: {self.config.threads}")
        print(f"[*] Timeout: {self.config.timeout}s")
        print("-" * 50)
        
        scan_start = time.time()
        
        # Select scanner based on scan type
        if self.config.scan_type == ScanType.TCP_CONNECT:
            scanner = TCPConnectScanner(self.config)
        else:
            raise NotImplementedError(f"Scan type {self.config.scan_type} not implemented yet")
        
        host_results = []
        
        # Scan each target
        for i, target in enumerate(self.config.targets, 1):
            print(f"[*] Scanning target {i}/{len(self.config.targets)}: {target}")
            
            target_start = time.time()
            
            # Resolve hostname if needed
            resolved_ip = target
            if not NetworkUtils.is_valid_ip(target):
                resolved_ip = NetworkUtils.resolve_hostname(target)
                if not resolved_ip:
                    print(f"[-] Could not resolve hostname: {target}")
                    continue
                elif self.config.verbose:
                    print(f"[*] Resolved {target} to {resolved_ip}")
            
            # Perform port scan
            port_results = scanner.scan_host(resolved_ip, self.config.ports)
            
            target_end = time.time()
            
            # Create host result
            host_result = HostResult(
                host=target,
                ports=port_results,
                scan_start=target_start,
                scan_end=target_end,
                is_alive=any(result and result.state and result.state.value == "open" for result in port_results)
            )
            
            host_results.append(host_result)
            
            # Print summary for this host
            open_ports = [r for r in port_results if r and r.state and r.state.value == "open"]
            if open_ports:
                print(f"[+] Found {len(open_ports)} open ports on {target}")
                for result in open_ports:
                    service_info = f" ({result.service})" if result.service else ""
                    banner_info = f" - {result.banner[:50]}..." if result.banner else ""
                    print(f"    {result.port}/tcp{service_info}{banner_info}")
            else:
                print(f"[-] No open ports found on {target}")
            
            print()
        
        scan_end = time.time()
        total_time = scan_end - scan_start
        
        # Print final summary
        self._print_summary(host_results, total_time)
        
        return host_results
    
    def _print_summary(self, results: List[HostResult], scan_time: float):
        """Print scan summary"""
        print("=" * 60)
        print("SCAN SUMMARY")
        print("=" * 60)
        
        if not results:
            print("No scan results to display")
            print("=" * 60)
            return
        
        total_hosts = len(results)
        live_hosts = len([r for r in results if r.is_alive])
        total_ports_scanned = sum(len(r.ports) for r in results if r.ports)
        total_open_ports = sum(len([p for p in r.ports if p and p.state and p.state.value == "open"]) for r in results if r.ports)
        
        print(f"Scan completed in {scan_time:.2f} seconds")
        print(f"Hosts scanned: {total_hosts}")
        print(f"Live hosts: {live_hosts}")
        print(f"Total ports scanned: {total_ports_scanned}")
        print(f"Open ports found: {total_open_ports}")
        
        if total_open_ports > 0:
            print(f"\nOpen ports by host:")
            for result in results:
                if not result.ports:
                    continue
                open_ports = [p for p in result.ports if p and p.state and p.state.value == "open"]
                if open_ports:
                    ports_str = ", ".join([f"{p.port}/tcp" for p in open_ports])
                    print(f"  {result.host}: {ports_str}")
        
        print("=" * 60)
