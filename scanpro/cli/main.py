"""
Interactive Command Line Interface for ScanPro
"""

import sys
import os
from typing import List, Dict, Any, Optional

from ..core.models import ScanConfig, ScanType, NetworkUtils
from ..controller.scan_controller import ScanController
from ..reporting.reporters import ReportManager
from ..config.profiles import ScanProfiles, PortPresets, ConfigManager


def print_banner():
    """Print ScanPro banner"""
    print("\n" + "="*60)
    print("    ____                  ____            ")
    print("   / __/_______  ____    / __ \\_________  ")
    print("  _\\ \\/ ___/ __ \\/ __ \\  / /_/ / ___/ __ \\ ")
    print(" /___/ /__/ /_/ / / / / / ____/ /  / /_/ / ")
    print("/____/\\___/\\____/_/ /_/ /_/   /_/   \\____/  ")
    print("\n   Professional Port Scanner v1.0.0")
    print("   For Cybersecurity Professionals")
    print("="*60)


def print_legal_warning():
    """Print legal warning and disclaimer"""
    print("\n⚠️  LEGAL WARNING AND DISCLAIMER:")
    print("   • Only scan systems you own or have explicit permission to test")
    print("   • Unauthorized scanning may be illegal in your jurisdiction")
    print("   • This tool is for authorized security testing only")
    print("   • The user is solely responsible for all activities")


def prompt_targets() -> List[str]:
    """Interactive target selection"""
    print("\n📍 TARGET SELECTION")
    print("-" * 20)
    print("Enter target(s) to scan:")
    print("  • Single IP: 192.168.1.1")
    print("  • Multiple IPs: 192.168.1.1,192.168.1.2")
    print("  • IP range: 192.168.1.1-192.168.1.10")
    print("  • CIDR notation: 192.168.1.0/24")
    print("  • Hostname: example.com")
    print("  • File path: targets.txt (one target per line)")
    print("  • Safe testing: 127.0.0.1 or localhost")
    
    while True:
        target_input = input("\nTargets: ").strip()
        if not target_input:
            print("❌ Please enter at least one target.")
            continue
        
        # Check if it's a file path
        if os.path.isfile(target_input):
            try:
                targets = load_targets_from_file(target_input)
                print(f"✅ Loaded {len(targets)} targets from file")
                return targets
            except Exception as e:
                print(f"❌ Error reading file: {e}")
                continue
        
        # Parse targets
        try:
            targets = []
            for target in target_input.split(','):
                targets.extend(NetworkUtils.parse_targets(target.strip()))
            
            if targets:
                print(f"✅ Parsed {len(targets)} targets")
                return targets
            else:
                print("❌ No valid targets found. Please try again.")
        except Exception as e:
            print(f"❌ Error parsing targets: {e}")


def check_target_safety(targets: List[str]) -> bool:
    """Check if targets are safe and get user confirmation if needed"""
    # Define safe local/VM networks
    safe_networks = [
        '127.0.0.1', '::1', 'localhost',
        '192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.',
        '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
        '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.'
    ]
    
    # Check if any targets are outside safe networks
    unsafe_targets = []
    for target in targets:
        if not any(target.startswith(safe) for safe in safe_networks):
            unsafe_targets.append(target)
    
    if unsafe_targets:
        print(f"\n⚠️  WARNING: External targets detected:")
        for target in unsafe_targets:
            print(f"   • {target}")
        
        print(f"\n   These targets are outside common local/VM networks.")
        print(f"   Ensure you have explicit permission to scan these systems!")
        
        while True:
            response = input("\n   Do you have permission to scan these targets? (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                print("   ❌ Scan cancelled for safety.")
                return False
            else:
                print("   Please answer 'yes' or 'no'")
    
    return True


def prompt_ports() -> List[int]:
    """Interactive port selection"""
    print("\n🔍 PORT SELECTION")
    print("-" * 17)
    print("Available port presets:")
    
    presets = PortPresets.list_presets()
    for i, (name, count) in enumerate(presets.items(), 1):
        print(f"  {i}. {name:<10} - {count} ports")
    
    print(f"  {len(presets)+1}. custom     - Enter custom ports")
    
    while True:
        try:
            choice = input(f"\nSelect option (1-{len(presets)+1}): ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                preset_names = list(presets.keys())
                
                if 1 <= choice_num <= len(presets):
                    preset_name = preset_names[choice_num - 1]
                    ports = PortPresets.get_preset(preset_name)
                    print(f"✅ Selected {preset_name} preset ({len(ports)} ports)")
                    return ports
                
                elif choice_num == len(presets) + 1:
                    # Custom ports
                    print("\nEnter custom ports:")
                    print("  • Single port: 80")
                    print("  • Multiple ports: 80,443,8080")
                    print("  • Port range: 1-1000")
                    print("  • Mixed: 22,80,443,8000-8100")
                    
                    port_input = input("\nPorts: ").strip()
                    if not port_input:
                        print("❌ Please enter ports.")
                        continue
                    
                    ports = NetworkUtils.parse_ports(port_input)
                    if ports:
                        print(f"✅ Parsed {len(ports)} ports")
                        return ports
                    else:
                        print("❌ No valid ports found.")
                
                else:
                    print(f"❌ Please enter a number between 1 and {len(presets)+1}")
            
            else:
                print("❌ Please enter a valid number.")
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


def prompt_scan_profile() -> Optional[str]:
    """Interactive scan profile selection"""
    print("\n⚙️  SCAN PROFILE")
    print("-" * 15)
    print("Available scan profiles:")
    
    profiles = ScanProfiles.list_profiles()
    profile_names = list(profiles.keys())
    
    for i, (name, desc) in enumerate(profiles.items(), 1):
        print(f"  {i}. {name:<12} - {desc}")
    
    print(f"  {len(profiles)+1}. custom      - Configure manually")
    
    while True:
        try:
            choice = input(f"\nSelect profile (1-{len(profiles)+1}): ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(profiles):
                    profile_name = profile_names[choice_num - 1]
                    print(f"✅ Selected {profile_name} profile")
                    return profile_name
                
                elif choice_num == len(profiles) + 1:
                    print("✅ Custom configuration selected")
                    return None
                
                else:
                    print(f"❌ Please enter a number between 1 and {len(profiles)+1}")
            
            else:
                print("❌ Please enter a valid number.")
                
        except Exception as e:
            print(f"❌ Error: {e}")


def prompt_custom_config() -> Dict[str, Any]:
    """Interactive custom configuration"""
    print("\n🔧 CUSTOM CONFIGURATION")
    print("-" * 22)
    
    config = {}
    
    # Timeout
    while True:
        try:
            timeout_input = input("Connection timeout in seconds [3.0]: ").strip()
            if not timeout_input:
                config['timeout'] = 3.0
                break
            
            timeout = float(timeout_input)
            if 0.1 <= timeout <= 60.0:
                config['timeout'] = timeout
                break
            else:
                print("❌ Timeout must be between 0.1 and 60.0 seconds")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Threads
    while True:
        try:
            threads_input = input("Number of concurrent threads [100]: ").strip()
            if not threads_input:
                config['threads'] = 100
                break
            
            threads = int(threads_input)
            if 1 <= threads <= 1000:
                config['threads'] = threads
                break
            else:
                print("❌ Threads must be between 1 and 1000")
        except ValueError:
            print("❌ Please enter a valid integer")
    
    # Delay
    while True:
        try:
            delay_input = input("Delay between requests in seconds [0.0]: ").strip()
            if not delay_input:
                config['delay'] = 0.0
                break
            
            delay = float(delay_input)
            if 0.0 <= delay <= 10.0:
                config['delay'] = delay
                break
            else:
                print("❌ Delay must be between 0.0 and 10.0 seconds")
        except ValueError:
            print("❌ Please enter a valid number")
    
    return config


def prompt_output_options() -> Dict[str, Any]:
    """Interactive output configuration"""
    print("\n💾 OUTPUT OPTIONS")
    print("-" * 16)
    
    config = {}
    
    # Verbosity
    print("Select output verbosity:")
    print("  1. Normal  - Standard output")
    print("  2. Verbose - Detailed output")
    print("  3. Quiet   - Minimal output")
    
    while True:
        try:
            choice = input("\nVerbosity (1-3) [1]: ")

            if not choice:
                choice = "1"
            
            if choice == "1":
                config['verbose'] = False
                config['quiet'] = False
                break
            elif choice == "2":
                config['verbose'] = True
                config['quiet'] = False
                break
            elif choice == "3":
                config['verbose'] = False
                config['quiet'] = True
                break
            else:
                print("❌ Please enter 1, 2, or 3")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Output file
    save_output = input("\nSave results to file? (y/n) [n]: ").strip().lower()
    if save_output in ['y', 'yes']:
        while True:
            filename = input("Output filename (e.g., results.json, report.txt): ").strip()
            if filename:
                config['output_file'] = filename
                
                # Determine format from extension
                if filename.endswith('.json'):
                    config['output_format'] = 'json'
                elif filename.endswith('.txt'):
                    config['output_format'] = 'text'
                else:
                    print("Format options:")
                    print("  1. JSON")
                    print("  2. Text")
                    
                    format_choice = input("Select format (1-2): ").strip()
                    if format_choice == "1":
                        config['output_format'] = 'json'
                    elif format_choice == "2":
                        config['output_format'] = 'text'
                    else:
                        print("❌ Invalid choice, defaulting to text")
                        config['output_format'] = 'text'
                
                print(f"✅ Output will be saved to {filename}")
                break
            else:
                print("❌ Please enter a filename")
    
    return config


def load_targets_from_file(filename: str) -> List[str]:
    """Load targets from file"""
    try:
        with open(filename, 'r') as f:
            targets = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return targets
    except FileNotFoundError:
        print(f"❌ Target file '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading target file: {e}")
        sys.exit(1)


def interactive_scan_config() -> ScanConfig:
    """Create scan configuration through interactive prompts"""
    
    # Get targets
    targets = prompt_targets()
    
    # Safety check
    if not check_target_safety(targets):
        sys.exit(1)
    
    # Get ports
    ports = prompt_ports()
    
    # Get scan profile
    profile_name = prompt_scan_profile()
    
    # Start with default configuration
    config_dict = {
        'timeout': None,
        'threads': None,
        'delay': None,
        'verbose': False,
        'quiet': False,
        'output_format': 'text',
        'output_file': None
    }
    
    # Apply profile if selected
    if profile_name:
        config_dict = ConfigManager.apply_profile(config_dict, profile_name)
    else:
        # Get custom configuration
        custom_config = prompt_custom_config()
        config_dict.update(custom_config)
    
    # Get output options
    output_config = prompt_output_options()
    config_dict.update(output_config)
    
    # Validate and sanitize configuration
    config_dict = ConfigManager.validate_config(config_dict)
    
    # Create scan configuration
    return ScanConfig(
        targets=targets,
        ports=ports,
        scan_type=config_dict.get('scan_type', ScanType.TCP_CONNECT),
        timeout=config_dict.get('timeout', 3.0),
        threads=config_dict.get('threads', 100),
        delay=config_dict.get('delay', 0.0),
        verbose=config_dict.get('verbose', False),
        output_format=config_dict.get('output_format', 'text'),
        output_file=config_dict.get('output_file')
    )


def show_scan_summary(config: ScanConfig):
    """Display scan configuration summary"""
    print("\n📋 SCAN SUMMARY")
    print("-" * 14)
    print(f"Targets:      {len(config.targets)} host(s)")
    if len(config.targets) <= 5:
        for target in config.targets:
            print(f"              • {target}")
    else:
        for target in config.targets[:3]:
            print(f"              • {target}")
        print(f"              ... and {len(config.targets) - 3} more")
    
    print(f"Ports:        {len(config.ports)} port(s)")
    print(f"Timeout:      {config.timeout}s")
    print(f"Threads:      {config.threads}")
    print(f"Delay:        {config.delay}s")
    print(f"Output:       {'Verbose' if config.verbose else 'Quiet' if hasattr(config, 'quiet') else 'Normal'}")
    if config.output_file:
        print(f"Save to:      {config.output_file}")
    
    print(f"\nEstimated scan time: ~{(len(config.targets) * len(config.ports) * config.timeout) / config.threads:.1f}s")


def main():
    """Main interactive CLI entry point"""
    try:
        # Print banner and legal warning
        print_banner()
        print_legal_warning()
        
        # Get user confirmation to proceed
        print(f"\nPress Enter to continue or Ctrl+C to exit...")
        input()
        
        # Interactive configuration
        config = interactive_scan_config()
        
        # Show scan summary
        show_scan_summary(config)
        
        # Final confirmation
        while True:
            proceed = input(f"\n🚀 Start scan? (y/n): ").strip().lower()
            if proceed in ['y', 'yes']:
                break
            elif proceed in ['n', 'no']:
                print("❌ Scan cancelled by user")
                return
            else:
                print("Please answer 'y' or 'n'")
        
        # Execute scan
        print(f"\n🔍 Starting scan...")
        print("-" * 20)
        
        controller = ScanController(config)
        results = controller.execute_scan()
        
        # Generate reports
        report_manager = ReportManager()
        
        # Create configuration dict for JSON report
        config_dict = {
            'scan_type': config.scan_type.value,
            'timeout': config.timeout,
            'threads': config.threads,
            'delay': config.delay,
            'total_targets': len(config.targets),
            'total_ports': len(config.ports)
        }
        
        # Generate and save report
        quiet_mode = hasattr(config, 'quiet') and getattr(config, 'quiet', False)
        if not quiet_mode:
            print()  # Add spacing before report
        
        report_manager.generate_report(
            results, 
            config.output_format, 
            config.output_file,
            config_dict
        )
        
        print(f"\n✅ Scan completed successfully!")
        if config.output_file:
            print(f"   Results saved to: {config.output_file}")
        
    except KeyboardInterrupt:
        print(f"\n❌ Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
