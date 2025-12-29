# Lighthouse Auto Scanner - Full Documentation

## Overview

The **Lighthouse Auto Scanner** is a comprehensive security auditing tool that combines Google Lighthouse performance testing with advanced API key and sensitive data extraction capabilities. This tool is designed for authorized security testing and educational purposes.

## Features

### 1. **Google Lighthouse Integration**
- Automated performance audits
- Accessibility testing
- Best practices validation
- SEO analysis
- PWA compliance checking

### 2. **API Key Detection**
Detects over 25 types of API keys and tokens including:
- AWS Access Keys & Secret Keys
- Google API Keys & OAuth tokens
- GitHub Personal Access Tokens
- Stripe API Keys (Live & Test)
- Slack Tokens & Webhooks
- Twilio API Keys & Account SIDs
- Mailgun API Keys
- PayPal Braintree tokens
- Square OAuth tokens
- Heroku API Keys
- Firebase tokens
- Generic API keys and secrets

### 3. **Private Key Detection**
Identifies various private key formats:
- RSA Private Keys
- SSH Private Keys
- DSA Private Keys
- EC Private Keys
- PGP Private Keys

### 4. **Credential Extraction**
- JWT Tokens
- Bearer Tokens
- Basic Authentication credentials
- Passwords in URLs
- Database connection strings
- MongoDB, MySQL, PostgreSQL connections

### 5. **Web Crawling**
- Configurable crawl depth
- Same-domain link following
- Rate limiting to avoid overload
- JavaScript file analysis
- Common sensitive file checking

## Installation

### Prerequisites
1. **Python 3.7+** (Python 3.12+ recommended)
2. **Node.js and npm** (for Lighthouse)
3. **Google Chrome** (for Lighthouse)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests beautifulsoup4 lxml
```

### Step 2: Install Lighthouse (Optional)
If you want to run Lighthouse audits:
```bash
npm install -g lighthouse
```

### Step 3: Make Script Executable
```bash
chmod +x lighthouse_auto.py
```

## Usage

### Basic Usage
Scan a website with default settings:
```bash
python lighthouse_auto.py https://example.com
```

### Advanced Options

#### 1. Skip Lighthouse (Faster Scanning)
```bash
python lighthouse_auto.py https://example.com --no-lighthouse
```

#### 2. Custom Crawl Depth
```bash
# Shallow scan (depth 1)
python lighthouse_auto.py https://example.com --depth 1

# Deep scan (depth 3)
python lighthouse_auto.py https://example.com --depth 3
```

#### 3. Custom Output Directory
```bash
python lighthouse_auto.py https://example.com --output ./security_reports
```

#### 4. Combined Options
```bash
python lighthouse_auto.py https://example.com \
  --no-lighthouse \
  --depth 3 \
  --output ./custom_output
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `url` | Target URL to scan (required) | - |
| `--depth N` | Crawl depth (0-5 recommended) | 2 |
| `--output DIR` | Output directory for reports | ./lighthouse_results |
| `--no-lighthouse` | Skip Lighthouse audit | False |

## Output

The scanner generates two types of reports:

### 1. Security Report (JSON)
Located at: `{output_dir}/security_report_{timestamp}.json`

Contains:
- Scan metadata (target, date, pages scanned)
- All detected API keys
- All detected private keys
- All detected tokens
- All detected credentials
- Statistical summary

### 2. Lighthouse Report (JSON) - Optional
Located at: `{output_dir}/lighthouse_report_{timestamp}.json`

Contains:
- Performance metrics
- Accessibility scores
- Best practices analysis
- SEO recommendations
- PWA compliance

## Security Report Structure

```json
{
  "scan_info": {
    "target_url": "https://example.com",
    "scan_date": "2025-12-29T05:57:42.435Z",
    "pages_scanned": 15
  },
  "findings": {
    "api_keys": [
      {
        "type": "aws_access_key",
        "value": "AKIAIOSFODNN7EXAMPLE",
        "url": "https://example.com/config.js",
        "timestamp": "2025-12-29T05:57:42.435Z"
      }
    ],
    "private_keys": [...],
    "tokens": [...],
    "credentials": [...],
    "sensitive_strings": [...]
  },
  "statistics": {
    "total_api_keys": 3,
    "total_private_keys": 1,
    "total_tokens": 5,
    "total_credentials": 2,
    "total_sensitive_strings": 4
  }
}
```

## How It Works

### 1. **Lighthouse Audit** (Optional)
- Runs Google Lighthouse CLI
- Generates comprehensive performance report
- Saves results in JSON format

### 2. **Web Crawling**
- Starts from target URL
- Follows internal links up to specified depth
- Maintains visited URL set to avoid duplicates
- Respects rate limits (0.5s delay between requests)

### 3. **Content Analysis**
For each page, the scanner analyzes:
- HTML content
- Inline JavaScript
- Data attributes
- Meta tags
- HTML comments
- External JavaScript files

### 4. **Pattern Matching**
Uses regex patterns to detect:
- API keys (25+ types)
- Private keys (5+ formats)
- Tokens and credentials
- Connection strings
- Authentication headers

### 5. **Common File Checking**
Attempts to access common sensitive files:
- `.env`, `.env.local`, `.env.production`
- `config.json`, `config.js`
- `secrets.json`, `credentials.json`
- `.git/config`
- `docker-compose.yml`
- Private key files (`id_rsa`, `server.key`, etc.)

### 6. **Report Generation**
- Aggregates all findings
- Categorizes by type
- Generates statistics
- Creates JSON and console reports

## Detection Patterns

### API Keys Detected
- **AWS**: Access keys (AKIA...), Secret keys
- **Google**: API keys (AIza...), OAuth client IDs
- **GitHub**: Personal access tokens (ghp_..., ghs_...)
- **Stripe**: Live keys (sk_live_..., rk_live_...)
- **Slack**: Tokens (xox...), Webhooks
- **Twilio**: API keys (SK...), Account SIDs (AC...)
- **Mailgun**: API keys (key-...)
- **PayPal**: Braintree tokens
- **Square**: OAuth tokens, Access tokens
- **Heroku**: API keys
- **Firebase**: FCM tokens

### Private Keys Detected
- RSA Private Keys
- OpenSSH Private Keys
- DSA Private Keys
- Elliptic Curve (EC) Private Keys
- PGP Private Key Blocks

### Tokens & Credentials
- JWT Tokens (eyJ...)
- Bearer Tokens
- Basic Authentication headers
- Passwords in URLs
- MongoDB connection strings
- MySQL/PostgreSQL connection strings
- JDBC connection strings

## Best Practices

### For Security Auditors
1. **Always get authorization** before scanning a website
2. **Review findings manually** - false positives can occur
3. **Verify credentials** before reporting them
4. **Document your scan** for compliance purposes
5. **Report responsibly** to website owners

### For Website Owners
If sensitive data is found:
1. **Immediately rotate** all exposed API keys
2. **Revoke and regenerate** private keys
3. **Change passwords** and connection strings
4. **Review access logs** for unauthorized access
5. **Implement proper secrets management** (e.g., HashiCorp Vault, AWS Secrets Manager)
6. **Use environment variables** instead of hardcoded credentials
7. **Add `.env` and config files to `.gitignore`**
8. **Enable GitHub secret scanning** for repositories
9. **Implement Content Security Policy** (CSP)
10. **Regular security audits** with tools like this

## Limitations

1. **False Positives**: Pattern matching may detect non-sensitive data that matches patterns
2. **Rate Limiting**: Some websites may block or rate-limit the scanner
3. **JavaScript Execution**: Does not execute JavaScript (use browser DevTools for JS-rendered content)
4. **Authentication**: Cannot scan pages behind authentication
5. **Dynamic Content**: May miss dynamically loaded content
6. **Obfuscation**: Cannot detect obfuscated or encrypted secrets

## Troubleshooting

### Lighthouse Not Found
```bash
# Install Lighthouse globally
npm install -g lighthouse

# Or skip Lighthouse
python lighthouse_auto.py https://example.com --no-lighthouse
```

### SSL Certificate Errors
The scanner disables SSL verification for testing. For production:
```python
# In the code, change:
response = self.session.get(url, timeout=10, verify=False)
# To:
response = self.session.get(url, timeout=10, verify=True)
```

### Rate Limiting Issues
Adjust the delay in the code:
```python
# In scan_page method, change:
time.sleep(0.5)  # 0.5 seconds
# To:
time.sleep(2.0)  # 2 seconds (slower but more respectful)
```

### Memory Issues with Large Sites
Reduce crawl depth:
```bash
python lighthouse_auto.py https://example.com --depth 1
```

## Examples

### Example 1: Quick Scan
```bash
# Fast scan without Lighthouse
python lighthouse_auto.py https://testwebsite.com --no-lighthouse --depth 1
```

### Example 2: Comprehensive Audit
```bash
# Full scan with Lighthouse and deep crawl
python lighthouse_auto.py https://mywebsite.com --depth 3
```

### Example 3: Multiple Targets
```bash
# Scan multiple websites
for url in website1.com website2.com website3.com; do
    python lighthouse_auto.py "https://$url" --output "./reports/$url"
done
```

### Example 4: CI/CD Integration
```bash
# Add to your CI/CD pipeline
python lighthouse_auto.py https://staging.myapp.com --no-lighthouse
if [ $? -ne 0 ]; then
    echo "Security scan failed!"
    exit 1
fi
```

## Legal and Ethical Considerations

### ⚠️ IMPORTANT DISCLAIMER

This tool is provided for **authorized security testing and educational purposes only**.

**Legal Requirements:**
- You MUST have explicit written permission to scan any website
- Unauthorized access to computer systems is illegal under laws such as:
  - Computer Fraud and Abuse Act (CFAA) in the US
  - Computer Misuse Act in the UK
  - Similar laws in other jurisdictions

**Ethical Usage:**
- Only scan your own websites or those you have permission to test
- Respect robots.txt and website terms of service
- Do not use findings for malicious purposes
- Report vulnerabilities responsibly
- Do not share or exploit discovered credentials

**Disclaimer:**
The authors and contributors of this tool are not responsible for any misuse or damage caused by this program. By using this tool, you agree to use it responsibly and legally.

## Contributing

Contributions are welcome! To add new detection patterns:

1. Add regex pattern to the `PATTERNS` dictionary in `LighthouseAutoScanner` class
2. Test pattern thoroughly to minimize false positives
3. Document the pattern and what it detects
4. Submit a pull request

Example:
```python
PATTERNS = {
    # ... existing patterns ...
    'new_api_service': r'new_service_[0-9a-zA-Z]{32}',
}
```

## Integration with Mr. Matrix Project

This tool integrates with the Mr. Matrix WORMGPT-V2V.X project as an automated security auditing component. It can be used alongside:

- `matrixs1.0.py` - Packet analysis tool
- `TESTNMAP.py` - Nmap GUI scanner
- `stakeus_gld_converter.py` - Financial calculations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Developed for the Mr. Matrix WORMGPT-V2V.X project
- Created by Catdevzsh and contributors
- Built with Python, BeautifulSoup, and Google Lighthouse

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X/issues
- Documentation: This file
- Examples: See usage section above

---

**Remember: With great power comes great responsibility. Use this tool wisely and ethically.**
