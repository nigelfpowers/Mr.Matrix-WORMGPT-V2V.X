# Smart Contract Query & Balance Finder

A comprehensive Python tool for querying smart contracts and finding token balances on EVM-compatible blockchains.

## Overview

This tool provides functionality to:

- 🔍 **Query Smart Contracts**: Generate and execute read-only contract calls
- 💰 **Check Token Balances**: Query ERC-20 token balances for any address
- 🏦 **Vault Queries**: Query vault contract data (totalAssets, pricePerShare, etc.)
- 📊 **Multi-Token Balances**: Calculate total portfolio value across multiple tokens
- 🔗 **Multi-Chain Support**: Works with Avalanche, Ethereum, BSC, Polygon, and other EVM chains

## Features

### ERC-20 Token Queries

Supports standard ERC-20 function calls:
- `balanceOf(address)` - Check token balance for an address
- `totalSupply()` - Get total token supply
- `decimals()` - Get token decimal places
- `symbol()` - Get token symbol
- `name()` - Get token name
- `allowance(owner, spender)` - Check allowance amount

### Vault Contract Queries

Supports common vault contract functions:
- `totalAssets()` - Get total assets in vault
- `balanceOf(address)` - Get vault share balance
- `pricePerShare()` - Get price per vault share
- `totalSupply()` - Get total vault shares

### Balance Calculation

- Query multiple tokens simultaneously
- Calculate total portfolio value in USD
- Support for tokens with different decimal configurations
- Automatic address validation

## Installation

### Basic Requirements
- Python 3.6+
- No external dependencies for query generation

### For Actual Execution (Optional)
```bash
pip install web3
```

## Usage

### 1. Query Single Token Balance

```python
from contract_query_balance_finder import ContractQueryBalanceFinder

# Initialize for Avalanche C-Chain
finder = ContractQueryBalanceFinder(chain_id=43114)

# Create balance query
usdc_contract = "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E"
wallet = "0x3e172fde66cefa9f4a4c373fe0932311fda11a76"

query = finder.create_balance_query(usdc_contract, wallet)
print(query)
# Output: {'to': '0x...', 'data': '0x70a08231...', 'description': '...'}
```

### 2. Query Token Total Supply

```python
# Query total supply of WAVAX
wavax_contract = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"
query = finder.create_total_supply_query(wavax_contract)
```

### 3. Query Vault Contract

```python
# Query vault total assets
vault_address = "0x152b9d0fdc40c096757f570a51e494bd4b943e50"
query = finder.create_vault_query(vault_address)
```

### 4. Multi-Token Balance Calculation

```python
# Calculate total balance across multiple tokens
balances = [
    ('USDC', 500000000, 6, 1.00),      # 500 USDC
    ('WAVAX', 10000000000000000000, 18, 35.50),  # 10 WAVAX
    ('BTC.b', 5000000, 8, 45000.00),   # 0.05 BTC
]

balance_data = finder.calculate_total_balance(balances)
print(finder.format_balance_summary(balance_data))
```

### 5. Execute Queries with web3.py

```python
from web3 import Web3
from contract_query_balance_finder import ContractQueryBalanceFinder

# Connect to Avalanche C-Chain
w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))

# Create query
finder = ContractQueryBalanceFinder(chain_id=43114)
query = finder.create_balance_query(
    contract_address="0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",  # USDC
    wallet_address="0x3e172fde66cefa9f4a4c373fe0932311fda11a76"
)

# Execute query
result = w3.eth.call({
    'to': query['to'],
    'data': query['data']
})

# Decode uint256 result
balance = finder.decode_uint256_response(result.hex())
print(f"Balance: {balance}")

# Convert to human-readable (assuming 6 decimals for USDC)
human_balance = balance / (10 ** 6)
print(f"Human-readable balance: {human_balance} USDC")
```

## Running Examples

Run the script to see all examples in action:

```bash
python3 contract_query_balance_finder.py
```

This will display:
1. Balance query example
2. Total supply query example
3. Vault query example
4. Multi-token balance calculation
5. Batch query generation

## Supported Networks

The tool supports any EVM-compatible chain. Common networks:

| Network | Chain ID | RPC Endpoint |
|---------|----------|--------------|
| Avalanche C-Chain | 43114 | https://api.avax.network/ext/bc/C/rpc |
| Ethereum Mainnet | 1 | https://eth.llamarpc.com |
| Binance Smart Chain | 56 | https://bsc-dataseed.binance.org/ |
| Polygon | 137 | https://polygon-rpc.com |
| Fantom | 250 | https://rpc.ftm.tools |
| Arbitrum One | 42161 | https://arb1.arbitrum.io/rpc |
| Optimism | 10 | https://mainnet.optimism.io |

## API Reference

### Class: ContractQueryBalanceFinder

#### Methods

##### `__init__(chain_id=43114)`
Initialize the query tool for a specific chain.

##### `create_balance_query(contract_address, wallet_address)`
Create a query to check ERC-20 token balance.

**Returns:** Query dictionary with `to`, `data`, and `description` fields.

##### `create_total_supply_query(contract_address)`
Create a query to check token total supply.

##### `create_vault_query(vault_address)`
Create a query to check vault total assets.

##### `create_multi_balance_query(tokens)`
Create multiple balance queries at once.

**Args:** List of tuples `[(contract_address, wallet_address), ...]`

##### `calculate_total_balance(balances)`
Calculate total portfolio value in USD.

**Args:** List of tuples `[(symbol, balance, decimals, price_usd), ...]`

##### `decode_uint256_response(response)`
Decode a uint256 response from a contract call.

##### `decode_string_response(response)`
Decode a string response from a contract call.

##### `encode_balance_of_call(address)`
Encode balanceOf(address) function call data.

##### `encode_total_supply_call()`
Encode totalSupply() function call data.

##### `encode_decimals_call()`
Encode decimals() function call data.

## Advanced Usage

### Query Multiple Balances and Calculate Total

```python
from web3 import Web3
from contract_query_balance_finder import ContractQueryBalanceFinder

# Setup
w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
finder = ContractQueryBalanceFinder(chain_id=43114)
wallet = "0xYourWalletAddress"

# Define tokens to query
tokens_config = [
    ("0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E", "USDC", 6, 1.00),
    ("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", "WAVAX", 18, 35.50),
]

# Query all balances
balance_results = []
for contract_addr, symbol, decimals, price in tokens_config:
    query = finder.create_balance_query(contract_addr, wallet)
    result = w3.eth.call({'to': query['to'], 'data': query['data']})
    balance = finder.decode_uint256_response(result.hex())
    balance_results.append((symbol, balance, decimals, price))

# Calculate total
total_data = finder.calculate_total_balance(balance_results)
print(finder.format_balance_summary(total_data))
```

### Query Vault Information

```python
from web3 import Web3
from contract_query_balance_finder import ContractQueryBalanceFinder

w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
finder = ContractQueryBalanceFinder(chain_id=43114)

vault_address = "0xYourVaultAddress"

# Query total assets in vault
query = finder.create_vault_query(vault_address)
result = w3.eth.call({'to': query['to'], 'data': query['data']})
total_assets = finder.decode_uint256_response(result.hex())

print(f"Vault Total Assets: {total_assets}")
```

## Function Signatures Reference

### ERC-20 Standard Functions

| Function | Signature | Selector |
|----------|-----------|----------|
| balanceOf(address) | `0x70a08231` | Get balance of address |
| totalSupply() | `0x18160ddd` | Get total token supply |
| decimals() | `0x313ce567` | Get token decimals |
| symbol() | `0x95d89b41` | Get token symbol |
| name() | `0x06fdde03` | Get token name |
| allowance(address,address) | `0xdd62ed3e` | Get allowance amount |

### Vault Functions

| Function | Signature | Selector |
|----------|-----------|----------|
| totalAssets() | `0x01e1d114` | Get total vault assets |
| pricePerShare() | `0x99530b06` | Get price per share |
| balanceOf(address) | `0x70a08231` | Get vault share balance |

## Common Token Contracts on Avalanche

| Token | Contract Address | Decimals |
|-------|------------------|----------|
| USDC | 0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E | 6 |
| USDT | 0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7 | 6 |
| WAVAX | 0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7 | 18 |
| BTC.b | 0x152b9d0FdC40C096757F570A51E494bd4b943E50 | 8 |
| WETH.e | 0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB | 18 |

## Error Handling

The tool includes comprehensive error handling:

```python
try:
    query = finder.create_balance_query(contract, wallet)
except ValueError as e:
    print(f"Error: {e}")
    # Handle invalid address or other validation errors
```

## Security Considerations

🔐 **IMPORTANT**:

1. **Read-Only Operations**: All contract queries are read-only (eth_call)
2. **No Private Keys**: This tool does not require or handle private keys
3. **Address Validation**: All addresses are validated before query generation
4. **No State Changes**: Contract queries do not modify blockchain state
5. **RPC Endpoints**: Use trusted RPC endpoints to avoid data manipulation

## Performance Tips

1. **Batch Queries**: Use `create_multi_balance_query()` to prepare multiple queries
2. **Caching**: Cache contract decimals/symbols to reduce RPC calls
3. **Parallel Execution**: Execute multiple queries in parallel when possible
4. **Rate Limiting**: Respect RPC endpoint rate limits

## Troubleshooting

### "Invalid address" Error
- Ensure address starts with "0x"
- Ensure address is exactly 42 characters (0x + 40 hex chars)
- Check for typos or missing characters

### "Unable to decode" Error
- Verify the contract implements the function you're calling
- Check that the contract address is correct
- Ensure you're connected to the correct network

### RPC Connection Issues
- Verify RPC endpoint is accessible
- Check network connectivity
- Try alternative RPC endpoints for the same chain

## Examples Output

When you run `python3 contract_query_balance_finder.py`, you'll see:

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        Smart Contract Query & Balance Finder v1.0                   ║
║                                                                      ║
║        Query contracts and find token balances on EVM chains        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

[Multiple examples demonstrating all functionality...]
```

## Integration with Existing Tools

This tool complements the existing `avalanche_transaction_sender.py`:

- **Transaction Sender**: Prepares and sends transactions (write operations)
- **Contract Query**: Reads contract data (read operations)

Together, they provide a complete toolkit for Avalanche C-Chain interactions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

---

*Part of the Mr. Matrix - WORMGPT-V2V.X project*
