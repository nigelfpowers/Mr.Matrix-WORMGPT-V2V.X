#!/usr/bin/env python3
"""
Avalanche C-Chain Transaction Sender
A tool for sending Ethereum transactions on the Avalanche C-Chain
"""

import json
from decimal import Decimal
from typing import Dict, Optional


class AvalancheTransactionSender:
    """
    Handles Ethereum transactions on Avalanche C-Chain (chainId 43114)
    """
    
    def __init__(self):
        self.chainId = 43114  # Avalanche C-Chain
        
    def parse_transaction(self, tx_data: Dict) -> Dict:
        """
        Parse and validate transaction data
        
        Args:
            tx_data: Dictionary containing transaction parameters
            
        Returns:
            Parsed transaction dictionary
        """
        required_fields = ['from', 'to', 'data', 'gas', 'gasPrice', 'nonce', 'value']
        
        for field in required_fields:
            if field not in tx_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate addresses
        if not self._is_valid_address(tx_data['from']):
            raise ValueError(f"Invalid 'from' address: {tx_data['from']}")
        
        if not self._is_valid_address(tx_data['to']):
            raise ValueError(f"Invalid 'to' address: {tx_data['to']}")
        
        # Parse transaction
        parsed_tx = {
            'chainId': tx_data.get('chainId', self.chainId),
            'from': tx_data['from'],
            'to': tx_data['to'],
            'data': tx_data['data'],
            'gas': tx_data['gas'],
            'gasPrice': tx_data['gasPrice'],
            'nonce': tx_data['nonce'],
            'value': tx_data['value']
        }
        
        return parsed_tx
    
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
    
    def decode_transfer_data(self, data: str) -> Optional[Dict]:
        """
        Decode ERC-20 transfer function data
        
        Args:
            data: Hex string containing function signature and parameters
            
        Returns:
            Dictionary with decoded transfer information
        """
        if not data.startswith('0x'):
            return None
        
        # Remove 0x prefix
        data = data[2:]
        
        # ERC-20 transfer function signature: 0xa9059cbb
        if not data.startswith('a9059cbb'):
            return None
        
        # Extract parameters (after function signature)
        params = data[8:]
        
        if len(params) < 128:  # Need at least 64 chars for address + 64 for amount
            return None
        
        # First 64 chars (32 bytes) = recipient address (padded)
        recipient = '0x' + params[24:64]  # Remove padding, get last 40 chars
        
        # Next 64 chars (32 bytes) = amount
        amount_hex = params[64:128]
        amount = int(amount_hex, 16)
        
        return {
            'function': 'transfer',
            'recipient': recipient,
            'amount': amount,
            'amount_hex': '0x' + amount_hex
        }
    
    def format_transaction_summary(self, tx_data: Dict) -> str:
        """
        Format transaction data for display
        
        Args:
            tx_data: Transaction dictionary
            
        Returns:
            Formatted string summary
        """
        lines = []
        lines.append("="*70)
        lines.append("AVALANCHE C-CHAIN TRANSACTION DETAILS".center(70))
        lines.append("="*70)
        lines.append("")
        
        # Basic transaction info
        lines.append(f"Chain ID:        {tx_data.get('chainId', 'N/A')}")
        lines.append(f"From:            {tx_data['from']}")
        lines.append(f"To:              {tx_data['to']}")
        lines.append(f"Value:           {tx_data['value']}")
        lines.append(f"Gas:             {tx_data['gas']}")
        lines.append(f"Gas Price:       {tx_data['gasPrice']}")
        lines.append(f"Nonce:           {tx_data['nonce']}")
        lines.append("")
        
        # Decode data if it's a transfer
        if tx_data.get('data'):
            decoded = self.decode_transfer_data(tx_data['data'])
            if decoded:
                lines.append("-"*70)
                lines.append("DECODED ERC-20 TRANSFER:".center(70))
                lines.append("-"*70)
                lines.append(f"Function:        {decoded['function']}")
                lines.append(f"Recipient:       {decoded['recipient']}")
                lines.append(f"Amount (wei):    {decoded['amount']}")
                lines.append(f"Amount (hex):    {decoded['amount_hex']}")
                
                # Calculate human-readable amounts for common token decimals
                lines.append("")
                lines.append("Possible amounts (by token decimals):")
                for decimals in [18, 6, 8]:
                    human_amount = Decimal(decoded['amount']) / Decimal(10 ** decimals)
                    # Format to avoid scientific notation
                    if human_amount < 1:
                        # Use fixed-point notation for small numbers
                        lines.append(f"  {decimals} decimals:   {human_amount:.18f}".rstrip('0').rstrip('.'))
                    else:
                        lines.append(f"  {decimals} decimals:   {human_amount}")
            else:
                lines.append(f"Data:            {tx_data['data']}")
        
        lines.append("")
        lines.append("="*70)
        
        return "\n".join(lines)
    
    def prepare_transaction(self, tx_data: Dict) -> Dict:
        """
        Prepare transaction for sending (validation and formatting)
        
        Args:
            tx_data: Raw transaction data
            
        Returns:
            Prepared transaction dictionary
        """
        # Parse and validate
        parsed_tx = self.parse_transaction(tx_data)
        
        # Display summary
        summary = self.format_transaction_summary(parsed_tx)
        print(summary)
        
        return parsed_tx
    
    def send_transaction(self, tx_data: Dict, private_key: Optional[str] = None) -> str:
        """
        Send transaction to Avalanche C-Chain
        
        Note: This is a placeholder. Actual implementation would require:
        - web3.py library
        - Private key for signing
        - Connection to Avalanche RPC endpoint
        
        Args:
            tx_data: Transaction dictionary
            private_key: Private key for signing (optional, for demonstration)
            
        Returns:
            Transaction hash or error message
        """
        print("\n" + "!"*70)
        print("WARNING: Transaction sending is not implemented".center(70))
        print("!"*70)
        print("\nTo send this transaction, you would need to:")
        print("1. Install web3.py: pip install web3")
        print("2. Provide your private key (NEVER share or commit this)")
        print("3. Connect to an Avalanche C-Chain RPC endpoint")
        print("4. Sign and send the transaction using web3.py")
        print("\nExample implementation:")
        print("-"*70)
        print("""
from web3 import Web3

# Connect to Avalanche C-Chain
w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))

# Example: Use the parsed transaction data
transaction = {
    'chainId': 43114,
    'from': '0xYourAddress',
    'to': '0xRecipientAddress',
    'value': 0,
    'gas': 102515,
    'gasPrice': 518000000,
    'nonce': 42,
    'data': '0xYourTransactionData'
}

# Sign transaction with your private key
your_private_key = 'YOUR_PRIVATE_KEY_HERE'  # NEVER commit this!
signed_tx = w3.eth.account.sign_transaction(transaction, your_private_key)

# Send transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Transaction sent: {tx_hash.hex()}")
        """)
        print("-"*70)
        
        return "Transaction not sent - implementation required"


def main():
    """Main entry point"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║         Avalanche C-Chain Transaction Sender v1.0                 ║")
    print("║                                                                    ║")
    print("║         Parse and prepare Ethereum transactions for Avalanche     ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Example transaction from the problem statement
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
    
    # Create sender instance
    sender = AvalancheTransactionSender()
    
    try:
        # Prepare transaction
        prepared_tx = sender.prepare_transaction(transaction_data)
        
        # Attempt to send (will show instructions instead)
        result = sender.send_transaction(prepared_tx)
        
        print(f"\nResult: {result}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
