#!/usr/bin/env pwsh
# Test script for Hostify CLI on Windows

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  Hostify CLI Test - Windows" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Check if CLOUDFLARE_API_TOKEN is set
Write-Host "[*] Checking environment..." -ForegroundColor Yellow
if (-not $env:CLOUDFLARE_API_TOKEN) {
    Write-Host "[!] CLOUDFLARE_API_TOKEN not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your Cloudflare API token:" -ForegroundColor Yellow
    Write-Host '  $env:CLOUDFLARE_API_TOKEN="your-token-here"' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or load from existing environment if available" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Environment configured" -ForegroundColor Green
Write-Host ""

# Test 1: Version command
Write-Host "Test 1: Version Command" -ForegroundColor Cyan
Write-Host "Command: hostify version" -ForegroundColor Gray
Write-Host ""
hostify version
Write-Host ""

# Test 2: Help command
Write-Host "Test 2: Help Command" -ForegroundColor Cyan
Write-Host "Command: hostify --help" -ForegroundColor Gray
Write-Host ""
hostify --help
Write-Host ""

# Test 3: Static command help
Write-Host "Test 3: Static Command Help" -ForegroundColor Cyan
Write-Host "Command: hostify static --help" -ForegroundColor Gray
Write-Host ""
hostify static --help
Write-Host ""

# Test 4: Port command help
Write-Host "Test 4: Port Command Help" -ForegroundColor Cyan
Write-Host "Command: hostify port --help" -ForegroundColor Gray
Write-Host ""
hostify port --help
Write-Host ""

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  All CLI tests completed!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
Write-Host "To host the demo site, run:" -ForegroundColor Yellow
Write-Host '  hostify static demo_site hostify-cli.yaspik.tech' -ForegroundColor Cyan
Write-Host ""
