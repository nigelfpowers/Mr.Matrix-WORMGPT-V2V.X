#!/usr/bin/env python3
"""
Smart Contract Query and Balance Finder
A comprehensive tool for querying smart contracts and finding token balances on EVM chains
"""

import json
from decimal import Decimal
from typing import Dict, List, Optional, Tuple


class ContractQueryBalanceFinder:
    """
    Handles smart contract queries and balance finding on EVM-compatible chains
    Supports Avalanche C-Chain (43114) and other EVM networks
    """
    
    # Standard ERC-20 ABI function signatures
    ERC20_FUNCTIONS = {
        'balanceOf': '0x70a08231',  # balanceOf(address)
        'totalSupply': '0x18160ddd',  # totalSupply()
        'decimals': '0x313ce567',  # decimals()
        'symbol': '0x95d89b41',  # symbol()
        'name': '0x06fdde03',  # name()
        'allowance': '0xdd62ed3e',  # allowance(address,address)
    }
    
    # Common vault function signatures
    VAULT_FUNCTIONS = {
        'totalAssets': '0x01e1d114',  # totalAssets()
        'balanceOf': '0x70a08231',  # balanceOf(address)
        'pricePerShare': '0x99530b06',  # pricePerShare()
        'totalSupply': '0x18160ddd',  # totalSupply()
    }
    
    def __init__(self, chain_id: int = 43114):
        """
        Initialize the contract query tool
        
        Args:
            chain_id: EVM chain ID (default: 43114 for Avalanche C-Chain)
        """
        self.chain_id = chain_id
        self.chain_names = {
            1: 'Ethereum Mainnet',
            43114: 'Avalanche C-Chain',
            56: 'Binance Smart Chain',
            137: 'Polygon',
            250: 'Fantom',
            42161: 'Arbitrum One',
            10: 'Optimism',
        }
    
    def get_chain_name(self) -> str:
        """Get the human-readable name of the current chain"""
        return self.chain_names.get(self.chain_id, f"Chain {self.chain_id}")
    
    def _is_valid_address(self, address: str) -> bool:
        """Validate Ethereum address format"""
        if not isinstance(address, str):
            return False
        if not address.startswith('0x'):
            return False
        if len(address) != 42:  # 0x + 40 hex characters
            return False
        try:
            int(address, 16)
            return True
        except ValueError:
            return False
    
    def _pad_address(self, address: str) -> str:
        """Pad address to 32 bytes (64 hex chars) for function call data"""
        if address.startswith('0x'):
            address = address[2:]
        return address.lower().zfill(64)
    
    def encode_balance_of_call(self, address: str) -> str:
        """
        Encode balanceOf(address) function call
        
        Args:
            address: Address to check balance for
            
        Returns:
            Encoded function call data
        """
        if not self._is_valid_address(address):
            raise ValueError(f"Invalid address: {address}")
        
        function_sig = self.ERC20_FUNCTIONS['balanceOf']
        padded_address = self._pad_address(address)
        
        return function_sig + padded_address
    
    def encode_total_supply_call(self) -> str:
        """Encode totalSupply() function call"""
        return self.ERC20_FUNCTIONS['totalSupply']
    
    def encode_decimals_call(self) -> str:
        """Encode decimals() function call"""
        return self.ERC20_FUNCTIONS['decimals']
    
    def encode_symbol_call(self) -> str:
        """Encode symbol() function call"""
        return self.ERC20_FUNCTIONS['symbol']
    
    def encode_name_call(self) -> str:
        """Encode name() function call"""
        return self.ERC20_FUNCTIONS['name']
    
    def encode_vault_total_assets_call(self) -> str:
        """Encode totalAssets() function call for vault contracts"""
        return self.VAULT_FUNCTIONS['totalAssets']
    
    def encode_vault_price_per_share_call(self) -> str:
        """Encode pricePerShare() function call for vault contracts"""
        return self.VAULT_FUNCTIONS['pricePerShare']
    
    def decode_uint256_response(self, response: str) -> int:
        """
        Decode uint256 response from contract call
        
        Args:
            response: Hex string response from contract
            
        Returns:
            Decoded integer value
        """
        if response.startswith('0x'):
            response = response[2:]
        
        # Pad to 64 characters if needed
        response = response.zfill(64)
        
        return int(response, 16)
    
    def decode_string_response(self, response: str) -> str:
        """
        Decode string response from contract call
        
        Args:
            response: Hex string response from contract
            
        Returns:
            Decoded string value
        """
        if response.startswith('0x'):
            response = response[2:]
        
        # String responses have: offset (32 bytes), length (32 bytes), data
        # Skip the offset and read length
        try:
            length = int(response[64:128], 16)
            # Extract string data
            string_hex = response[128:128 + (length * 2)]
            # Convert hex to bytes and decode
            return bytes.fromhex(string_hex).decode('utf-8')
        except Exception:
            return f"Unable to decode: 0x{response}"
    
    def create_balance_query(self, contract_address: str, wallet_address: str) -> Dict:
        """
        Create a balance query for an ERC-20 token
        
        Args:
            contract_address: Token contract address
            wallet_address: Wallet address to check balance
            
        Returns:
            Query dictionary with call parameters
        """
        if not self._is_valid_address(contract_address):
            raise ValueError(f"Invalid contract address: {contract_address}")
        
        if not self._is_valid_address(wallet_address):
            raise ValueError(f"Invalid wallet address: {wallet_address}")
        
        call_data = self.encode_balance_of_call(wallet_address)
        
        return {
            'to': contract_address.lower(),
            'data': call_data,
            'description': f'balanceOf({wallet_address}) on {contract_address}'
        }
    
    def create_total_supply_query(self, contract_address: str) -> Dict:
        """
        Create a total supply query for an ERC-20 token
        
        Args:
            contract_address: Token contract address
            
        Returns:
            Query dictionary with call parameters
        """
        if not self._is_valid_address(contract_address):
            raise ValueError(f"Invalid contract address: {contract_address}")
        
        call_data = self.encode_total_supply_call()
        
        return {
            'to': contract_address.lower(),
            'data': call_data,
            'description': f'totalSupply() on {contract_address}'
        }
    
    def create_vault_query(self, vault_address: str) -> Dict:
        """
        Create a query for vault total assets
        
        Args:
            vault_address: Vault contract address
            
        Returns:
            Query dictionary with call parameters
        """
        if not self._is_valid_address(vault_address):
            raise ValueError(f"Invalid vault address: {vault_address}")
        
        call_data = self.encode_vault_total_assets_call()
        
        return {
            'to': vault_address.lower(),
            'data': call_data,
            'description': f'totalAssets() on vault {vault_address}'
        }
    
    def create_multi_balance_query(self, tokens: List[Tuple[str, str]]) -> List[Dict]:
        """
        Create multiple balance queries
        
        Args:
            tokens: List of tuples (contract_address, wallet_address)
            
        Returns:
            List of query dictionaries
        """
        queries = []
        for contract_addr, wallet_addr in tokens:
            try:
                query = self.create_balance_query(contract_addr, wallet_addr)
                queries.append(query)
            except ValueError as e:
                print(f"⚠ Skipping invalid query: {e}")
        
        return queries
    
    def calculate_total_balance(
        self,
        balances: List[Tuple[str, int, int, Optional[float]]],
    ) -> Dict:
        """
        Calculate total balance in USD from multiple tokens
        
        Args:
            balances: List of tuples (token_symbol, balance, decimals, price_usd)
            
        Returns:
            Dictionary with total balance details
        """
        total_usd = Decimal('0')
        token_details = []
        
        for token_symbol, balance, decimals, price_usd in balances:
            # Convert balance to human-readable
            human_balance = Decimal(balance) / Decimal(10 ** decimals)
            
            # Calculate USD value if price provided
            usd_value = None
            if price_usd is not None:
                usd_value = human_balance * Decimal(str(price_usd))
                total_usd += usd_value
            
            token_details.append({
                'symbol': token_symbol,
                'balance': human_balance,
                'balance_raw': balance,
                'decimals': decimals,
                'price_usd': price_usd,
                'value_usd': usd_value
            })
        
        return {
            'tokens': token_details,
            'total_usd': total_usd,
            'token_count': len(token_details)
        }
    
    def format_balance_summary(self, balance_data: Dict) -> str:
        """
        Format balance summary for display
        
        Args:
            balance_data: Balance data from calculate_total_balance
            
        Returns:
            Formatted string
        """
        lines = []
        lines.append("="*80)
        lines.append("TOKEN BALANCE SUMMARY".center(80))
        lines.append("="*80)
        lines.append("")
        
        for token in balance_data['tokens']:
            lines.append(f"Token: {token['symbol']}")
            lines.append(f"  Balance:        {token['balance']}")
            lines.append(f"  Raw Balance:    {token['balance_raw']}")
            lines.append(f"  Decimals:       {token['decimals']}")
            
            if token['price_usd'] is not None:
                lines.append(f"  Price (USD):    ${token['price_usd']:.4f}")
                lines.append(f"  Value (USD):    ${token['value_usd']:.2f}")
            else:
                lines.append(f"  Price (USD):    Not provided")
            
            lines.append("")
        
        lines.append("-"*80)
        lines.append(f"Total Tokens:     {balance_data['token_count']}")
        if balance_data['total_usd'] > 0:
            lines.append(f"Total Value:      ${balance_data['total_usd']:.2f} USD")
        lines.append("="*80)
        
        return "\n".join(lines)
    
    def format_contract_query(self, query: Dict) -> str:
        """
        Format contract query for display
        
        Args:
            query: Query dictionary
            
        Returns:
            Formatted string
        """
        lines = []
        lines.append("="*80)
        lines.append("CONTRACT QUERY".center(80))
        lines.append("="*80)
        lines.append("")
        lines.append(f"Chain:           {self.get_chain_name()} (ID: {self.chain_id})")
        lines.append(f"Contract:        {query['to']}")
        lines.append(f"Call Data:       {query['data']}")
        lines.append(f"Description:     {query.get('description', 'N/A')}")
        lines.append("")
        lines.append("="*80)
        
        return "\n".join(lines)
    
    def generate_web3_query_code(self, query: Dict) -> str:
        """
        Generate Python code for executing contract query with web3.py
        
        Args:
            query: Query dictionary
            
        Returns:
            Python code string
        """
        code = f"""
# Install web3.py: pip install web3
from web3 import Web3

# Connect to chain
w3 = Web3(Web3.HTTPProvider('YOUR_RPC_ENDPOINT'))  # e.g., https://api.avax.network/ext/bc/C/rpc

# Execute contract call
result = w3.eth.call({{
    'to': '{query['to']}',
    'data': '{query['data']}'
}})

# Decode result (uint256 example)
decoded_value = int(result.hex(), 16)
print(f"Result: {{decoded_value}}")
"""
        return code


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║        Smart Contract Query & Balance Finder v1.0                   ║
    ║                                                                      ║
    ║        Query contracts and find token balances on EVM chains        ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def example_balance_queries():
    """Demonstrate balance query functionality"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Query ERC-20 Token Balance".center(80))
    print("="*80 + "\n")
    
    finder = ContractQueryBalanceFinder(chain_id=43114)
    
    # Example: Query USDC balance for an address on Avalanche
    usdc_contract = "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E"  # USDC on Avalanche
    wallet_address = "0x3e172fde66cefa9f4a4c373fe0932311fda11a76"
    
    query = finder.create_balance_query(usdc_contract, wallet_address)
    print(finder.format_contract_query(query))
    
    print("\nTo execute this query with web3.py:")
    print("-"*80)
    print(finder.generate_web3_query_code(query))
    print("-"*80)


def example_total_supply_query():
    """Demonstrate total supply query functionality"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Query Token Total Supply".center(80))
    print("="*80 + "\n")
    
    finder = ContractQueryBalanceFinder(chain_id=43114)
    
    # Example: Query WAVAX total supply
    wavax_contract = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"  # WAVAX on Avalanche
    
    query = finder.create_total_supply_query(wavax_contract)
    print(finder.format_contract_query(query))
    
    print("\nTo execute this query with web3.py:")
    print("-"*80)
    print(finder.generate_web3_query_code(query))
    print("-"*80)


def example_vault_query():
    """Demonstrate vault query functionality"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Query Vault Total Assets".center(80))
    print("="*80 + "\n")
    
    finder = ContractQueryBalanceFinder(chain_id=43114)
    
    # Example: Query a vault contract
    vault_address = "0x152b9d0fdc40c096757f570a51e494bd4b943e50"  # Example vault
    
    query = finder.create_vault_query(vault_address)
    print(finder.format_contract_query(query))
    
    print("\nTo execute this query with web3.py:")
    print("-"*80)
    print(finder.generate_web3_query_code(query))
    print("-"*80)


def example_multi_balance():
    """Demonstrate multi-token balance calculation"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Calculate Total Balance Across Multiple Tokens".center(80))
    print("="*80 + "\n")
    
    finder = ContractQueryBalanceFinder(chain_id=43114)
    
    # Example balance data (in real usage, this would come from contract calls)
    # Format: (symbol, balance_raw, decimals, price_usd)
    example_balances = [
        ('USDC', 500000000, 6, 1.00),  # 500 USDC at $1.00
        ('WAVAX', 10000000000000000000, 18, 35.50),  # 10 WAVAX at $35.50
        ('BTC.b', 5000000, 8, 45000.00),  # 0.05 BTC at $45,000
    ]
    
    balance_data = finder.calculate_total_balance(example_balances)
    print(finder.format_balance_summary(balance_data))


def example_multi_token_queries():
    """Demonstrate creating multiple balance queries"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Create Multiple Balance Queries".center(80))
    print("="*80 + "\n")
    
    finder = ContractQueryBalanceFinder(chain_id=43114)
    
    # Example: Query balances for multiple tokens for same wallet
    wallet = "0x3e172fde66cefa9f4a4c373fe0932311fda11a76"
    tokens = [
        ("0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E", wallet),  # USDC
        ("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", wallet),  # WAVAX
        ("0x152b9d0fdc40c096757f570a51e494bd4b943e50", wallet),  # Token 3
    ]
    
    queries = finder.create_multi_balance_query(tokens)
    
    print(f"Generated {len(queries)} balance queries:\n")
    for i, query in enumerate(queries, 1):
        print(f"Query {i}:")
        print(f"  Contract: {query['to']}")
        print(f"  Data:     {query['data']}")
        print(f"  Desc:     {query['description']}")
        print()
    
    print("-"*80)
    print("To execute all queries with web3.py:")
    print("-"*80)
    print("""
from web3 import Web3

# Connect to Avalanche C-Chain
w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))

# Execute all queries
balances = []
for query in queries:
    result = w3.eth.call({
        'to': query['to'],
        'data': query['data']
    })
    balance = int(result.hex(), 16)
    balances.append(balance)
    print(f"{query['description']}: {balance}")
    """)
    print("-"*80)


def main():
    """Main entry point"""
    print_banner()
    
    # Run all examples
    example_balance_queries()
    example_total_supply_query()
    example_vault_query()
    example_multi_balance()
    example_multi_token_queries()
    
    print("\n" + "="*80)
    print("For complete documentation, see CONTRACT_QUERY_README.md".center(80))
    print("="*80 + "\n")
    
    return 0


if __name__ == "__main__":
    exit(main())
