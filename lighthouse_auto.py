#!/usr/bin/env python3
"""
Fully Automated Lighthouse Script with API Key & Sensitive Data Extraction
A comprehensive security auditing tool for web applications

This script performs:
1. Google Lighthouse performance audits
2. Extraction of API keys, tokens, and credentials
3. Detection of private keys and sensitive data
4. Web crawling and deep analysis
5. Automated reporting

DISCLAIMER: This tool is for authorized security auditing and educational purposes only.
Unauthorized access to computer systems is illegal.
"""

import re
import json
import subprocess
import sys
import os
import argparse
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required packages not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "requests", "beautifulsoup4"])
    # Add user site-packages to path
    import site
    import importlib
    site.main()
    importlib.invalidate_caches()
    import requests
    from bs4 import BeautifulSoup


class LighthouseAutoScanner:
    """Automated Lighthouse scanner with API key extraction capabilities"""
    
    # Comprehensive regex patterns for detecting API keys and sensitive data
    PATTERNS = {
        'aws_access_key': r'AKIA[0-9A-Z]{16}',
        'aws_secret_key': r'aws(.{0,20})?[\'"][0-9a-zA-Z/+]{40}[\'"]',
        'github_token': r'gh[ps]_[a-zA-Z0-9]{36,}',
        'github_oauth': r'[a-zA-Z0-9_-]*:[a-zA-Z0-9_-]+@github\.com*',
        'google_api_key': r'AIza[0-9A-Za-z\-_]{35,}',
        'google_oauth': r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com',
        'stripe_key': r'sk_live_[0-9a-zA-Z]{24,}',
        'stripe_restricted': r'rk_live_[0-9a-zA-Z]{24,}',
        'slack_token': r'xox[pborsa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}',
        'slack_webhook': r'https://hooks\.slack\.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}',
        'twilio_api_key': r'SK[0-9a-fA-F]{32}',
        'twilio_account_sid': r'AC[a-zA-Z0-9_\\-]{32}',
        'mailgun_api_key': r'key-[0-9a-zA-Z]{32}',
        'paypal_braintree': r'access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}',
        'square_oauth': r'sq0atp-[0-9A-Za-z\\-_]{22}',
        'square_access_token': r'sqOatp-[0-9A-Za-z\\-_]{22}',
        'heroku_api_key': r'[hH][eE][rR][oO][kK][uU].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}',
        'firebase': r'AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}',
        'generic_api_key': r'api[_]?key.*[\'"][0-9a-zA-Z]{32,45}[\'"]',
        'generic_secret': r'secret.*[\'"][0-9a-zA-Z]{32,45}[\'"]',
        'rsa_private_key': r'-----BEGIN RSA PRIVATE KEY-----',
        'ssh_private_key': r'-----BEGIN OPENSSH PRIVATE KEY-----',
        'dsa_private_key': r'-----BEGIN DSA PRIVATE KEY-----',
        'ec_private_key': r'-----BEGIN EC PRIVATE KEY-----',
        'pgp_private_key': r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
        'jwt_token': r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
        'password_in_url': r'[a-zA-Z]{3,10}://[^/\s:@]{3,20}:[^/\s:@]{3,20}@.{1,100}["\'\s]',
        'connection_string': r'(mongodb|mysql|postgres|jdbc)://[^\s]+',
        'bearer_token': r'[Bb]earer [a-zA-Z0-9_\-\.=]+',
        'basic_auth': r'[Bb]asic [a-zA-Z0-9_\-\.=]+',
    }
    
    def __init__(self, target_url, output_dir='./lighthouse_results'):
        """Initialize the scanner with a target URL"""
        self.target_url = target_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.findings = {
            'api_keys': [],
            'private_keys': [],
            'tokens': [],
            'credentials': [],
            'sensitive_strings': []
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # SSL verification (set to True for production, False for testing)
        self.verify_ssl = False  # Can be made configurable via command line argument
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_lighthouse(self):
        """Run Google Lighthouse audit on the target URL"""
        print(f"\n[*] Running Lighthouse audit on {self.target_url}...")
        
        # Check if lighthouse is installed
        try:
            subprocess.run(['lighthouse', '--version'], 
                          capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[!] Lighthouse not found. Installing via npm...")
            try:
                subprocess.run(['npm', 'install', '-g', 'lighthouse'], check=True)
            except Exception as e:
                print(f"[!] Could not install Lighthouse: {e}")
                print("[!] Please install manually: npm install -g lighthouse")
                return None
        
        # Run Lighthouse
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(self.output_dir, f'lighthouse_report_{timestamp}.json')
        
        try:
            cmd = [
                'lighthouse',
                self.target_url,
                '--output=json',
                '--output-path=' + output_file,
                '--chrome-flags="--headless"',
                '--quiet'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if os.path.exists(output_file):
                print(f"[+] Lighthouse report saved to: {output_file}")
                with open(output_file, 'r') as f:
                    return json.load(f)
            else:
                print("[!] Lighthouse report not generated")
                return None
                
        except subprocess.TimeoutExpired:
            print("[!] Lighthouse scan timed out")
            return None
        except Exception as e:
            print(f"[!] Error running Lighthouse: {e}")
            return None
    
    def extract_sensitive_data(self, content, url):
        """Extract API keys and sensitive data from content"""
        findings_count = 0
        
        for key_type, pattern in self.PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                finding = {
                    'type': key_type,
                    'value': match.group(0)[:100],  # Truncate long matches
                    'url': url,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Categorize findings
                if 'private_key' in key_type or 'ssh' in key_type:
                    self.findings['private_keys'].append(finding)
                elif 'token' in key_type or 'jwt' in key_type or 'bearer' in key_type:
                    self.findings['tokens'].append(finding)
                elif 'password' in key_type or 'auth' in key_type or 'connection' in key_type:
                    self.findings['credentials'].append(finding)
                elif 'api_key' in key_type or 'secret' in key_type:
                    self.findings['api_keys'].append(finding)
                else:
                    self.findings['sensitive_strings'].append(finding)
                
                findings_count += 1
        
        return findings_count
    
    def scan_page(self, url, max_depth=2, current_depth=0):
        """Scan a single page for sensitive data"""
        if current_depth > max_depth or url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        print(f"[*] Scanning: {url} (depth: {current_depth})")
        
        try:
            response = self.session.get(url, timeout=10, verify=self.verify_ssl)
            response.raise_for_status()
            
            # Extract from HTML content
            findings_html = self.extract_sensitive_data(response.text, url)
            
            # Extract from inline scripts
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check inline scripts
            for script in soup.find_all('script'):
                if script.string:
                    self.extract_sensitive_data(script.string, url)
            
            # Check data attributes
            for element in soup.find_all(attrs={'data-key': True}):
                self.extract_sensitive_data(str(element), url)
            
            # Check meta tags
            for meta in soup.find_all('meta'):
                if meta.get('content'):
                    self.extract_sensitive_data(meta.get('content'), url)
            
            # Check comments
            comments = soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in str(text))
            for comment in comments:
                self.extract_sensitive_data(str(comment), url)
            
            # Extract links for crawling
            if current_depth < max_depth:
                base_domain = urlparse(self.target_url).netloc
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    parsed = urlparse(absolute_url)
                    
                    # Only crawl same domain
                    if parsed.netloc == base_domain and absolute_url not in self.visited_urls:
                        time.sleep(0.5)  # Rate limiting
                        self.scan_page(absolute_url, max_depth, current_depth + 1)
            
            if findings_html > 0:
                print(f"[+] Found {findings_html} potential sensitive items on {url}")
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Error scanning {url}: {e}")
        except Exception as e:
            print(f"[!] Unexpected error scanning {url}: {e}")
    
    def scan_javascript_files(self, url):
        """Scan external JavaScript files for sensitive data"""
        print(f"\n[*] Scanning JavaScript files from {url}...")
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            js_files = []
            for script in soup.find_all('script', src=True):
                js_url = urljoin(url, script['src'])
                js_files.append(js_url)
            
            for js_url in js_files:
                if js_url not in self.visited_urls:
                    print(f"[*] Analyzing: {js_url}")
                    self.visited_urls.add(js_url)
                    
                    try:
                        js_response = self.session.get(js_url, timeout=10)
                        findings = self.extract_sensitive_data(js_response.text, js_url)
                        if findings > 0:
                            print(f"[+] Found {findings} items in {js_url}")
                    except Exception as e:
                        print(f"[!] Error fetching {js_url}: {e}")
                    
                    time.sleep(0.5)
        
        except Exception as e:
            print(f"[!] Error scanning JavaScript files: {e}")
    
    def check_common_files(self):
        """Check for common files that may contain sensitive data"""
        print("\n[*] Checking common sensitive files...")
        
        common_files = [
            '.env',
            '.env.local',
            '.env.production',
            'config.json',
            'config.js',
            'secrets.json',
            'credentials.json',
            'settings.json',
            'app.config',
            'web.config',
            '.git/config',
            '.aws/credentials',
            'id_rsa',
            'id_dsa',
            'private.key',
            'server.key',
            'database.yml',
            'docker-compose.yml',
            '.dockerenv',
            'Dockerfile',
        ]
        
        for file in common_files:
            file_url = urljoin(self.target_url, file)
            try:
                response = self.session.get(file_url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] Found accessible file: {file_url}")
                    findings = self.extract_sensitive_data(response.text, file_url)
                    if findings > 0:
                        print(f"[+] Extracted {findings} sensitive items from {file}")
            except (requests.exceptions.RequestException, Exception):
                pass  # File doesn't exist or not accessible
    
    def generate_report(self):
        """Generate comprehensive security report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.output_dir, f'security_report_{timestamp}.json')
        
        report = {
            'scan_info': {
                'target_url': self.target_url,
                'scan_date': datetime.now().isoformat(),
                'pages_scanned': len(self.visited_urls),
            },
            'findings': self.findings,
            'statistics': {
                'total_api_keys': len(self.findings['api_keys']),
                'total_private_keys': len(self.findings['private_keys']),
                'total_tokens': len(self.findings['tokens']),
                'total_credentials': len(self.findings['credentials']),
                'total_sensitive_strings': len(self.findings['sensitive_strings']),
            }
        }
        
        # Save JSON report
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[+] Security report saved to: {report_file}")
        
        # Generate text summary
        self.print_summary(report)
        
        return report_file
    
    def print_summary(self, report):
        """Print summary of findings"""
        print("\n" + "="*70)
        print("LIGHTHOUSE AUTO SCANNER - SECURITY AUDIT SUMMARY".center(70))
        print("="*70)
        print(f"\nTarget URL: {self.target_url}")
        print(f"Scan Date: {report['scan_info']['scan_date']}")
        print(f"Pages Scanned: {report['scan_info']['pages_scanned']}")
        print("\n" + "-"*70)
        print("FINDINGS:".ljust(40))
        print("-"*70)
        
        stats = report['statistics']
        print(f"  API Keys Found:".ljust(40) + f"{stats['total_api_keys']}")
        print(f"  Private Keys Found:".ljust(40) + f"{stats['total_private_keys']}")
        print(f"  Tokens Found:".ljust(40) + f"{stats['total_tokens']}")
        print(f"  Credentials Found:".ljust(40) + f"{stats['total_credentials']}")
        print(f"  Sensitive Strings Found:".ljust(40) + f"{stats['total_sensitive_strings']}")
        
        total = sum(stats.values())
        print("\n" + "-"*70)
        print(f"TOTAL SENSITIVE ITEMS: {total}".center(70))
        print("="*70)
        
        if total > 0:
            print("\n[!] WARNING: Sensitive data detected!")
            print("[!] Review the detailed report for security risks.")
            print("[!] Immediately rotate/revoke any exposed credentials.")
        else:
            print("\n[+] No obvious sensitive data detected.")
            print("[+] However, manual review is still recommended.")
    
    def run_full_scan(self, include_lighthouse=True, crawl_depth=2):
        """Run complete automated scan"""
        print("\n" + "="*70)
        print("LIGHTHOUSE AUTO SCANNER - STARTING FULL SCAN".center(70))
        print("="*70)
        print(f"\nTarget: {self.target_url}")
        print(f"Crawl Depth: {crawl_depth}")
        print(f"Lighthouse: {'Enabled' if include_lighthouse else 'Disabled'}")
        print("\n" + "="*70)
        
        # Step 1: Run Lighthouse if enabled
        lighthouse_report = None
        if include_lighthouse:
            lighthouse_report = self.run_lighthouse()
        
        # Step 2: Crawl and scan pages
        print("\n[*] Starting web crawling and sensitive data extraction...")
        self.scan_page(self.target_url, max_depth=crawl_depth)
        
        # Step 3: Scan JavaScript files
        self.scan_javascript_files(self.target_url)
        
        # Step 4: Check common sensitive files
        self.check_common_files()
        
        # Step 5: Generate report
        report_file = self.generate_report()
        
        print("\n[+] Scan completed successfully!")
        print(f"[+] Results saved to: {self.output_dir}")
        
        return report_file


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description='Fully Automated Lighthouse Scanner with API Key Extraction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic scan with Lighthouse
  python lighthouse_auto.py https://example.com
  
  # Scan without Lighthouse (faster)
  python lighthouse_auto.py https://example.com --no-lighthouse
  
  # Deep crawl with depth 3
  python lighthouse_auto.py https://example.com --depth 3
  
  # Custom output directory
  python lighthouse_auto.py https://example.com --output ./my_results
  
DISCLAIMER: Use only on authorized targets. Unauthorized access is illegal.
        """
    )
    
    parser.add_argument('url', help='Target URL to scan')
    parser.add_argument('--depth', type=int, default=2,
                       help='Crawl depth (default: 2)')
    parser.add_argument('--output', default='./lighthouse_results',
                       help='Output directory (default: ./lighthouse_results)')
    parser.add_argument('--no-lighthouse', action='store_true',
                       help='Skip Lighthouse audit (faster)')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Create scanner and run
    scanner = LighthouseAutoScanner(args.url, args.output)
    
    try:
        scanner.run_full_scan(
            include_lighthouse=not args.no_lighthouse,
            crawl_depth=args.depth
        )
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        print("[*] Generating partial report...")
        scanner.generate_report()
    except Exception as e:
        print(f"\n[!] Error during scan: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
