#!/usr/bin/env node

/**
 * Example Usage of Ethereum Address Checker
 * 
 * This script demonstrates how to use the ethereumAddressChecker.js utility
 */

const checker = require('./ethereumAddressChecker');

async function runExamples() {
    console.log('═══════════════════════════════════════════════════════');
    console.log('  Ethereum Address Checker - Usage Examples');
    console.log('═══════════════════════════════════════════════════════\n');

    // Example 1: Check if address is valid
    console.log('Example 1: Validate Address');
    console.log('───────────────────────────────────────────────────────');
    const isValid = checker.isValidAddress(checker.TARGET_ADDRESS);
    console.log(`Address: ${checker.TARGET_ADDRESS}`);
    console.log(`Is Valid: ${isValid ? '✓' : '✗'}`);
    console.log();

    // Example 2: Get the true value of the target address
    console.log('Example 2: Get True Value of Target Address');
    console.log('───────────────────────────────────────────────────────');
    try {
        const trueValue = await checker.getTrueValue();
        if (trueValue.success) {
            console.log('✓ Success!');
            console.log(`Balance: ${trueValue.balance.eth} ETH`);
            console.log(`Type: ${trueValue.type}`);
            console.log(`Transactions: ${trueValue.transactionCount}`);
        } else {
            console.log(`✗ Error: ${trueValue.error}`);
        }
    } catch (error) {
        console.log(`✗ Network Error: ${error.message}`);
        console.log('Note: This requires internet access and an Ethereum RPC endpoint');
    }
    console.log();

    // Example 3: Check any other address
    console.log('Example 3: Check Any Address');
    console.log('───────────────────────────────────────────────────────');
    const vitalikAddress = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'; // Vitalik's address
    console.log(`Checking Vitalik Buterin's address: ${vitalikAddress}`);
    try {
        const info = await checker.getAddressInfo(vitalikAddress);
        if (info.success) {
            console.log('✓ Success!');
            console.log(`Balance: ${info.balance.eth} ETH`);
            console.log(`Type: ${info.type}`);
        } else {
            console.log(`✗ Error: ${info.error}`);
        }
    } catch (error) {
        console.log(`✗ Network Error: ${error.message}`);
        console.log('Note: This requires internet access and an Ethereum RPC endpoint');
    }
    console.log();

    console.log('═══════════════════════════════════════════════════════');
    console.log('  Examples Complete');
    console.log('═══════════════════════════════════════════════════════');
    console.log('\nTo use with your own RPC endpoint:');
    console.log('  await checker.getTrueValue("https://your-rpc-url.com");');
    console.log('\nTo check any address:');
    console.log('  await checker.getAddressInfo("0xYourAddressHere");');
}

// Run examples
if (require.main === module) {
    runExamples().catch(console.error);
}

module.exports = { runExamples };
