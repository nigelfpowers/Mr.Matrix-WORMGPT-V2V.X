# Ethereum Address Checker

This directory contains utilities to interact with and check the value of Ethereum addresses, specifically designed to work with the address: `0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50`

## Overview

The utilities provide three different ways to check Ethereum address information:

1. **Solidity Smart Contract** - A deployable smart contract for on-chain address checking
2. **JavaScript/Node.js Utility** - Using ethers.js for programmatic access
3. **Python Utility** - Using web3.py for Python-based checking

## Files

- `EthereumAddressChecker.sol` - Solidity smart contract
- `ethereumAddressChecker.js` - JavaScript/Node.js utility
- `ethereumAddressChecker.py` - Python utility

## Features

All utilities can:
- ✅ Check the balance of an Ethereum address (in ETH and Wei)
- ✅ Determine if an address is a contract or EOA (Externally Owned Account)
- ✅ Get transaction count for an address
- ✅ Validate Ethereum addresses
- ✅ Get comprehensive "true value" information

## Installation & Usage

### 1. Solidity Smart Contract

The smart contract `EthereumAddressChecker.sol` can be deployed to any EVM-compatible blockchain.

**Key Functions:**
```solidity
// Get the balance of the target address
function getTargetBalance() public view returns (uint256)

// Check if the target address is a contract
function isTargetContract() public view returns (bool)

// Get comprehensive info about the target address
function getTrueValue() public view returns (uint256 balance, bool isContractAddress)

// Check any address
function getAddressInfo(address _address) public view returns (uint256 balance, bool isContractAddress)
```

**Deployment:**
1. Use Remix IDE (https://remix.ethereum.org/)
2. Copy the contract code from `EthereumAddressChecker.sol`
3. Compile with Solidity 0.8.0 or higher
4. Deploy to your preferred network (Ethereum mainnet, testnet, or other EVM chains)

**Interacting with the Contract:**
- Call `getTrueValue()` to get information about the target address
- Call `getTargetBalance()` to get just the balance
- Call `isTargetContract()` to check if it's a smart contract

### 2. JavaScript/Node.js Utility

**Installation:**
```bash
# Install dependencies
npm install ethers
```

**Usage:**
```bash
# Run directly
node ethereumAddressChecker.js
```

**Programmatic Usage:**
```javascript
const checker = require('./ethereumAddressChecker');

// Get true value of the target address
const info = await checker.getTrueValue();

// Check any address
const balance = await checker.getAddressBalance('0xYourAddressHere');

// Check if address is a contract
const contractCheck = await checker.isContract('0xYourAddressHere');

// Validate address format
const isValid = checker.isValidAddress('0xYourAddressHere');
```

**With Custom RPC:**
```javascript
const info = await checker.getTrueValue('https://your-rpc-url.com');
```

### 3. Python Utility

**Installation:**
```bash
# Install dependencies
pip install web3
```

**Usage:**
```bash
# Run directly
python ethereumAddressChecker.py
```

**Programmatic Usage:**
```python
from ethereumAddressChecker import EthereumAddressChecker

# Initialize checker
checker = EthereumAddressChecker()

# Or with custom RPC
checker = EthereumAddressChecker(rpc_url='https://your-rpc-url.com')

# Get true value of target address
info = checker.get_true_value()

# Check any address
balance = checker.get_balance('0xYourAddressHere')

# Check if it's a contract
contract_info = checker.is_contract('0xYourAddressHere')

# Get comprehensive info
full_info = checker.get_address_info('0xYourAddressHere')
```

## Target Address Information

**Address:** `0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50`

This address can be:
- An Externally Owned Account (EOA) - a regular wallet
- A Smart Contract - a deployed contract on the Ethereum blockchain

The utilities will determine which type it is and provide relevant information including:
- Balance (in both ETH and Wei)
- Whether it's a contract or EOA
- Transaction count
- Contract code (if applicable)

## RPC Endpoints

For production use, you should use your own RPC endpoint from providers like:
- **Infura** (https://infura.io/)
- **Alchemy** (https://www.alchemy.com/)
- **QuickNode** (https://www.quicknode.com/)
- **Ankr** (https://www.ankr.com/)

The utilities use public endpoints by default, which may have rate limits.

## Example Output

```
Ethereum Address Checker Utility

Checking target address...

✓ Address 0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50 is valid

Checking true value of address: 0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50

=== Address Information ===
Address: 0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50
Type: EOA (Externally Owned Account)
Balance: 0.123456789 ETH (123456789000000000 Wei)
Transaction Count: 42
Is Contract: False
===========================
```

## Understanding the "True Value"

The "true value" of an Ethereum address refers to:
1. **Balance** - The amount of ETH held by the address
2. **Type** - Whether it's a contract or regular account
3. **Activity** - Number of transactions sent from this address
4. **Code** - If it's a contract, the bytecode deployed at this address

## Security Notes

- Never send ETH to addresses you don't trust
- Always verify addresses are correct (case-sensitive checksums)
- Be cautious when interacting with smart contracts
- Use test networks (testnets) for testing before mainnet

## Troubleshooting

**"Not connected to Ethereum network"**
- Check your internet connection
- Verify the RPC endpoint is accessible
- Try a different RPC provider

**"Invalid address format"**
- Ensure the address starts with "0x"
- Verify the address is 42 characters long (0x + 40 hex characters)
- Check for typos in the address

**Rate limiting errors**
- Use your own RPC endpoint instead of public ones
- Add delays between requests
- Consider using a paid RPC service for higher limits

## Contributing

Feel free to submit pull requests or open issues to improve these utilities!

## License

MIT License - See LICENSE file for details
