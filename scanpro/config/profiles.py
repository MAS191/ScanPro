"""
Configuration profiles and settings for ScanPro
"""

from typing import Dict, Any
from ..core.models import ScanType


class ScanProfiles:
    """Predefined scan profiles for different use cases"""
    
    PROFILES = {
        'default': {
            'timeout': 3.0,
            'threads': 100,
            'delay': 0.0,
            'scan_type': ScanType.TCP_CONNECT,
            'description': 'Default balanced scan profile'
        },
        
        'fast': {
            'timeout': 1.0,
            'threads': 200,
            'delay': 0.0,
            'scan_type': ScanType.TCP_CONNECT,
            'description': 'Fast scan with reduced timeout and high concurrency'
        },
        
        'slow': {
            'timeout': 10.0,
            'threads': 50,
            'delay': 0.1,
            'scan_type': ScanType.TCP_CONNECT,
            'description': 'Slow, careful scan to avoid detection'
        },
        
        'stealth': {
            'timeout': 5.0,
            'threads': 25,
            'delay': 0.5,
            'scan_type': ScanType.TCP_CONNECT,
            'description': 'Stealthy scan with delays between requests'
        },
        
        'aggressive': {
            'timeout': 2.0,
            'threads': 300,
            'delay': 0.0,
            'scan_type': ScanType.TCP_CONNECT,
            'description': 'Aggressive scan for maximum speed'
        }
    }
    
    @classmethod
    def get_profile(cls, profile_name: str) -> Dict[str, Any]:
        """Get scan profile configuration"""
        if profile_name not in cls.PROFILES:
            raise ValueError(f"Unknown profile: {profile_name}. Available: {list(cls.PROFILES.keys())}")
        
        return cls.PROFILES[profile_name].copy()
    
    @classmethod
    def list_profiles(cls) -> Dict[str, str]:
        """List available profiles with descriptions"""
        return {name: config['description'] for name, config in cls.PROFILES.items()}


class PortPresets:
    """Common port sets for scanning"""
    
    PRESETS = {
        'top20': [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443],
        
        'top100': [
            7, 9, 13, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113, 119, 135,
            139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543, 544, 548,
            554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433,
            1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986,
            4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000,
            6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768,
            49152, 49153, 49154, 49155, 49156, 49157
        ],
        
        'web': [80, 443, 8000, 8008, 8080, 8081, 8443, 8888, 9000, 9090],
        
        'mail': [25, 110, 143, 465, 587, 993, 995],
        
        'db': [1433, 1521, 3306, 5432, 27017, 6379],
        
        'remote': [22, 23, 3389, 5900, 5901, 5902],
        
        'all': list(range(1, 65536))
    }
    
    @classmethod
    def get_preset(cls, preset_name: str) -> list:
        """Get port preset"""
        if preset_name not in cls.PRESETS:
            raise ValueError(f"Unknown preset: {preset_name}. Available: {list(cls.PRESETS.keys())}")
        
        return cls.PRESETS[preset_name].copy()
    
    @classmethod
    def list_presets(cls) -> Dict[str, int]:
        """List available presets with port counts"""
        return {name: len(ports) for name, ports in cls.PRESETS.items()}


class ConfigManager:
    """Manages configuration loading and validation"""
    
    @staticmethod
    def apply_profile(config_dict: Dict[str, Any], profile_name: str) -> Dict[str, Any]:
        """Apply a scan profile to configuration"""
        profile = ScanProfiles.get_profile(profile_name)
        
        # Profile settings override defaults but not explicit user settings
        for key, value in profile.items():
            if key not in config_dict or config_dict[key] is None:
                config_dict[key] = value
        
        return config_dict
    
    @staticmethod
    def validate_config(config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize configuration"""
        # Handle None values by providing defaults
        timeout = config_dict.get('timeout')
        if timeout is None:
            timeout = 3.0
        
        threads = config_dict.get('threads')
        if threads is None:
            threads = 100
            
        delay = config_dict.get('delay')
        if delay is None:
            delay = 0.0
        
        # Ensure reasonable limits
        config_dict['timeout'] = max(0.1, min(timeout, 60.0))
        config_dict['threads'] = max(1, min(threads, 1000))
        config_dict['delay'] = max(0.0, min(delay, 10.0))
        
        return config_dict
