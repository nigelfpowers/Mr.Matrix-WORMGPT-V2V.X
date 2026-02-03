# Rainbow Wallet Balance Checker - iPhone Shortcut

An iPhone Shortcut designed to help you view all real balances and coins in your Rainbow wallet by automating navigation and providing helpful guidance.

## 🌈 Overview

This iOS Shortcut automates the process of opening Rainbow wallet and guiding you to view all your real balances and coins. It helps ensure that no tokens are hidden and all balances are properly displayed.

## ✨ Features

- **Automatic App Launch**: Opens Rainbow wallet automatically
- **Smart Navigation**: Uses URL schemes to navigate directly to wallet view
- **Balance Refresh Reminders**: Prompts you to refresh balances
- **Hidden Token Detection**: Guides you to settings to unhide any hidden tokens
- **Interactive Menu**: Provides options to switch accounts, access settings, or run diagnostics
- **Debug Mode Integration**: Links to the full Rainbow Wallet Debugger for advanced troubleshooting

## 📲 Installation

### Method 1: Direct Import (Recommended)

1. **Download the Shortcut File**
   - Download `RainbowWalletBalanceChecker.shortcut` from this repository
   - You can download it directly to your iPhone using Safari or transfer it via AirDrop/iCloud

2. **Import to Shortcuts App**
   - Open the downloaded `.shortcut` file on your iPhone
   - Tap "Add Shortcut" when prompted
   - The shortcut will appear in your Shortcuts library

### Method 2: Manual Creation

If you prefer to create the shortcut manually:

1. Open the **Shortcuts** app on your iPhone
2. Tap the **+** button to create a new shortcut
3. Add the following actions in order:
   - **Comment**: Add description
   - **Show Notification**: "Opening Rainbow wallet..."
   - **Open App**: Select "Rainbow"
   - **Wait**: 2 seconds
   - **Open URL**: `rainbow://wallet`
   - **Wait**: 1 second
   - **Show Notification**: Instructions to pull down to refresh
   - **Ask for Input**: Prompt for next action (settings/switch/debug/done)
   - **If** statements to handle different user choices

### Method 3: iCloud Link (if available)

If an iCloud link is provided, simply:
1. Open the link on your iPhone
2. Tap "Get Shortcut"
3. Review permissions and tap "Add Shortcut"

## 🎯 How to Use

### Basic Usage

1. **Run the Shortcut**
   - Open the Shortcuts app
   - Tap "Rainbow Wallet Balance Checker"
   - Or add it to your Home Screen for quick access

2. **Follow the Prompts**
   - The shortcut will automatically open Rainbow wallet
   - Wait for the app to load completely
   - Pull down on the wallet screen to refresh all balances

3. **Check Hidden Tokens**
   - If prompted, type "settings" to open wallet settings
   - Navigate to: Wallets > [Your Wallet Name] > Hidden Tokens
   - Unhide any tokens you want to see

### Adding to Home Screen

For even faster access:

1. Open the Shortcuts app
2. Find "Rainbow Wallet Balance Checker"
3. Tap the ••• menu (three dots)
4. Tap "Add to Home Screen"
5. Customize the name and icon if desired
6. Tap "Add"

Now you can launch the shortcut directly from your home screen!

### Adding to Widgets

1. Long-press on your home screen
2. Tap the **+** button in the top corner
3. Search for "Shortcuts"
4. Select the widget size you prefer
5. Add the widget to your home screen
6. Tap the widget to configure it
7. Select "Rainbow Wallet Balance Checker"

## 🔧 What the Shortcut Does

### Step-by-Step Process

1. **Initial Notification**
   - Displays a notification that the shortcut is starting

2. **Opens Rainbow Wallet**
   - Launches the Rainbow app using iOS's app launching capability
   - Waits 2 seconds for the app to load

3. **Navigate to Wallet View**
   - Uses the `rainbow://wallet` URL scheme to navigate directly to the wallet balance view
   - This ensures you're on the right screen to see all balances

4. **Provides Instructions**
   - Shows a notification reminding you to:
     - Pull down to refresh balances
     - Check for hidden tokens in settings
     - Ensure internet connectivity

5. **Interactive Options**
   - Asks what you'd like to do next:
     - **switch**: Switch to another wallet account
     - **settings**: Open wallet settings to manage hidden tokens
     - **debug**: Access the full debugger documentation
     - **done**: Complete the balance check

6. **Settings Navigation** (if selected)
   - Opens Rainbow settings using `rainbow://settings` URL scheme
   - Provides guidance to navigate to hidden tokens section

7. **Debug Mode** (if selected)
   - Opens the GitHub repository with the full Rainbow Wallet Debugger
   - For users who need comprehensive diagnostics

## 💡 Tips for Viewing All Balances

### Enable All Token Display

1. Open Rainbow wallet
2. Go to **Settings** ⚙️
3. Navigate to **Wallets**
4. Select your wallet
5. Tap **Hidden Tokens**
6. Review and unhide any tokens you want to see

### Check Small Balances

1. In Rainbow settings
2. Look for **"Show small balances"** option
3. Enable it to see tokens with very small values

### Ensure Network Connection

1. Make sure you're connected to the internet
2. Check if Wi-Fi or cellular data is working
3. Try switching between Wi-Fi and cellular if one isn't working

### Refresh Balances

1. In the wallet view, pull down from the top
2. This forces a refresh of all token balances
3. Wait for the refresh to complete

### Check All Accounts

If you have multiple wallets/accounts in Rainbow:
1. Tap the wallet selector at the top
2. Switch between different wallets
3. Each wallet may have different tokens and balances

## 🔐 Privacy & Security

- ✅ **No Data Collection**: This shortcut doesn't collect or transmit any data
- ✅ **Local Execution**: Everything runs locally on your iPhone
- ✅ **No Private Key Access**: The shortcut never accesses your private keys or seed phrases
- ✅ **Open Source**: The shortcut actions are fully transparent
- ✅ **No External Servers**: Doesn't connect to any third-party servers

## ⚠️ Troubleshooting

### Shortcut Doesn't Open Rainbow

**Solution**:
- Make sure Rainbow wallet is installed on your iPhone
- Check that the app bundle identifier is correct (`me.rainbow`)
- Try updating to the latest version of Rainbow wallet

### URL Schemes Don't Work

**Solution**:
- Some versions of Rainbow may not support all URL schemes
- Try manually navigating instead
- Update Rainbow wallet to the latest version

### Balances Still Not Showing

**Solution**:
1. Run the full diagnostic tool:
   ```bash
   python3 rainbow_wallet_debugger.py
   ```
2. Check network connectivity
3. Verify Ethereum RPC endpoints are reachable
4. Clear app cache and restart Rainbow wallet

### Shortcut Asks for Permissions

**Solution**:
- Grant the requested permissions (app launching, notifications)
- These are safe and necessary for the shortcut to function
- Review the permissions in Settings > Shortcuts

## 🔗 Related Tools

### Rainbow Wallet Debugger (Full Version)

For comprehensive diagnostics, use the Python-based debugger:

```bash
# On iPhone with Termux
cd ~/Mr.Matrix-WORMGPT-V2V.X
python rainbow_wallet_debugger.py

# On Desktop
python3 rainbow_wallet_debugger.py
```

See [RAINBOW_WALLET_DEBUGGER_README.md](RAINBOW_WALLET_DEBUGGER_README.md) for complete documentation.

## 📱 Compatibility

- **iOS**: 14.0 or later (iOS 15+ recommended)
- **watchOS**: Compatible with Apple Watch
- **Rainbow Wallet**: All recent versions
- **Shortcuts App**: Pre-installed on iOS 14+

## 🆘 Support

### Getting Help

If you encounter issues:

1. **Check the Troubleshooting section** above
2. **Run the full debugger** for detailed diagnostics
3. **Visit the GitHub repository**: [Mr.Matrix-WORMGPT-V2V.X](https://github.com/nigelfpowers/Mr.Matrix-WORMGPT-V2V.X)
4. **Open an issue** on GitHub with:
   - Your iOS version
   - Rainbow wallet version
   - Description of the problem
   - Screenshots if applicable

### Common Questions

**Q: Will this work with other wallets?**
A: This shortcut is specifically designed for Rainbow wallet. The URL schemes and navigation are Rainbow-specific.

**Q: Can I customize the shortcut?**
A: Yes! Open it in the Shortcuts app and modify any actions to suit your needs.

**Q: Is this safe to use?**
A: Yes. The shortcut only launches the app and provides navigation. It doesn't access any sensitive data.

**Q: Can I share this with friends?**
A: Absolutely! You can share the `.shortcut` file or the iCloud link.

## 🔄 Updates

To update the shortcut:
1. Download the latest version from the repository
2. Import it again (it will replace the old version)
3. Or manually edit your existing shortcut with new actions

## 📝 Version History

### v1.0.0 (Initial Release)
- Basic wallet opening and navigation
- Interactive menu system
- Settings and debug mode access
- Guided instructions for viewing all balances

## 🤝 Contributing

Improvements and suggestions are welcome! 

To contribute:
1. Fork the repository
2. Make your changes
3. Test the shortcut thoroughly
4. Submit a pull request

## 📄 License

This shortcut is part of the Mr.Matrix-WORMGPT-V2V.X project and is licensed under the MIT License.

## ⚡ Quick Reference Card

```
┌─────────────────────────────────────────────┐
│  RAINBOW WALLET BALANCE CHECKER SHORTCUTS   │
├─────────────────────────────────────────────┤
│  Run Shortcut → Opens Rainbow automatically │
│  Pull Down    → Refresh all balances       │
│  Type 'settings' → Manage hidden tokens    │
│  Type 'debug'    → Full diagnostics        │
│  Type 'done'     → Complete check          │
└─────────────────────────────────────────────┘
```

---

**Mr. Matrix - Your Unhinged Source of Knowledge in Dot Matrix Style 💀😈**

*Powered by Mr.Matrix-WORMGPT-V2V.X*
