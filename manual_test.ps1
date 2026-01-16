# Hostify Manual Test Script
# This script helps you test Hostify with your Cloudflare token

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "  Hostify Manual Test Script" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check if token is set
$token = $env:CLOUDFLARE_API_TOKEN
if (-not $token) {
    Write-Host "❌ CLOUDFLARE_API_TOKEN not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your token first:" -ForegroundColor Yellow
    Write-Host '  $env:CLOUDFLARE_API_TOKEN="your_token_here"' -ForegroundColor White
    Write-Host ""
    Write-Host "Or set it permanently:" -ForegroundColor Yellow
    Write-Host '  setx CLOUDFLARE_API_TOKEN "your_token_here"' -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Token found: " -NoNewline -ForegroundColor Green
Write-Host $token.Substring(0, 10) + "..." -ForegroundColor Gray
Write-Host ""

# Test options
Write-Host "Choose a test:" -ForegroundColor Cyan
Write-Host "1. Test with demo site (./demo_site)" -ForegroundColor White
Write-Host "2. Test with custom directory" -ForegroundColor White
Write-Host "3. Test with existing server (port)" -ForegroundColor White
Write-Host "4. Test CLI version" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 Testing with demo site..." -ForegroundColor Green
        Write-Host ""
        $domain = Read-Host "Enter your domain (e.g., test.example.com)"
        
        Write-Host ""
        Write-Host "Running: python -c 'from hostify import Host; Host(domain=""$domain"", path=""./demo_site"").serve()'" -ForegroundColor Gray
        Write-Host ""
        
        python -c "from hostify import Host; Host(domain='$domain', path='./demo_site').serve()"
    }
    
    "2" {
        Write-Host ""
        Write-Host "🚀 Testing with custom directory..." -ForegroundColor Green
        Write-Host ""
        $domain = Read-Host "Enter your domain (e.g., test.example.com)"
        $path = Read-Host "Enter directory path (e.g., ./my_site)"
        
        Write-Host ""
        Write-Host "Running: python -c 'from hostify import Host; Host(domain=""$domain"", path=""$path"").serve()'" -ForegroundColor Gray
        Write-Host ""
        
        python -c "from hostify import Host; Host(domain='$domain', path='$path').serve()"
    }
    
    "3" {
        Write-Host ""
        Write-Host "🚀 Testing with existing server..." -ForegroundColor Green
        Write-Host ""
        $domain = Read-Host "Enter your domain (e.g., app.example.com)"
        $port = Read-Host "Enter port number (e.g., 3000)"
        
        Write-Host ""
        Write-Host "⚠️  Make sure your app is running on port $port first!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Running: python -c 'from hostify import Host; Host(domain=""$domain"", port=$port).serve()'" -ForegroundColor Gray
        Write-Host ""
        
        python -c "from hostify import Host; Host(domain='$domain', port=$port).serve()"
    }
    
    "4" {
        Write-Host ""
        Write-Host "🚀 Testing CLI..." -ForegroundColor Green
        Write-Host ""
        
        # Check CLI version
        Write-Host "Version:" -ForegroundColor Cyan
        hostify version
        Write-Host ""
        
        Write-Host "Choose CLI test:" -ForegroundColor Cyan
        Write-Host "1. hostify static" -ForegroundColor White
        Write-Host "2. hostify port" -ForegroundColor White
        Write-Host ""
        
        $cliChoice = Read-Host "Enter choice (1-2)"
        
        if ($cliChoice -eq "1") {
            $domain = Read-Host "Enter domain"
            $path = Read-Host "Enter path (default: .)"
            if (-not $path) { $path = "." }
            
            Write-Host ""
            Write-Host "Running: hostify static $path $domain" -ForegroundColor Gray
            Write-Host ""
            
            hostify static $path $domain
        }
        elseif ($cliChoice -eq "2") {
            $domain = Read-Host "Enter domain"
            $port = Read-Host "Enter port"
            
            Write-Host ""
            Write-Host "⚠️  Make sure your app is running on port $port first!" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Running: hostify port $port $domain" -ForegroundColor Gray
            Write-Host ""
            
            hostify port $port $domain
        }
    }
    
    default {
        Write-Host ""
        Write-Host "❌ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Test completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the tunnel" -ForegroundColor Yellow
