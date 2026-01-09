# Avalanche C-Chain Transaction Sender

A Python tool for parsing, validating, and preparing Ethereum transactions for the Avalanche C-Chain network.

## Overview

This tool helps you work with Ethereum transactions on the Avalanche C-Chain (chainId: 43114). It can:

- Parse and validate transaction data
- Decode ERC-20 token transfer data
- Display human-readable transaction summaries
- Provide implementation guidance for sending transactions

## Features

- ✅ **Transaction Validation**: Validates all required fields and addresses
- ✅ **ERC-20 Decoding**: Automatically decodes ERC-20 transfer function calls
- ✅ **Amount Calculation**: Shows token amounts for different decimal configurations
- ✅ **Safe by Design**: Does not send transactions without explicit implementation
- ✅ **Educational**: Provides example code for actual transaction sending

## Usage

### Basic Usage

Run the script with the built-in example transaction:

```bash
python3 avalanche_transaction_sender.py
```

### Example Transaction

The script includes an example transaction from the Avalanche C-Chain:

```python
transaction_data = {
    "chainId": 43114,
    "data": "0xa9059cbb000000000000000000000000eb98b3a7bf0e139b08164f01824c6aae93b11c6a000000000000000000000000000000000000000000000000000000000bebc200",
    "from": "0x3e172fde66cefa9f4a4c373fe0932311fda11a76",
    "gas": "0x19073",
    "gasPrice": "0x1ee62800",
    "nonce": "0x2a",
    "to": "0x152b9d0fdc40c096757f570a51e494bd4b943e50",
    "value": "0x0"
}
```

### Custom Usage

You can modify the script to use your own transaction data:

```python
from avalanche_transaction_sender import AvalancheTransactionSender

# Your transaction data
your_transaction = {
    "chainId": 43114,
    "from": "0xYourAddress",
    "to": "0xRecipientAddress",
    "data": "0xYourData",
    "gas": "0xGasLimit",
    "gasPrice": "0xGasPrice",
    "nonce": "0xNonce",
    "value": "0x0"
}

# Create sender and prepare transaction
sender = AvalancheTransactionSender()
prepared_tx = sender.prepare_transaction(your_transaction)
```

## Output Example

```
======================================================================
                AVALANCHE C-CHAIN TRANSACTION DETAILS                 
======================================================================

Chain ID:        43114
From:            0x3e172fde66cefa9f4a4c373fe0932311fda11a76
To:              0x152b9d0fdc40c096757f570a51e494bd4b943e50
Value:           0x0
Gas:             0x19073
Gas Price:       0x1ee62800
Nonce:           0x2a

----------------------------------------------------------------------
                       DECODED ERC-20 TRANSFER:                       
----------------------------------------------------------------------
Function:        transfer
Recipient:       0xeb98b3a7bf0e139b08164f01824c6aae93b11c6a
Amount (wei):    200000000
Amount (hex):    0x000000000000000000000000000000000000000000000000000000000bebc200

Possible amounts (by token decimals):
  18 decimals:   0.0000000002 (very small amount - likely not 18 decimals)
  6 decimals:    200 (most likely - USDC/USDT use 6 decimals)
  8 decimals:    2 (possible - some tokens use 8 decimals)

======================================================================
```

## Transaction Details Explained

### Chain ID: 43114
This is the Avalanche C-Chain network identifier.

### Data Field Breakdown
The data field `0xa9059cbb...` contains:
- `a9059cbb`: Function selector for ERC-20 `transfer(address,uint256)`
- Next 64 hex chars: Recipient address (padded)
- Next 64 hex chars: Transfer amount in wei/smallest unit

### Gas and Gas Price
- **Gas**: `0x19073` (102,515 in decimal) - Maximum gas units for the transaction
- **Gas Price**: `0x1ee62800` (518,000,000 in decimal, or 518 Gwei)

## Sending Transactions (Implementation Required)

**⚠️ WARNING**: This tool does NOT send transactions by default for security reasons.

To actually send transactions, you would need to:

1. **Install web3.py**:
   ```bash
   pip install web3
   ```

2. **Use a private key** (NEVER commit or share this):
   ```python
   from web3 import Web3
   
   # Connect to Avalanche C-Chain
   w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
   
   # Prepare transaction
   transaction = {
       'chainId': 43114,
       'from': '0xYourAddress',
       'to': '0xRecipientAddress',
       'value': 0,
       'gas': 102515,
       'gasPrice': 518000000,
       'nonce': 42,
       'data': '0xYourData'
   }
   
   # Sign transaction with private key
   signed_tx = w3.eth.account.sign_transaction(transaction, 'YOUR_PRIVATE_KEY')
   
   # Send transaction
   tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
   print(f"Transaction sent: {tx_hash.hex()}")
   ```

3. **Alternative RPC Endpoints**:
   - Avalanche Mainnet: `https://api.avax.network/ext/bc/C/rpc`
   - Avalanche Testnet (Fuji): `https://api.avax-test.network/ext/bc/C/rpc`

## Security Considerations

🔐 **IMPORTANT SECURITY NOTES**:

1. **Never share your private keys**
2. **Never commit private keys to version control**
3. **Always verify transaction details before sending**
4. **Test on testnet first** (Fuji testnet for Avalanche)
5. **Use environment variables** for sensitive data
6. **Double-check recipient addresses** - transactions are irreversible
7. **Verify gas prices** to avoid overpaying

## Requirements

- Python 3.6+
- No external dependencies for basic parsing and validation

### Optional (for actual transaction sending):
- `web3.py` - For interacting with Ethereum/Avalanche nodes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Disclaimer

This tool is provided for educational purposes. Always exercise caution when handling cryptocurrency transactions. The authors are not responsible for any losses incurred through the use of this tool.

---

*Part of the Mr. Matrix - WORMGPT-V2V.X project*
