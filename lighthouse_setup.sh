#!/bin/bash
# Quick Start Script for Lighthouse Auto Scanner
# This script sets up and demonstrates the lighthouse_auto.py tool

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║        Lighthouse Auto Scanner - Quick Start Setup                ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "[1/4] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3.7 or higher."
    exit 1
fi

# Install Python dependencies
echo ""
echo "[2/4] Installing Python dependencies..."
pip3 install --user requests beautifulsoup4 lxml || {
    echo "✗ Failed to install Python dependencies"
    exit 1
}
echo "✓ Python dependencies installed"

# Check Node.js and npm (optional for Lighthouse)
echo ""
echo "[3/4] Checking for Node.js and npm (optional, for Lighthouse)..."
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    NODE_VERSION=$(node --version)
    NPM_VERSION=$(npm --version)
    echo "✓ Found: Node.js $NODE_VERSION, npm $NPM_VERSION"
    
    # Ask if user wants to install Lighthouse
    echo ""
    read -p "Install Google Lighthouse? (y/n) [y]: " INSTALL_LIGHTHOUSE
    INSTALL_LIGHTHOUSE=${INSTALL_LIGHTHOUSE:-y}
    
    if [[ "$INSTALL_LIGHTHOUSE" =~ ^[Yy]$ ]]; then
        echo "Installing Lighthouse globally..."
        npm install -g lighthouse || {
            echo "⚠ Failed to install Lighthouse globally. You can still use the script without it."
        }
        echo "✓ Lighthouse installed"
    else
        echo "⚠ Skipping Lighthouse installation. Use --no-lighthouse flag when running scans."
    fi
else
    echo "⚠ Node.js/npm not found. Lighthouse features will not be available."
    echo "  You can still use the script with --no-lighthouse flag."
fi

# Run test demo
echo ""
echo "[4/4] Running test demo..."
python3 lighthouse_test_demo.py

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║        Setup Complete! Ready to scan.                              ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Quick Start Examples:"
echo ""
echo "  # Scan a website (with Lighthouse)"
echo "  python3 lighthouse_auto.py https://example.com"
echo ""
echo "  # Fast scan without Lighthouse"
echo "  python3 lighthouse_auto.py https://example.com --no-lighthouse"
echo ""
echo "  # Deep scan with custom output"
echo "  python3 lighthouse_auto.py https://example.com --depth 3 --output ./reports"
echo ""
echo "For full documentation, see: LIGHTHOUSE_README.md"
echo ""
