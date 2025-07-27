"""
Reporting and output formatting for scan results
"""

import json
import time
from typing import List, Dict, Any
from pathlib import Path

from ..core.models import HostResult, ScanResult


class JSONReporter:
    """JSON format reporter"""
    
    @staticmethod
    def generate_report(results: List[HostResult], config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate JSON report from scan results"""
        current_time = time.time()
        
        # Filter out None values for start/end times
        valid_start_times = [r.scan_start for r in results if r.scan_start is not None]
        valid_end_times = [r.scan_end for r in results if r.scan_end is not None]
        
        report = {
            "scanpro_version": "1.0.0",
            "scan_info": {
                "start_time": min(valid_start_times) if valid_start_times else current_time,
                "end_time": max(valid_end_times) if valid_end_times else current_time,
                "total_hosts": len(results),
                "total_ports_scanned": sum(len(r.ports) for r in results if r.ports),
                "scan_config": config or {}
            },
            "hosts": []
        }
        
        for host_result in results:
            scan_duration = 0
            if host_result.scan_start is not None and host_result.scan_end is not None:
                scan_duration = host_result.scan_end - host_result.scan_start
                
            host_data = {
                "host": host_result.host,
                "scan_start": host_result.scan_start or current_time,
                "scan_end": host_result.scan_end or current_time,
                "scan_duration": scan_duration,
                "is_alive": host_result.is_alive,
                "ports": []
            }
            
            for port_result in host_result.ports:
                port_data = {
                    "port": port_result.port,
                    "state": port_result.state.value,
                    "service": port_result.service,
                    "banner": port_result.banner,
                    "scan_time": port_result.scan_time,
                    "error": port_result.error
                }
                host_data["ports"].append(port_data)
            
            report["hosts"].append(host_data)
        
        return report
    
    @staticmethod
    def save_report(results: List[HostResult], filename: str, config: Dict[str, Any] = None):
        """Save JSON report to file"""
        report = JSONReporter.generate_report(results, config)
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[*] JSON report saved to: {filename}")


class TextReporter:
    """Plain text reporter"""
    
    @staticmethod
    def generate_report(results: List[HostResult]) -> str:
        """Generate plain text report"""
        lines = []
        lines.append("ScanPro Scan Report")
        lines.append("=" * 50)
        lines.append("")
        
        for host_result in results:
            scan_duration = 0
            if host_result.scan_start is not None and host_result.scan_end is not None:
                scan_duration = host_result.scan_end - host_result.scan_start
                
            lines.append(f"Host: {host_result.host}")
            lines.append(f"Status: {'Up' if host_result.is_alive else 'Down'}")
            lines.append(f"Scan Duration: {scan_duration:.2f}s")
            lines.append("")
            
            open_ports = [p for p in host_result.ports if p and p.state and p.state.value == "open"]
            
            if open_ports:
                lines.append("Open Ports:")
                for port in open_ports:
                    service_info = f" ({port.service})" if port.service else ""
                    banner_info = f" - {port.banner}" if port.banner else ""
                    lines.append(f"  {port.port}/tcp{service_info}{banner_info}")
            else:
                lines.append("No open ports found")
            
            lines.append("")
            lines.append("-" * 30)
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def save_report(results: List[HostResult], filename: str):
        """Save text report to file"""
        report = TextReporter.generate_report(results)
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"[*] Text report saved to: {filename}")


class ReportManager:
    """Manages different report formats"""
    
    def __init__(self):
        self.reporters = {
            'json': JSONReporter,
            'text': TextReporter,
            'txt': TextReporter
        }
    
    def generate_report(self, results: List[HostResult], format_type: str, 
                       output_file: str = None, config: Dict[str, Any] = None):
        """Generate and optionally save report in specified format"""
        
        if format_type not in self.reporters:
            raise ValueError(f"Unsupported report format: {format_type}")
        
        reporter = self.reporters[format_type]
        
        if output_file:
            # Save to file
            if format_type == 'json':
                reporter.save_report(results, output_file, config)
            else:
                reporter.save_report(results, output_file)
        else:
            # Print to console
            if format_type == 'json':
                report = reporter.generate_report(results, config)
                print(json.dumps(report, indent=2))
            else:
                report = reporter.generate_report(results)
                print(report)
