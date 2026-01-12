#!/bin/bash
# Test script for Hostify CLI on Linux/macOS

echo "============================================================"
echo "  Hostify CLI Test - Linux/macOS"
echo "============================================================"
echo ""

# Check if CLOUDFLARE_API_TOKEN is set
echo "[*] Checking environment..."
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "[!] CLOUDFLARE_API_TOKEN not set"
    echo ""
    echo "Please set your Cloudflare API token:"
    echo '  export CLOUDFLARE_API_TOKEN="your-token-here"'
    echo ""
    echo "Or load from existing environment if available"
    exit 1
fi

echo "[+] Environment configured"
echo ""

# Test 1: Version command
echo "Test 1: Version Command"
echo "Command: hostify version"
echo ""
hostify version
echo ""

# Test 2: Help command
echo "Test 2: Help Command"
echo "Command: hostify --help"
echo ""
hostify --help
echo ""

# Test 3: Static command help
echo "Test 3: Static Command Help"
echo "Command: hostify static --help"
echo ""
hostify static --help
echo ""

# Test 4: Port command help
echo "Test 4: Port Command Help"
echo "Command: hostify port --help"
echo ""
hostify port --help
echo ""

echo "============================================================"
echo "  All CLI tests completed!"
echo "============================================================"
echo ""
echo "To host the demo site, run:"
echo "  hostify static demo_site hostify-cli.yaspik.tech"
echo ""
