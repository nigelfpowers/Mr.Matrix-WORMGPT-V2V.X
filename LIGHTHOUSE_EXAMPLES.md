# Lighthouse Auto Scanner - Configuration Examples

This file provides example configurations and use cases for the Lighthouse Auto Scanner.

## Basic Configuration

### Minimal Scan (Quick Test)
```bash
python3 lighthouse_auto.py https://example.com --no-lighthouse --depth 1
```
- Skips Lighthouse for speed
- Only scans the main page and immediate links
- Best for: Quick security checks

### Standard Scan (Recommended)
```bash
python3 lighthouse_auto.py https://example.com --depth 2
```
- Includes Lighthouse performance audit
- Crawls 2 levels deep
- Best for: Regular security audits

### Deep Scan (Comprehensive)
```bash
python3 lighthouse_auto.py https://example.com --depth 3 --output ./security_audit_$(date +%Y%m%d)
```
- Full Lighthouse audit
- Crawls 3 levels deep
- Timestamped output directory
- Best for: Thorough security assessments

## Use Cases

### 1. Pre-Deployment Security Check
```bash
#!/bin/bash
# Run before deploying to production

echo "Running pre-deployment security scan..."
python3 lighthouse_auto.py https://staging.myapp.com \
  --no-lighthouse \
  --depth 2 \
  --output ./pre_deploy_scan

# Check if sensitive data was found
if grep -q '"total_api_keys": 0' ./pre_deploy_scan/security_report_*.json; then
    echo "✓ No API keys detected. Safe to deploy."
    exit 0
else
    echo "✗ WARNING: Sensitive data detected! Review before deployment."
    exit 1
fi
```

### 2. Multiple Website Monitoring
```bash
#!/bin/bash
# Monitor multiple websites

WEBSITES=(
    "https://website1.com"
    "https://website2.com"
    "https://website3.com"
)

for site in "${WEBSITES[@]}"; do
    echo "Scanning $site..."
    python3 lighthouse_auto.py "$site" \
        --no-lighthouse \
        --depth 1 \
        --output "./scans/$(echo $site | sed 's/https:\/\///')"
done

echo "All scans complete!"
```

### 3. CI/CD Pipeline Integration
```yaml
# GitHub Actions example
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        pip install requests beautifulsoup4
    
    - name: Run security scan
      run: |
        python3 lighthouse_auto.py https://staging.myapp.com \
          --no-lighthouse \
          --output ./scan_results
    
    - name: Upload results
      uses: actions/upload-artifact@v2
      with:
        name: security-scan-results
        path: ./scan_results/
```

### 4. Scheduled Monitoring (Cron)
```bash
# Add to crontab: crontab -e
# Run daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/lighthouse_auto.py https://mywebsite.com --no-lighthouse --output /var/log/security_scans/$(date +\%Y\%m\%d) 2>&1 | logger -t lighthouse_scan
```

### 5. Development Server Testing
```bash
# Test local development server
python3 lighthouse_auto.py http://localhost:3000 \
  --no-lighthouse \
  --depth 1 \
  --output ./dev_scan

# Test with authentication (if needed, modify script to include auth headers)
```

## Advanced Patterns

### Custom Rate Limiting
Modify the script to adjust crawl speed:
```python
# In lighthouse_auto.py, line ~230
time.sleep(2.0)  # Increase from 0.5 to 2.0 seconds
```

### Filtering Results
Extract only specific types of findings:
```bash
# After scanning, filter results
python3 lighthouse_auto.py https://example.com --no-lighthouse

# Extract only API keys
cat ./lighthouse_results/security_report_*.json | jq '.findings.api_keys'

# Count findings by type
cat ./lighthouse_results/security_report_*.json | jq '.statistics'
```

### Bulk Analysis
```bash
#!/bin/bash
# Analyze multiple pages from a list

while IFS= read -r url; do
    echo "Scanning: $url"
    python3 lighthouse_auto.py "$url" \
        --no-lighthouse \
        --depth 1 \
        --output "./bulk_scan/$(echo $url | md5sum | cut -d' ' -f1)"
    sleep 5  # Pause between scans
done < urls.txt

# Generate summary
echo "Summary of findings:"
find ./bulk_scan -name "security_report_*.json" -exec jq '.statistics' {} \;
```

## Environment Variables

You can set these before running the script:

```bash
# Set default output directory
export LIGHTHOUSE_OUTPUT_DIR="./my_scans"

# Set crawl depth
export LIGHTHOUSE_DEPTH=2

# Example with environment variables
python3 lighthouse_auto.py https://example.com \
  --output "${LIGHTHOUSE_OUTPUT_DIR}" \
  --depth "${LIGHTHOUSE_DEPTH}"
```

## Reporting

### Generate HTML Summary
```bash
#!/bin/bash
# Convert JSON report to readable HTML

REPORT_FILE=$(ls -t ./lighthouse_results/security_report_*.json | head -1)

echo "<html><head><title>Security Report</title></head><body>" > report.html
echo "<h1>Security Scan Results</h1>" >> report.html
echo "<pre>" >> report.html
jq '.' "$REPORT_FILE" >> report.html
echo "</pre></body></html>" >> report.html

echo "HTML report generated: report.html"
```

### Email Alerts
```bash
#!/bin/bash
# Send email if sensitive data is found

python3 lighthouse_auto.py https://example.com --no-lighthouse

REPORT=$(ls -t ./lighthouse_results/security_report_*.json | head -1)
TOTAL_FINDINGS=$(jq '[.statistics | to_entries[] | .value] | add' "$REPORT")

if [ "$TOTAL_FINDINGS" -gt 0 ]; then
    echo "Security scan found $TOTAL_FINDINGS sensitive items" | \
        mail -s "⚠️ Security Alert: Sensitive Data Detected" admin@example.com
fi
```

## Best Practices

1. **Always get authorization** before scanning any website
2. **Run scans regularly** (weekly or after each deployment)
3. **Keep results secure** - they contain sensitive information
4. **Rotate detected credentials** immediately
5. **Use version control** for scan configurations
6. **Document findings** and remediation steps
7. **Integrate with CI/CD** for automated security checks
8. **Monitor trends** over time

## Performance Tips

- Use `--no-lighthouse` for faster scans when performance audit is not needed
- Reduce `--depth` for large websites to avoid long scan times
- Run scans during off-peak hours to minimize impact
- Use parallel scanning for multiple domains (but respect rate limits)

## Troubleshooting

### Scan Taking Too Long
```bash
# Reduce depth
python3 lighthouse_auto.py https://example.com --depth 1

# Skip Lighthouse
python3 lighthouse_auto.py https://example.com --no-lighthouse
```

### Memory Issues
```bash
# Process results in smaller batches
# Scan specific pages instead of full site crawl
python3 lighthouse_auto.py https://example.com/specific-page --depth 0
```

### False Positives
Review and filter results:
```bash
# Extract and review manually
cat ./lighthouse_results/security_report_*.json | jq '.findings.api_keys' | less
```

## Support

For issues or questions:
- See LIGHTHOUSE_README.md for detailed documentation
- Check GitHub issues: https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X/issues
- Review example scripts in this file

---

Remember: Use responsibly and ethically. Only scan websites you own or have explicit permission to test.
