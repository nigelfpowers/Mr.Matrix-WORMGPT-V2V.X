"""
Ethereum Address Checker Utility

This utility provides functions to check Ethereum address balances and details
using web3.py library.
"""

from web3 import Web3
import json

# The target Ethereum address
TARGET_ADDRESS = '0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50'

class EthereumAddressChecker:
    """Class to check Ethereum address information"""
    
    def __init__(self, rpc_url=None):
        """
        Initialize the checker with an RPC URL
        
        Args:
            rpc_url (str): The Ethereum RPC URL. If None, uses a default provider.
        """
        if rpc_url:
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        else:
            # Default to a public Ethereum mainnet endpoint
            # Note: For production use, you should use your own RPC endpoint (Infura, Alchemy, etc.)
            self.w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
        
        if not self.w3.is_connected():
            print("Warning: Not connected to Ethereum network")
    
    def is_valid_address(self, address):
        """
        Check if an address is valid
        
        Args:
            address (str): The Ethereum address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return Web3.is_address(address)
    
    def get_checksum_address(self, address):
        """
        Convert an address to its checksum format
        
        Args:
            address (str): The Ethereum address
            
        Returns:
            str: The checksummed address
        """
        try:
            return Web3.to_checksum_address(address)
        except Exception as e:
            return None
    
    def get_balance(self, address):
        """
        Get the balance of an address
        
        Args:
            address (str): The Ethereum address
            
        Returns:
            dict: Balance information
        """
        try:
            checksum_address = self.get_checksum_address(address)
            if not checksum_address:
                return {
                    'address': address,
                    'error': 'Invalid address format',
                    'success': False
                }
            
            balance_wei = self.w3.eth.get_balance(checksum_address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            return {
                'address': checksum_address,
                'balance_wei': str(balance_wei),
                'balance_eth': str(balance_eth),
                'success': True
            }
        except Exception as e:
            return {
                'address': address,
                'error': str(e),
                'success': False
            }
    
    def is_contract(self, address):
        """
        Check if an address is a smart contract
        
        Args:
            address (str): The Ethereum address
            
        Returns:
            dict: Contract status information
        """
        try:
            checksum_address = self.get_checksum_address(address)
            if not checksum_address:
                return {
                    'address': address,
                    'error': 'Invalid address format',
                    'success': False
                }
            
            code = self.w3.eth.get_code(checksum_address)
            is_contract_address = len(code) > 0
            
            return {
                'address': checksum_address,
                'is_contract': is_contract_address,
                'code_length': len(code),
                'success': True
            }
        except Exception as e:
            return {
                'address': address,
                'error': str(e),
                'success': False
            }
    
    def get_transaction_count(self, address):
        """
        Get the transaction count (nonce) for an address
        
        Args:
            address (str): The Ethereum address
            
        Returns:
            int: Number of transactions sent from this address
        """
        try:
            checksum_address = self.get_checksum_address(address)
            if not checksum_address:
                return None
            
            return self.w3.eth.get_transaction_count(checksum_address)
        except Exception as e:
            return None
    
    def get_address_info(self, address):
        """
        Get comprehensive information about an address
        
        Args:
            address (str): The Ethereum address
            
        Returns:
            dict: Complete address information
        """
        try:
            checksum_address = self.get_checksum_address(address)
            if not checksum_address:
                return {
                    'address': address,
                    'error': 'Invalid address format',
                    'success': False
                }
            
            # Get balance
            balance_wei = self.w3.eth.get_balance(checksum_address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            # Check if contract
            code = self.w3.eth.get_code(checksum_address)
            is_contract_address = len(code) > 0
            
            # Get transaction count
            tx_count = self.w3.eth.get_transaction_count(checksum_address)
            
            return {
                'address': checksum_address,
                'balance': {
                    'wei': str(balance_wei),
                    'eth': str(balance_eth)
                },
                'is_contract': is_contract_address,
                'transaction_count': tx_count,
                'type': 'Contract' if is_contract_address else 'EOA (Externally Owned Account)',
                'success': True
            }
        except Exception as e:
            return {
                'address': address,
                'error': str(e),
                'success': False
            }
    
    def get_true_value(self, address=TARGET_ADDRESS):
        """
        Get the true value and comprehensive information about the target address
        
        Args:
            address (str): The Ethereum address (defaults to TARGET_ADDRESS)
            
        Returns:
            dict: Complete information about the address
        """
        print(f"Checking true value of address: {address}")
        info = self.get_address_info(address)
        
        if info['success']:
            print('\n=== Address Information ===')
            print(f"Address: {info['address']}")
            print(f"Type: {info['type']}")
            print(f"Balance: {info['balance']['eth']} ETH ({info['balance']['wei']} Wei)")
            print(f"Transaction Count: {info['transaction_count']}")
            print(f"Is Contract: {info['is_contract']}")
            print('===========================\n')
        else:
            print(f"Error: {info['error']}")
        
        return info


def main():
    """Main function to demonstrate the utility"""
    print('Ethereum Address Checker Utility\n')
    print('Checking target address...\n')
    
    # Initialize checker
    checker = EthereumAddressChecker()
    
    # Check if the address is valid
    if checker.is_valid_address(TARGET_ADDRESS):
        print(f"✓ Address {TARGET_ADDRESS} is valid\n")
        
        # Get the true value
        result = checker.get_true_value(TARGET_ADDRESS)
        
        # Print result as JSON
        print("\nJSON Output:")
        print(json.dumps(result, indent=2))
    else:
        print(f"✗ Address {TARGET_ADDRESS} is not valid")


if __name__ == "__main__":
    main()
