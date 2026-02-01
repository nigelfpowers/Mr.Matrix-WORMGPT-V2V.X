# Rainbow Wallet Debugger Script

A comprehensive mobile-friendly debugging tool for Rainbow wallet that can run locally on your phone using Termux or any Python environment.

## Features

🔍 **Comprehensive Diagnostics**
- Network connectivity checks
- Ethereum RPC endpoint testing
- DNS resolution verification
- Local storage inspection
- System resource analysis

🎨 **Mobile-Friendly Interface**
- Color-coded output for easy reading
- Clear status indicators (✓/✗)
- Detailed logging
- Exportable debug reports

🔧 **Debug Capabilities**
- Identifies common wallet issues
- Provides actionable solutions
- Tests multiple RPC providers
- Checks wallet storage permissions
- Monitors network quality

## Installation on Mobile (Termux)

### Step 1: Install Termux
Download Termux from:
- F-Droid (recommended): https://f-droid.org/en/packages/com.termux/
- Google Play Store

### Step 2: Set Up Python in Termux
```bash
# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python

# Install git
pkg install git
```

### Step 3: Clone the Repository
```bash
# Navigate to a convenient directory
cd ~/

# Clone the repository
git clone https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X.git

# Navigate to the directory
cd Mr.Matrix-WORMGPT-V2V.X
```

### Step 4: Run the Debugger
```bash
# Make the script executable (if not already)
chmod +x rainbow_wallet_debugger.py

# Run the debugger
python rainbow_wallet_debugger.py
```

## Installation on Desktop/Laptop

### Requirements
- Python 3.7 or higher
- Internet connection (for network tests)

### Running the Script
```bash
# Clone the repository
git clone https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X.git
cd Mr.Matrix-WORMGPT-V2V.X

# Run the debugger
python3 rainbow_wallet_debugger.py
```

## What the Script Checks

### 1. Network Connectivity
Tests connections to:
- ethereum.org
- infura.io
- cloudflare.com
- google.com

Provides a connectivity success rate and identifies network issues.

### 2. Ethereum RPC Endpoints
Checks reachability of major Ethereum node providers:
- Infura
- Alchemy
- Cloudflare Ethereum Gateway
- Ankr

### 3. DNS Resolution
Verifies DNS is working correctly for:
- rainbow.me (Rainbow wallet domain)
- ethereum.org
- infura.io
- alchemy.com

### 4. Local Storage
Scans for Rainbow wallet storage in common locations:
- `~/.rainbow`
- `~/Library/Application Support/Rainbow` (macOS)
- `~/.config/rainbow` (Linux)
- `/data/data/me.rainbow/files` (Android)

Checks read/write permissions to identify permission issues.

### 5. System Resources
- Python version compatibility check
- Required module availability
- Optional module detection (web3, requests, eth_account)

### 6. Common Issues Diagnosis
Automatically identifies and provides solutions for:
- Poor network connectivity
- DNS resolution problems
- RPC endpoint failures
- Storage permission issues

## Output Example

```
╔═══════════════════════════════════════════════════════════╗
║       Rainbow Wallet Debugger - Mr. Matrix Edition       ║
║                   Mobile-Friendly Version                 ║
╚═══════════════════════════════════════════════════════════╝
Started: 2026-02-01 19:51:00
Platform: Linux 5.15.0

Starting comprehensive diagnostics...

[19:51:00] [INFO] Checking system resources...
[19:51:00] [INFO] Python version: 3.11.0
[19:51:00] [SUCCESS] ✓ Python version is compatible

[19:51:00] [INFO] Checking network connectivity...
[19:51:01] [SUCCESS] ✓ Connection to ethereum.org:443 successful
[19:51:01] [SUCCESS] ✓ Connection to infura.io:443 successful
...
```

## Saving Debug Reports

The script can save a comprehensive debug report to a file. When prompted:
- Type `y` to save the report
- The report will be saved as `rainbow_debug_YYYYMMDD_HHMMSS.txt`

The report includes:
- Full test results
- Complete debug log
- System information
- Timestamp of diagnostics

## Troubleshooting

### "Permission denied" error
```bash
chmod +x rainbow_wallet_debugger.py
```

### "Module not found" error
The script uses only Python standard library modules for core functionality. Optional modules (web3, requests, eth_account) are not required but will enable additional features if installed.

To install optional modules:
```bash
# In Termux
pkg install python-pip
pip install web3 requests eth-account

# On Desktop
pip3 install web3 requests eth-account
```

### Script won't run on Android
Make sure you're using Termux from F-Droid, not the outdated Play Store version.

### No internet connection detected
- Check your WiFi/mobile data connection
- Try switching between WiFi and mobile data
- Check if a VPN is interfering

## Use Cases

### 1. Wallet Not Connecting
Run the debugger to identify network or RPC issues:
```bash
python rainbow_wallet_debugger.py
```
Look for RPC endpoint failures or network connectivity problems.

### 2. Transaction Failures
Check if Ethereum nodes are reachable and DNS is working properly.

### 3. Slow Wallet Performance
The network connectivity test will show which endpoints are responsive.

### 4. Storage/Permission Issues
The local storage check will identify permission problems that may prevent wallet data access.

## Privacy & Security

- **No data is transmitted**: All diagnostics run locally on your device
- **No wallet keys accessed**: The script only checks network and storage paths
- **No personal data collected**: Results are only saved locally if you choose to save them
- **Open source**: Full source code available for review

## Support

For issues or feature requests:
- GitHub: https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X/issues
- Review the saved debug report for detailed diagnostic information

## License

This tool is part of the Mr.Matrix-WORMGPT-V2V.X project and is licensed under the MIT License.

## Disclaimer

This debugging tool is for diagnostic purposes only. It does not access, modify, or transmit any wallet data, private keys, or sensitive information. Always exercise caution when debugging wallet applications and never share your private keys or seed phrases with anyone.

---

*Mr. Matrix - Your Unhinged Source of Knowledge in Dot Matrix Style 💀😈*
