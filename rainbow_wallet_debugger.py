#!/usr/bin/env python3
"""
Rainbow Wallet Debugger Script
A comprehensive debugging tool for Rainbow wallet that can run locally on mobile devices.
Compatible with Termux and standard Python environments.

Author: Mr. Matrix - WORMGPT-V2V.X
License: MIT
"""

import json
import os
import sys
import time
import socket
import platform
from datetime import datetime
from typing import Dict, List, Optional

# Color codes for terminal output (works on most mobile terminals)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class RainbowWalletDebugger:
    """Main debugger class for Rainbow wallet diagnostics"""
    
    def __init__(self):
        self.debug_log = []
        self.start_time = datetime.now()
        self.test_results = {}
        
    def print_banner(self):
        """Display the debugger banner"""
        banner = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════════╗
║       Rainbow Wallet Debugger - Mr. Matrix Edition       ║
║                   Mobile-Friendly Version                 ║
╚═══════════════════════════════════════════════════════════╝{Colors.ENDC}
{Colors.OKCYAN}Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
Platform: {platform.system()} {platform.release()}{Colors.ENDC}
"""
        print(banner)
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.debug_log.append(log_entry)
        
        # Color coding based on level
        if level == "ERROR":
            print(f"{Colors.FAIL}{log_entry}{Colors.ENDC}")
        elif level == "WARNING":
            print(f"{Colors.WARNING}{log_entry}{Colors.ENDC}")
        elif level == "SUCCESS":
            print(f"{Colors.OKGREEN}{log_entry}{Colors.ENDC}")
        else:
            print(log_entry)
    
    def check_network_connectivity(self) -> bool:
        """Check internet connectivity"""
        self.log("Checking network connectivity...", "INFO")
        
        test_hosts = [
            ("ethereum.org", 443),
            ("infura.io", 443),
            ("cloudflare.com", 443),
            ("google.com", 443)
        ]
        
        results = []
        for host, port in test_hosts:
            try:
                socket.create_connection((host, port), timeout=5)
                self.log(f"✓ Connection to {host}:{port} successful", "SUCCESS")
                results.append(True)
            except (socket.timeout, socket.error) as e:
                self.log(f"✗ Connection to {host}:{port} failed: {e}", "ERROR")
                results.append(False)
        
        success_rate = (sum(results) / len(results)) * 100
        self.test_results['network_connectivity'] = success_rate
        
        if success_rate >= 50:
            self.log(f"Network connectivity: {success_rate:.0f}% ({sum(results)}/{len(results)} hosts reachable)", "SUCCESS")
            return True
        else:
            self.log(f"Network connectivity issues detected: Only {success_rate:.0f}% of hosts reachable", "WARNING")
            return False
    
    def check_ethereum_rpc_endpoints(self) -> Dict[str, bool]:
        """Check connectivity to common Ethereum RPC endpoints"""
        self.log("Checking Ethereum RPC endpoints...", "INFO")
        
        endpoints = [
            "mainnet.infura.io",
            "eth-mainnet.g.alchemy.com",
            "cloudflare-eth.com",
            "rpc.ankr.com"
        ]
        
        results = {}
        for endpoint in endpoints:
            try:
                socket.create_connection((endpoint, 443), timeout=5)
                self.log(f"✓ RPC endpoint {endpoint} is reachable", "SUCCESS")
                results[endpoint] = True
            except (socket.timeout, socket.error) as e:
                self.log(f"✗ RPC endpoint {endpoint} is unreachable: {e}", "ERROR")
                results[endpoint] = False
        
        self.test_results['rpc_endpoints'] = results
        return results
    
    def check_local_storage(self) -> bool:
        """Check for Rainbow wallet local storage and common issues"""
        self.log("Checking for local storage issues...", "INFO")
        
        # Common Rainbow wallet storage locations
        storage_paths = [
            os.path.expanduser("~/.rainbow"),
            os.path.expanduser("~/Library/Application Support/Rainbow"),
            os.path.expanduser("~/.config/rainbow"),
            "/data/data/me.rainbow/files"  # Android
        ]
        
        found_storage = False
        for path in storage_paths:
            if os.path.exists(path):
                self.log(f"✓ Found wallet storage at: {path}", "SUCCESS")
                found_storage = True
                
                # Check permissions
                if os.access(path, os.R_OK):
                    self.log(f"  ✓ Storage is readable", "SUCCESS")
                else:
                    self.log(f"  ✗ Storage is not readable - permission issue!", "ERROR")
                
                if os.access(path, os.W_OK):
                    self.log(f"  ✓ Storage is writable", "SUCCESS")
                else:
                    self.log(f"  ✗ Storage is not writable - permission issue!", "WARNING")
        
        if not found_storage:
            self.log("No Rainbow wallet storage found on this device", "WARNING")
            self.log("This could mean:", "INFO")
            self.log("  1. Rainbow wallet is not installed", "INFO")
            self.log("  2. Using a different storage location", "INFO")
            self.log("  3. Running on a mobile device with different paths", "INFO")
        
        self.test_results['local_storage'] = found_storage
        return found_storage
    
    def check_dns_resolution(self) -> bool:
        """Check DNS resolution for critical wallet domains"""
        self.log("Checking DNS resolution...", "INFO")
        
        domains = [
            "rainbow.me",
            "ethereum.org",
            "infura.io",
            "alchemy.com"
        ]
        
        results = []
        for domain in domains:
            try:
                ip = socket.gethostbyname(domain)
                self.log(f"✓ DNS resolution for {domain}: {ip}", "SUCCESS")
                results.append(True)
            except socket.gaierror as e:
                self.log(f"✗ DNS resolution failed for {domain}: {e}", "ERROR")
                results.append(False)
        
        success_rate = (sum(results) / len(results)) * 100
        self.test_results['dns_resolution'] = success_rate
        
        return success_rate >= 50
    
    def check_system_resources(self):
        """Check system resources and compatibility"""
        self.log("Checking system resources...", "INFO")
        
        # Python version check
        python_version = sys.version.split()[0]
        self.log(f"Python version: {python_version}", "INFO")
        
        if sys.version_info >= (3, 7):
            self.log("✓ Python version is compatible", "SUCCESS")
        else:
            self.log("✗ Python version may be too old", "WARNING")
        
        # Check available modules
        required_modules = ['json', 'socket', 'os', 'sys']
        optional_modules = ['requests', 'web3', 'eth_account']
        
        self.log("Checking required modules...", "INFO")
        for module in required_modules:
            try:
                __import__(module)
                self.log(f"✓ Module '{module}' is available", "SUCCESS")
            except ImportError:
                self.log(f"✗ Module '{module}' is missing", "ERROR")
        
        self.log("Checking optional modules for advanced features...", "INFO")
        available_optional = []
        for module in optional_modules:
            try:
                __import__(module)
                self.log(f"✓ Module '{module}' is available", "SUCCESS")
                available_optional.append(module)
            except ImportError:
                self.log(f"⚠ Module '{module}' not found (optional)", "WARNING")
        
        self.test_results['optional_modules'] = available_optional
    
    def diagnose_common_issues(self):
        """Provide diagnosis for common Rainbow wallet issues"""
        self.log("Running common issue diagnostics...", "INFO")
        
        issues = []
        
        # Network issues
        if self.test_results.get('network_connectivity', 0) < 50:
            issues.append({
                'issue': 'Poor Network Connectivity',
                'severity': 'HIGH',
                'solution': 'Check your internet connection. Try switching between WiFi and mobile data.'
            })
        
        # DNS issues
        if self.test_results.get('dns_resolution', 0) < 50:
            issues.append({
                'issue': 'DNS Resolution Problems',
                'severity': 'MEDIUM',
                'solution': 'Try changing DNS servers. Use 8.8.8.8 (Google) or 1.1.1.1 (Cloudflare).'
            })
        
        # RPC endpoint issues
        rpc_results = self.test_results.get('rpc_endpoints', {})
        if rpc_results and sum(rpc_results.values()) == 0:
            issues.append({
                'issue': 'All RPC Endpoints Unreachable',
                'severity': 'HIGH',
                'solution': 'Your device may be blocking connections to Ethereum nodes. Check firewall settings.'
            })
        
        if issues:
            self.log("\n" + "="*60, "WARNING")
            self.log("IDENTIFIED ISSUES:", "WARNING")
            self.log("="*60, "WARNING")
            
            for i, issue in enumerate(issues, 1):
                self.log(f"\n{i}. {issue['issue']} [Severity: {issue['severity']}]", "ERROR")
                self.log(f"   Solution: {issue['solution']}", "INFO")
        else:
            self.log("\n✓ No critical issues detected!", "SUCCESS")
    
    def generate_debug_report(self) -> str:
        """Generate a comprehensive debug report"""
        report = f"""
{'='*60}
        RAINBOW WALLET DEBUG REPORT
{'='*60}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform: {platform.system()} {platform.release()}
Python: {sys.version.split()[0]}

TEST RESULTS:
{'-'*60}
"""
        for test_name, result in self.test_results.items():
            report += f"{test_name}: {result}\n"
        
        report += f"\n{'-'*60}\nFULL DEBUG LOG:\n{'-'*60}\n"
        report += "\n".join(self.debug_log)
        report += f"\n{'='*60}\n"
        
        return report
    
    def save_debug_report(self, filename: Optional[str] = None):
        """Save debug report to file"""
        if filename is None:
            filename = f"rainbow_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report = self.generate_debug_report()
        
        try:
            with open(filename, 'w') as f:
                f.write(report)
            self.log(f"✓ Debug report saved to: {filename}", "SUCCESS")
        except Exception as e:
            self.log(f"✗ Failed to save report: {e}", "ERROR")
    
    def run_full_diagnostics(self):
        """Run all diagnostic tests"""
        self.print_banner()
        
        print(f"\n{Colors.BOLD}Starting comprehensive diagnostics...{Colors.ENDC}\n")
        
        # Run all checks
        self.check_system_resources()
        print()
        
        self.check_network_connectivity()
        print()
        
        self.check_dns_resolution()
        print()
        
        self.check_ethereum_rpc_endpoints()
        print()
        
        self.check_local_storage()
        print()
        
        self.diagnose_common_issues()
        
        # Summary
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}DIAGNOSTICS COMPLETE{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")
        
        # Ask to save report
        try:
            save = input(f"{Colors.OKCYAN}Save debug report to file? (y/n): {Colors.ENDC}").strip().lower()
            if save == 'y':
                self.save_debug_report()
        except (KeyboardInterrupt, EOFError):
            print("\n")
        
        print(f"\n{Colors.OKGREEN}Thank you for using Rainbow Wallet Debugger!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}For issues, visit: https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X{Colors.ENDC}\n")

def main():
    """Main entry point"""
    try:
        debugger = RainbowWalletDebugger()
        debugger.run_full_diagnostics()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Debugger interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.FAIL}Fatal error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
