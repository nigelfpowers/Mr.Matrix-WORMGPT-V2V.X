# Quick Reference: Avalanche Blockchain Tools

This quick reference shows how to use the blockchain tools in the Mr. Matrix toolkit.

## Tools Overview

| Tool | Purpose | Operations |
|------|---------|------------|
| **contract_query_balance_finder.py** | Query contracts & check balances | Read-only (eth_call) |
| **avalanche_transaction_sender.py** | Prepare & send transactions | Write operations |

## Common Use Cases

### 1. Check Your Token Balance

```bash
python3 contract_query_balance_finder.py
```

This will show examples of querying USDC, WAVAX, and other token balances.

### 2. Calculate Total Portfolio Value

Query multiple tokens and get total USD value:

```python
from contract_query_balance_finder import ContractQueryBalanceFinder

finder = ContractQueryBalanceFinder(chain_id=43114)

# Your token holdings (symbol, raw_balance, decimals, price_usd)
holdings = [
    ('USDC', 500000000, 6, 1.00),
    ('WAVAX', 10000000000000000000, 18, 35.50),
]

total = finder.calculate_total_balance(holdings)
print(finder.format_balance_summary(total))
# Shows: Total Value: $855.00 USD
```

### 3. Query Vault Information

```python
vault_address = "0x152b9d0fdc40c096757f570a51e494bd4b943e50"
query = finder.create_vault_query(vault_address)
# Returns: Call data for totalAssets() query
```

### 4. Prepare a Token Transfer

```bash
python3 avalanche_transaction_sender.py
```

This will parse and validate the example transaction, showing decoded transfer details.

## Function Signatures Quick Reference

### ERC-20 Standard

```
balanceOf(address):      0x70a08231
totalSupply():           0x18160ddd
decimals():              0x313ce567
symbol():                0x95d89b41
name():                  0x06fdde03
```

### Vault Functions

```
totalAssets():           0x01e1d114
pricePerShare():         0x99530b06
balanceOf(address):      0x70a08231
```

### Transfer Function

```
transfer(address,uint256): 0xa9059cbb
```

## Avalanche C-Chain Details

- **Chain ID**: 43114
- **RPC Endpoint**: https://api.avax.network/ext/bc/C/rpc
- **Block Explorer**: https://snowtrace.io

## Common Tokens on Avalanche

| Token | Address | Decimals |
|-------|---------|----------|
| USDC | 0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E | 6 |
| WAVAX | 0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7 | 18 |
| BTC.b | 0x152b9d0FdC40C096757F570A51E494bd4b943E50 | 8 |

## Workflow Example

1. **Query balances** using contract_query_balance_finder.py
2. **Calculate totals** to see your portfolio value
3. **Prepare transactions** using avalanche_transaction_sender.py
4. **Execute with web3.py** (requires private key)

## Security Reminders

- 🔐 Never commit private keys
- ✅ Always verify transaction details before sending
- 🧪 Test on testnet first (Fuji: chainId 43113)
- 📖 Read the full documentation before using with real funds

## Documentation

- [CONTRACT_QUERY_README.md](CONTRACT_QUERY_README.md) - Contract query tool
- [AVALANCHE_TRANSACTION_README.md](AVALANCHE_TRANSACTION_README.md) - Transaction sender
- [STAKEUS_GLD_README.md](STAKEUS_GLD_README.md) - Staking calculator

---

*Part of the Mr. Matrix - WORMGPT-V2V.X project*
