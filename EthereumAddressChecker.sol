// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title EthereumAddressChecker
 * @dev A simple contract to interact with and check Ethereum addresses
 */
contract EthereumAddressChecker {
    
    // The target address we're checking
    address public constant TARGET_ADDRESS = 0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50;
    
    // Event emitted when address balance is checked
    event BalanceChecked(address indexed checkedAddress, uint256 balance);
    
    // Event emitted when value is sent to an address
    event ValueSent(address indexed recipient, uint256 amount);
    
    /**
     * @dev Get the balance of the target address
     * @return The balance in wei
     */
    function getTargetBalance() public view returns (uint256) {
        return TARGET_ADDRESS.balance;
    }
    
    /**
     * @dev Get the balance of any address
     * @param _address The address to check
     * @return The balance in wei
     */
    function getAddressBalance(address _address) public view returns (uint256) {
        return _address.balance;
    }
    
    /**
     * @dev Check if the target address is a contract
     * @return true if it's a contract, false if it's an EOA (externally owned account)
     */
    function isTargetContract() public view returns (bool) {
        return isContract(TARGET_ADDRESS);
    }
    
    /**
     * @dev Check if any address is a contract
     * @param _address The address to check
     * @return true if it's a contract, false if it's an EOA
     */
    function isContract(address _address) public view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(_address)
        }
        return size > 0;
    }
    
    /**
     * @dev Send ETH to the target address
     * @notice This function is payable and will forward the sent ETH to the target address
     */
    function sendToTarget() public payable {
        require(msg.value > 0, "Must send some ETH");
        (bool success, ) = TARGET_ADDRESS.call{value: msg.value}("");
        require(success, "Transfer failed");
        emit ValueSent(TARGET_ADDRESS, msg.value);
    }
    
    /**
     * @dev Send ETH to any address
     * @param _recipient The address to send ETH to
     */
    function sendToAddress(address payable _recipient) public payable {
        require(msg.value > 0, "Must send some ETH");
        (bool success, ) = _recipient.call{value: msg.value}("");
        require(success, "Transfer failed");
        emit ValueSent(_recipient, msg.value);
    }
    
    /**
     * @dev Get the true value (balance) and type of the target address
     * @return balance The balance in wei
     * @return isContractAddress Whether the address is a contract
     */
    function getTrueValue() public view returns (uint256 balance, bool isContractAddress) {
        balance = TARGET_ADDRESS.balance;
        isContractAddress = isContract(TARGET_ADDRESS);
    }
    
    /**
     * @dev Get comprehensive information about any address
     * @param _address The address to check
     * @return balance The balance in wei
     * @return isContractAddress Whether the address is a contract
     */
    function getAddressInfo(address _address) public view returns (
        uint256 balance,
        bool isContractAddress
    ) {
        balance = _address.balance;
        isContractAddress = isContract(_address);
    }
}
