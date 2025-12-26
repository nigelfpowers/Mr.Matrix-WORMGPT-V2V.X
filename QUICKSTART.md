# Ethereum Address Checker - Quick Start Guide

## Overview

This repository now includes comprehensive tools to check and interact with Ethereum addresses, specifically addressing the need to retrieve the "true value" of address `0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50`.

## What's the "True Value" of an Ethereum Address?

The "true value" of an Ethereum address includes:
1. **Balance** - How much ETH the address holds (in both ETH and Wei)
2. **Type** - Whether it's a Contract or EOA (Externally Owned Account)
3. **Activity** - Number of transactions sent from this address
4. **Status** - Whether it contains any contract code

## Quick Start

### Option 1: JavaScript/Node.js (Recommended for most users)

```bash
# Install dependencies
npm install

# Check the target address
npm run check-eth-address

# Or run examples
node examples.js
```

### Option 2: Python

```bash
# Install dependencies
pip install -r requirements.txt

# Check the target address
python ethereumAddressChecker.py
```

### Option 3: Deploy Smart Contract

Deploy `EthereumAddressChecker.sol` to any EVM-compatible blockchain using:
- [Remix IDE](https://remix.ethereum.org/)
- Hardhat
- Truffle
- Foundry

## Files Included

| File | Description |
|------|-------------|
| `EthereumAddressChecker.sol` | Solidity smart contract for on-chain checking |
| `ethereumAddressChecker.js` | JavaScript utility using ethers.js |
| `ethereumAddressChecker.py` | Python utility using web3.py |
| `examples.js` | Working code examples |
| `ETHEREUM_CHECKER_README.md` | Complete documentation |
| `package.json` | Node.js configuration with ethers.js |
| `requirements.txt` | Python dependencies |

## Key Features

✅ Check balance of any Ethereum address  
✅ Determine if address is a smart contract  
✅ Get transaction count for addresses  
✅ Validate Ethereum address format  
✅ Support for custom RPC endpoints  
✅ Comprehensive error handling  

## Important Notes

⚠️ **RPC Endpoint Required**: For actual network queries, you need an Ethereum RPC endpoint from:
- Infura (https://infura.io/)
- Alchemy (https://www.alchemy.com/)
- QuickNode (https://www.quicknode.com/)
- Ankr (https://www.ankr.com/)

⚠️ **Security**: The smart contract's send functions don't have access controls. They are for demonstration purposes. Add proper authorization (like OpenZeppelin's Ownable) for production use.

## Example Usage

### JavaScript
```javascript
const checker = require('./ethereumAddressChecker');

// Check the target address
const info = await checker.getTrueValue();

// Check any address
const balance = await checker.getAddressBalance('0xYourAddress');

// With custom RPC
const info = await checker.getTrueValue('https://your-rpc-url.com');
```

### Python
```python
from ethereumAddressChecker import EthereumAddressChecker

checker = EthereumAddressChecker(rpc_url='https://your-rpc-url.com')
info = checker.get_true_value()
print(info)
```

### Solidity
```solidity
// Deploy the contract, then call:
EthereumAddressChecker checker = EthereumAddressChecker(contractAddress);
(uint256 balance, bool isContract) = checker.getTrueValue();
```

## Target Address Information

**Address**: `0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50`

Use any of the utilities above to:
- Check its current balance
- See if it's a contract or regular wallet
- View its transaction history count
- Monitor its activity

## Need Help?

See [ETHEREUM_CHECKER_README.md](ETHEREUM_CHECKER_README.md) for:
- Detailed installation instructions
- Complete API documentation
- Troubleshooting guide
- Security best practices
- More code examples

## License

MIT License - See [LICENSE](LICENSE) file for details.
