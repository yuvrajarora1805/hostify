"""
Test Cloudflare API Token
This script validates your Cloudflare API token
"""

import requests
import os
import sys

print("=" * 60)
print("  Cloudflare API Token Validator")
print("=" * 60)
print()

# Get token
token = os.getenv('CLOUDFLARE_API_TOKEN') or os.getenv('CF_API_TOKEN')

if not token:
    print("❌ No token found in environment variables!")
    print()
    print("Set it with:")
    print('  $env:CLOUDFLARE_API_TOKEN="your_token"')
    sys.exit(1)

print(f"✅ Token found: {token[:15]}...")
print()
print("Testing token with Cloudflare API...")
print()

# Test the token
try:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Verify token by getting user details
    response = requests.get(
        'https://api.cloudflare.com/client/v4/user/tokens/verify',
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Token is VALID!")
            print()
            print("Token Details:")
            result = data.get('result', {})
            print(f"  Status: {result.get('status', 'N/A')}")
            print(f"  ID: {result.get('id', 'N/A')}")
            print()
            
            # Get zones to verify permissions
            print("Checking permissions...")
            zones_response = requests.get(
                'https://api.cloudflare.com/client/v4/zones',
                headers=headers,
                timeout=10
            )
            
            if zones_response.status_code == 200:
                zones_data = zones_response.json()
                if zones_data.get('success'):
                    zones = zones_data.get('result', [])
                    print(f"✅ Can access {len(zones)} zone(s)")
                    if zones:
                        print()
                        print("Your domains:")
                        for zone in zones[:5]:  # Show first 5
                            print(f"  • {zone.get('name')}")
                    print()
                    print("🎉 Token is working correctly!")
                    print()
                    print("You can now use Hostify with this token.")
                else:
                    print("⚠️  Token valid but cannot list zones")
                    print("   Make sure token has 'Zone:Read' permission")
            else:
                print(f"⚠️  Cannot verify zone access: {zones_response.status_code}")
        else:
            print("❌ Token validation failed!")
            print(f"   Error: {data.get('errors', 'Unknown error')}")
    else:
        print(f"❌ Token is INVALID!")
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Network error: {e}")
    print()
    print("Please check your internet connection.")
except Exception as e:
    print(f"❌ Error: {e}")

print()
