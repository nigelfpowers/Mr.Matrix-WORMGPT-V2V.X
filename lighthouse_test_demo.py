#!/usr/bin/env python3
"""
Test/Demo script for Lighthouse Auto Scanner
Demonstrates the API key detection patterns without requiring a real website
"""

import re

# Import patterns from the main script
PATTERNS = {
    'aws_access_key': r'AKIA[0-9A-Z]{16}',
    'github_token': r'gh[ps]_[a-zA-Z0-9]{36,}',
    'google_api_key': r'AIza[0-9A-Za-z\-_]{35,}',
    'stripe_key': r'sk_live_[0-9a-zA-Z]{24,}',
    'jwt_token': r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
    'rsa_private_key': r'-----BEGIN RSA PRIVATE KEY-----',
    'ssh_private_key': r'-----BEGIN OPENSSH PRIVATE KEY-----',
}

# Test data with example patterns (these are fake/example keys, not real)
test_samples = [
    ("AWS Access Key", "const awsKey = 'AKIAIOSFODNN7EXAMPLE';"),
    ("GitHub Token", "GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwxyz"),
    ("Google API Key", "const googleKey = 'AIzaSyDaGmWKa4JsXZ-HjGw7ISLn_3namBG';"),
    ("Stripe Live Key", "sk_live_abcdefghijklmnop123456"),
    ("JWT Token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"),
    ("RSA Private Key", "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA..."),
    ("API in JS", "var apiKey = 'AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234';"),
    ("Connection String", "mongodb://user:password@localhost:27017/mydb"),
]

def test_pattern_detection():
    """Test the pattern detection on sample data"""
    print("="*70)
    print("LIGHTHOUSE AUTO SCANNER - PATTERN DETECTION TEST".center(70))
    print("="*70)
    print("\nTesting API key and sensitive data detection patterns...\n")
    
    total_detected = 0
    
    for test_name, test_string in test_samples:
        print(f"\n[Testing] {test_name}")
        print(f"Sample: {test_string[:60]}...")
        
        detected = False
        for key_type, pattern in PATTERNS.items():
            matches = re.finditer(pattern, test_string, re.IGNORECASE)
            for match in matches:
                detected = True
                total_detected += 1
                print(f"  ✓ Detected as: {key_type}")
                print(f"    Match: {match.group(0)[:50]}...")
        
        if not detected:
            print(f"  ✗ No pattern matched (this may need attention)")
    
    print("\n" + "="*70)
    print(f"Total Detections: {total_detected}")
    print("="*70)
    
    if total_detected >= len(test_samples) * 0.8:  # At least 80% detected
        print("\n[+] Pattern detection working correctly!")
        return True
    else:
        print("\n[!] Some patterns may need adjustment")
        return False

def demonstrate_usage():
    """Demonstrate how to use the lighthouse_auto.py script"""
    print("\n" + "="*70)
    print("USAGE EXAMPLES".center(70))
    print("="*70)
    
    examples = [
        ("Basic Scan", "python lighthouse_auto.py https://example.com"),
        ("No Lighthouse (faster)", "python lighthouse_auto.py https://example.com --no-lighthouse"),
        ("Deep Scan", "python lighthouse_auto.py https://example.com --depth 3"),
        ("Custom Output", "python lighthouse_auto.py https://example.com --output ./my_reports"),
        ("Combined Options", "python lighthouse_auto.py https://example.com --no-lighthouse --depth 1 --output ./quick_scan"),
    ]
    
    for name, command in examples:
        print(f"\n{name}:")
        print(f"  $ {command}")
    
    print("\n" + "="*70)

def show_detected_types():
    """Show all types of sensitive data that can be detected"""
    print("\n" + "="*70)
    print("DETECTABLE SENSITIVE DATA TYPES".center(70))
    print("="*70)
    
    categories = {
        "API Keys": [
            "AWS Access Keys & Secret Keys",
            "Google API Keys & OAuth",
            "GitHub Personal Access Tokens",
            "Stripe Live & Test Keys",
            "Slack Tokens & Webhooks",
            "Twilio API Keys",
            "Mailgun API Keys",
            "PayPal Braintree Tokens",
            "Square OAuth Tokens",
            "Heroku API Keys",
            "Firebase Tokens",
        ],
        "Private Keys": [
            "RSA Private Keys",
            "SSH Private Keys",
            "DSA Private Keys",
            "EC Private Keys",
            "PGP Private Keys",
        ],
        "Tokens & Credentials": [
            "JWT Tokens",
            "Bearer Tokens",
            "Basic Authentication",
            "Passwords in URLs",
            "Database Connection Strings",
        ]
    }
    
    for category, items in categories.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║        Lighthouse Auto Scanner - Test & Demo Script               ║
║                                                                    ║
║        This script demonstrates the pattern detection              ║
║        capabilities without scanning a real website                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run tests
    test_pattern_detection()
    
    # Show detectable types
    show_detected_types()
    
    # Show usage examples
    demonstrate_usage()
    
    print("\n" + "="*70)
    print("To run a real scan, use:")
    print("  python lighthouse_auto.py https://your-website.com")
    print("\nFor full documentation, see:")
    print("  LIGHTHOUSE_README.md")
    print("="*70 + "\n")
