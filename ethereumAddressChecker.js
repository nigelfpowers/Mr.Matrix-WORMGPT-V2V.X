/**
 * Ethereum Address Checker Utility
 * 
 * This utility provides functions to check Ethereum address balances and details
 * using ethers.js library.
 */

const { ethers } = require('ethers');

// The target Ethereum address
const TARGET_ADDRESS = '0x52eb1cc878c40c436de5f70ef7ddc28b12e66a50';

/**
 * Get the balance of an Ethereum address
 * @param {string} address - The Ethereum address to check
 * @param {string} rpcUrl - The RPC URL (defaults to Ethereum mainnet via Infura)
 * @returns {Promise<Object>} - Object containing balance in ETH and Wei
 */
async function getAddressBalance(address, rpcUrl = null) {
    try {
        // Use default provider if no RPC URL is provided
        const provider = rpcUrl 
            ? new ethers.JsonRpcProvider(rpcUrl)
            : ethers.getDefaultProvider('mainnet');
        
        const balanceWei = await provider.getBalance(address);
        const balanceEth = ethers.formatEther(balanceWei);
        
        return {
            address: address,
            balanceWei: balanceWei.toString(),
            balanceEth: balanceEth,
            success: true
        };
    } catch (error) {
        return {
            address: address,
            error: error.message,
            success: false
        };
    }
}

/**
 * Check if an address is a contract
 * @param {string} address - The Ethereum address to check
 * @param {string} rpcUrl - The RPC URL
 * @returns {Promise<Object>} - Object containing contract status
 */
async function isContract(address, rpcUrl = null) {
    try {
        const provider = rpcUrl 
            ? new ethers.JsonRpcProvider(rpcUrl)
            : ethers.getDefaultProvider('mainnet');
        
        const code = await provider.getCode(address);
        const isContractAddress = code !== '0x';
        
        return {
            address: address,
            isContract: isContractAddress,
            code: code,
            success: true
        };
    } catch (error) {
        return {
            address: address,
            error: error.message,
            success: false
        };
    }
}

/**
 * Get comprehensive information about an Ethereum address
 * @param {string} address - The Ethereum address to check
 * @param {string} rpcUrl - The RPC URL
 * @returns {Promise<Object>} - Object containing all address information
 */
async function getAddressInfo(address, rpcUrl = null) {
    try {
        const provider = rpcUrl 
            ? new ethers.JsonRpcProvider(rpcUrl)
            : ethers.getDefaultProvider('mainnet');
        
        // Get balance
        const balanceWei = await provider.getBalance(address);
        const balanceEth = ethers.formatEther(balanceWei);
        
        // Check if it's a contract
        const code = await provider.getCode(address);
        const isContractAddress = code !== '0x';
        
        // Get transaction count (nonce)
        const transactionCount = await provider.getTransactionCount(address);
        
        return {
            address: address,
            balance: {
                wei: balanceWei.toString(),
                eth: balanceEth
            },
            isContract: isContractAddress,
            transactionCount: transactionCount,
            type: isContractAddress ? 'Contract' : 'EOA (Externally Owned Account)',
            success: true
        };
    } catch (error) {
        return {
            address: address,
            error: error.message,
            success: false
        };
    }
}

/**
 * Get the true value of the target address
 * @param {string} rpcUrl - Optional RPC URL
 * @returns {Promise<Object>} - Complete information about the target address
 */
async function getTrueValue(rpcUrl = null) {
    console.log(`Checking true value of address: ${TARGET_ADDRESS}`);
    const info = await getAddressInfo(TARGET_ADDRESS, rpcUrl);
    
    if (info.success) {
        console.log('\n=== Address Information ===');
        console.log(`Address: ${info.address}`);
        console.log(`Type: ${info.type}`);
        console.log(`Balance: ${info.balance.eth} ETH (${info.balance.wei} Wei)`);
        console.log(`Transaction Count: ${info.transactionCount}`);
        console.log(`Is Contract: ${info.isContract}`);
        console.log('===========================\n');
    } else {
        console.error(`Error: ${info.error}`);
    }
    
    return info;
}

/**
 * Validate if a string is a valid Ethereum address
 * @param {string} address - The address to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function isValidAddress(address) {
    return ethers.isAddress(address);
}

// Main execution if run directly
if (require.main === module) {
    (async () => {
        console.log('Ethereum Address Checker Utility\n');
        console.log('Checking target address...\n');
        
        // Check if the address is valid
        if (isValidAddress(TARGET_ADDRESS)) {
            console.log(`✓ Address ${TARGET_ADDRESS} is valid\n`);
            
            // Get the true value
            await getTrueValue();
        } else {
            console.error(`✗ Address ${TARGET_ADDRESS} is not valid`);
        }
    })();
}

// Export functions for use in other modules
module.exports = {
    TARGET_ADDRESS,
    getAddressBalance,
    isContract,
    getAddressInfo,
    getTrueValue,
    isValidAddress
};
