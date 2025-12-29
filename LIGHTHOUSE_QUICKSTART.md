# Lighthouse Auto Scanner - Quick Reference

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Option A: Use setup script (recommended)
bash lighthouse_setup.sh

# Option B: Manual installation
pip install -r requirements.txt
npm install -g lighthouse  # Optional, for Lighthouse features
```

### 2. Basic Usage
```bash
# Scan a website
python3 lighthouse_auto.py https://example.com

# Fast scan without Lighthouse
python3 lighthouse_auto.py https://example.com --no-lighthouse
```

### 3. View Results
```bash
# Results are saved in ./lighthouse_results/
ls -l lighthouse_results/

# View security report
cat lighthouse_results/security_report_*.json | jq '.'
```

## 📋 Command Reference

| Command | Description |
|---------|-------------|
| `python3 lighthouse_auto.py URL` | Basic scan with all features |
| `--depth N` | Set crawl depth (0-5) |
| `--output DIR` | Custom output directory |
| `--no-lighthouse` | Skip Lighthouse audit |
| `--help` | Show help message |

## 🔍 What It Detects

### API Keys (25+ types)
- AWS, Google Cloud, GitHub, Stripe
- Slack, Twilio, Mailgun, PayPal
- Square, Heroku, Firebase

### Private Keys
- RSA, SSH, DSA, EC, PGP

### Credentials
- JWT tokens, Bearer tokens
- Basic auth, Passwords in URLs
- Database connection strings

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `lighthouse_auto.py` | Main scanner script |
| `lighthouse_test_demo.py` | Test/demo without scanning real sites |
| `lighthouse_setup.sh` | Automated setup script |
| `LIGHTHOUSE_README.md` | Full documentation |
| `LIGHTHOUSE_EXAMPLES.md` | Configuration examples |
| `requirements.txt` | Python dependencies |

## ⚠️ Important Notes

1. **Authorization Required**: Only scan websites you own or have permission to test
2. **Ethical Use**: Unauthorized access to systems is illegal
3. **Secure Results**: Reports contain sensitive data - keep them secure
4. **Immediate Action**: Rotate any exposed credentials immediately

## 🔗 Links

- Full Documentation: [LIGHTHOUSE_README.md](LIGHTHOUSE_README.md)
- Examples & Use Cases: [LIGHTHOUSE_EXAMPLES.md](LIGHTHOUSE_EXAMPLES.md)
- Test/Demo: Run `python3 lighthouse_test_demo.py`

## 🐛 Troubleshooting

**Lighthouse not found?**
```bash
npm install -g lighthouse
# Or use --no-lighthouse flag
```

**SSL errors?**
```bash
# The script disables SSL verification for testing
# For production, modify line ~182 in lighthouse_auto.py
```

**Scan too slow?**
```bash
# Reduce depth
python3 lighthouse_auto.py URL --depth 1

# Skip Lighthouse
python3 lighthouse_auto.py URL --no-lighthouse
```

## 📞 Support

- GitHub Issues: https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X/issues
- Documentation: See LIGHTHOUSE_README.md
- Demo: `python3 lighthouse_test_demo.py`

---

**Mr. Matrix - WORMGPT-V2V.X**  
*The Cat that hacks for you* 💀😈
