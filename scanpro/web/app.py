"""
Flask web interface for ScanPro
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import threading
import time
from datetime import datetime
import uuid

from ..core.models import ScanConfig, ScanType, NetworkUtils
from ..controller.scan_controller import ScanController
from ..config.profiles import ScanProfiles, PortPresets


class ScanProWeb:
    """Web interface for ScanPro"""
    
    def __init__(self):
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self.app.secret_key = 'scanpro-web-interface-key'
        
        # Store active scans
        self.active_scans = {}
        self.completed_scans = {}
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard page"""
            return render_template('index.html',
                                 profiles=ScanProfiles.list_profiles(),
                                 presets=PortPresets.list_presets())
        
        @self.app.route('/scan', methods=['POST'])
        def start_scan():
            """Start a new scan"""
            try:
                # Get form data
                targets = request.form.get('targets', '127.0.0.1')
                ports = request.form.get('ports', 'top20')
                profile = request.form.get('profile', 'default')
                timeout = float(request.form.get('timeout', 3.0))
                threads = int(request.form.get('threads', 100))
                
                # Safety check for non-localhost targets
                target_list = NetworkUtils.parse_targets(targets)
                
                # Define safe local ranges (localhost + common VM/lab networks)
                safe_ranges = {
                    '127.0.0.1', '::1', 'localhost',
                    # VirtualBox default ranges
                    '192.168.56.0/24',  # VirtualBox Host-Only
                    # VMware default ranges  
                    '192.168.1.0/24',   # VMware NAT
                    '192.168.57.0/24',  # VMware Host-Only
                    # Docker ranges
                    '172.17.0.0/16',    # Docker default bridge
                    # Common lab ranges
                    '10.0.0.0/24',      # Common lab network
                    '192.168.0.0/24',   # Home router default
                }
                
                # Check which targets are outside safe ranges
                potentially_unsafe = []
                for target in target_list:
                    if target in ['127.0.0.1', '::1', 'localhost']:
                        continue
                    
                    # Check if target is in a safe VM/lab range
                    is_safe = False
                    try:
                        import ipaddress
                        target_ip = ipaddress.ip_address(target)
                        for safe_range in safe_ranges:
                            if '/' in safe_range:
                                if target_ip in ipaddress.ip_network(safe_range, strict=False):
                                    is_safe = True
                                    break
                            elif target == safe_range:
                                is_safe = True
                                break
                    except ValueError:
                        # Not a valid IP, treat as potentially unsafe
                        pass
                    
                    if not is_safe:
                        potentially_unsafe.append(target)
                
                # Check if user confirmed scanning potentially unsafe targets
                if potentially_unsafe:
                    confirmed = request.form.get('confirmed_scan', 'false').lower() == 'true'
                    if not confirmed:
                        return jsonify({
                            'success': False,
                            'need_confirmation': True,
                            'non_localhost_targets': potentially_unsafe,
                            'message': f'You are about to scan targets outside safe VM/lab ranges: {", ".join(potentially_unsafe)}. Please confirm you own these systems.'
                        })
                
                # Parse ports
                if ports.lower() in PortPresets.PRESETS:
                    port_list = PortPresets.get_preset(ports.lower())
                else:
                    port_list = NetworkUtils.parse_ports(ports)
                
                # Create scan configuration
                config = ScanConfig(
                    targets=target_list,
                    ports=port_list,
                    scan_type=ScanType.TCP_CONNECT,
                    timeout=timeout,
                    threads=threads,
                    verbose=False
                )
                
                # Generate scan ID
                scan_id = str(uuid.uuid4())[:8]
                
                # Store scan info
                scan_info = {
                    'id': scan_id,
                    'status': 'starting',
                    'start_time': datetime.now().isoformat(),
                    'config': {
                        'targets': target_list,
                        'ports': len(port_list),
                        'profile': profile,
                        'timeout': timeout,
                        'threads': threads
                    },
                    'results': None,
                    'progress': 0,
                    'total_ports': len(port_list) * len(target_list),
                    'scanned_ports': 0,
                    'current_target': None
                }
                
                self.active_scans[scan_id] = scan_info
                
                # Start scan in background thread
                thread = threading.Thread(
                    target=self._run_scan_background,
                    args=(scan_id, config)
                )
                thread.daemon = True
                thread.start()
                
                return jsonify({
                    'success': True,
                    'scan_id': scan_id,
                    'message': 'Scan started successfully'
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/scan/<scan_id>/status')
        def scan_status(scan_id):
            """Get scan status"""
            if scan_id in self.active_scans:
                return jsonify(self.active_scans[scan_id])
            elif scan_id in self.completed_scans:
                return jsonify(self.completed_scans[scan_id])
            else:
                return jsonify({'error': 'Scan not found'}), 404
        
        @self.app.route('/scan/<scan_id>/results')
        def scan_results(scan_id):
            """Get detailed scan results"""
            if scan_id in self.completed_scans:
                scan_info = self.completed_scans[scan_id]
                return render_template('results.html', 
                                     scan=scan_info,
                                     results=scan_info['results'])
            else:
                return redirect(url_for('index'))
        
        @self.app.route('/api/scans')
        def list_scans():
            """API endpoint to list all scans"""
            all_scans = {}
            all_scans.update(self.active_scans)
            all_scans.update(self.completed_scans)
            return jsonify(all_scans)
        
        @self.app.route('/api/scan/<scan_id>/download')
        def download_results(scan_id):
            """Download scan results as JSON"""
            if scan_id in self.completed_scans:
                scan_info = self.completed_scans[scan_id]
                results = scan_info['results']
                
                from flask import Response
                response = Response(
                    json.dumps(results, indent=2),
                    mimetype='application/json',
                    headers={'Content-Disposition': f'attachment;filename=scanpro_results_{scan_id}.json'}
                )
                return response
            else:
                return jsonify({'error': 'Scan not found'}), 404
    
    def _run_scan_background(self, scan_id, config):
        """Run scan in background thread"""
        try:
            # Update status to running
            self.active_scans[scan_id]['status'] = 'running'
            self.active_scans[scan_id]['progress'] = 5
            
            # Execute scan with progress updates
            controller = ScanController(config)
            
            # Update status to scanning
            self.active_scans[scan_id]['status'] = 'scanning' 
            self.active_scans[scan_id]['progress'] = 10
            
            # Track progress during scan
            total_targets = len(config.targets)
            for i, target in enumerate(config.targets):
                self.active_scans[scan_id]['current_target'] = target
                self.active_scans[scan_id]['progress'] = 10 + (i * 80 // total_targets)
            
            # Execute the actual scan
            results = controller.execute_scan()
            
            # Update progress to processing
            self.active_scans[scan_id]['status'] = 'processing'
            self.active_scans[scan_id]['progress'] = 90
            
            # Process results for web display
            processed_results = self._process_results(results)
            
            # Move to completed scans
            scan_info = self.active_scans.pop(scan_id)
            scan_info.update({
                'status': 'completed',
                'end_time': datetime.now().isoformat(),
                'results': processed_results,
                'progress': 100,
                'current_target': None
            })
            
            self.completed_scans[scan_id] = scan_info
            
        except Exception as e:
            # Handle scan error
            if scan_id in self.active_scans:
                scan_info = self.active_scans.pop(scan_id)
                scan_info.update({
                    'status': 'error',
                    'end_time': datetime.now().isoformat(),
                    'error': str(e),
                    'progress': 0,
                    'current_target': None
                })
                self.completed_scans[scan_id] = scan_info
    
    def _process_results(self, host_results):
        """Process scan results for web display"""
        processed = {
            'summary': {
                'total_hosts': len(host_results),
                'live_hosts': len([h for h in host_results if h.is_alive]),
                'total_ports': sum(len(h.ports) for h in host_results),
                'open_ports': sum(len([p for p in h.ports if p.state.value == 'open']) for h in host_results)
            },
            'hosts': []
        }
        
        for host_result in host_results:
            host_data = {
                'host': host_result.host,
                'is_alive': host_result.is_alive,
                'scan_duration': host_result.scan_end - host_result.scan_start if host_result.scan_end and host_result.scan_start else 0,
                'open_ports': [],
                'closed_ports': [],
                'filtered_ports': []
            }
            
            for port_result in host_result.ports:
                port_data = {
                    'port': port_result.port,
                    'service': port_result.service,
                    'banner': port_result.banner,
                    'scan_time': port_result.scan_time
                }
                
                if port_result.state.value == 'open':
                    host_data['open_ports'].append(port_data)
                elif port_result.state.value == 'closed':
                    host_data['closed_ports'].append(port_data)
                else:
                    host_data['filtered_ports'].append(port_data)
            
            processed['hosts'].append(host_data)
        
        return processed
    
    def run(self, host='127.0.0.1', port=5000, debug=False):
        """Run the Flask web server"""
        print(f"🌐 Starting ScanPro Web Server...")
        print(f"📍 Access at: http://{host}:{port}")
        print(f"🛡️  Safe targets: localhost, VMs (192.168.x.x), lab networks")
        print(f"⚠️  External targets require ownership confirmation")
        print("-" * 60)
        
        self.app.run(host=host, port=port, debug=debug, threaded=True)


def create_app():
    """Factory function to create Flask app"""
    web_app = ScanProWeb()
    return web_app.app


if __name__ == "__main__":
    web = ScanProWeb()
    web.run(debug=True)
