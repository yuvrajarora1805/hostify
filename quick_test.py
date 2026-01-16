"""
Quick Manual Test Script for Hostify
Run this to quickly test if Hostify is working
"""

from hostify import Host
import os

print("=" * 60)
print("  Hostify Quick Test")
print("=" * 60)
print()

# Check for API token
token = os.getenv('CLOUDFLARE_API_TOKEN') or os.getenv('CF_API_TOKEN')

if not token:
    print("❌ No Cloudflare API token found!")
    print()
    print("Please set your token first:")
    print("  Windows: $env:CLOUDFLARE_API_TOKEN=\"your_token_here\"")
    print("  Linux/Mac: export CLOUDFLARE_API_TOKEN=\"your_token_here\"")
    print()
    exit(1)

print(f"✅ Token found: {token[:10]}...")
print()

# Get domain from user
domain = input("Enter your domain (e.g., test.example.com): ").strip()

if not domain:
    print("❌ Domain is required!")
    exit(1)

print()
print("Choose test mode:")
print("1. Static site (./demo_site)")
print("2. Custom directory")
print("3. Existing server (port)")
print()

choice = input("Enter choice (1-3): ").strip()

try:
    if choice == "1":
        print()
        print(f"🚀 Hosting demo site at {domain}...")
        print()
        Host(domain=domain, path="./demo_site").serve()
        
    elif choice == "2":
        path = input("Enter directory path: ").strip()
        print()
        print(f"🚀 Hosting {path} at {domain}...")
        print()
        Host(domain=domain, path=path).serve()
        
    elif choice == "3":
        port = int(input("Enter port number: ").strip())
        print()
        print(f"⚠️  Make sure your app is running on port {port}!")
        print()
        print(f"🚀 Connecting to localhost:{port} at {domain}...")
        print()
        Host(domain=domain, port=port).serve()
        
    else:
        print("❌ Invalid choice!")
        exit(1)
        
except KeyboardInterrupt:
    print()
    print("✅ Stopped by user")
except Exception as e:
    print()
    print(f"❌ Error: {e}")
    exit(1)
