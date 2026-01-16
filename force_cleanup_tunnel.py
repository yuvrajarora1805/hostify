"""
Force cleanup orphaned Cloudflare tunnels.

This script will:
1. List all tunnels
2. Delete the specified tunnel (even if it has errors)
3. Clean up associated DNS records
"""

import os
import sys
from hostify.cloudflare import Cloudflare, CloudflareAPIError

def force_delete_tunnel(tunnel_id: str):
    """
    Force delete a tunnel and its associated resources.
    
    Args:
        tunnel_id: The tunnel ID to delete
    """
    print(f"\n[FORCE CLEANUP] Starting cleanup for tunnel: {tunnel_id}")
    print("=" * 60)
    
    # Initialize Cloudflare client
    try:
        cf = Cloudflare()
        account_id = cf.get_account_id()
        print(f"[+] Connected to Cloudflare account: {account_id}")
    except CloudflareAPIError as e:
        print(f"[ERROR] Failed to connect to Cloudflare: {e}")
        return False
    
    # Step 1: List all tunnels to verify it exists
    print(f"\n[+] Checking if tunnel exists...")
    try:
        tunnels = cf.list_tunnels()
        tunnel_exists = any(t['id'] == tunnel_id for t in tunnels)
        
        if tunnel_exists:
            tunnel_info = next(t for t in tunnels if t['id'] == tunnel_id)
            print(f"    [OK] Found tunnel: {tunnel_info.get('name', 'Unknown')}")
            print(f"    Status: {tunnel_info.get('status', 'Unknown')}")
        else:
            print(f"    [WARN] Tunnel {tunnel_id} not found in account")
            print(f"    It may have been already deleted")
            return True
    except Exception as e:
        print(f"    [WARN] Error listing tunnels: {e}")
    
    # Step 2: Try to delete tunnel connections first
    print(f"\n[+] Attempting to clean up tunnel connections...")
    try:
        # Delete tunnel connections by sending DELETE to connections endpoint
        endpoint = f"/accounts/{account_id}/cfd_tunnel/{tunnel_id}/connections"
        try:
            cf._make_request("DELETE", endpoint)
            print(f"    [OK] Deleted tunnel connections")
        except CloudflareAPIError as e:
            # Connections might not exist, that's okay
            print(f"    [INFO] No active connections to delete")
    except Exception as e:
        print(f"    [WARN] Error cleaning connections: {e}")
    
    # Step 3: Find and delete associated DNS records
    print(f"\n[+] Searching for associated DNS records...")
    try:
        # Get all zones
        zones_response = cf._make_request("GET", "/zones")
        zones = zones_response if isinstance(zones_response, list) else [zones_response]
        
        deleted_records = 0
        for zone in zones:
            zone_id = zone['id']
            zone_name = zone['name']
            
            # List DNS records for this zone
            try:
                records = cf.list_dns_records(zone_id, record_type="CNAME")
                
                # Find records pointing to this tunnel
                tunnel_cname = f"{tunnel_id}.cfargotunnel.com"
                for record in records:
                    if record.get('content') == tunnel_cname:
                        try:
                            cf.delete_dns_record(zone_id, record['id'])
                            print(f"    [OK] Deleted DNS record: {record['name']} (zone: {zone_name})")
                            deleted_records += 1
                        except Exception as e:
                            print(f"    [WARN] Failed to delete DNS record {record['name']}: {e}")
            except Exception as e:
                # Skip zones we can't access
                pass
        
        if deleted_records == 0:
            print(f"    [INFO] No DNS records found pointing to this tunnel")
    except Exception as e:
        print(f"    [WARN] Error searching for DNS records: {e}")
    
    # Step 4: Force delete the tunnel
    print(f"\n[+] Force deleting tunnel...")
    try:
        # Try with force parameter
        endpoint = f"/accounts/{account_id}/cfd_tunnel/{tunnel_id}"
        cf._make_request("DELETE", endpoint)
        print(f"    [OK] Successfully deleted tunnel!")
        
        # Verify deletion
        tunnels = cf.list_tunnels()
        if not any(t['id'] == tunnel_id for t in tunnels):
            print(f"    [OK] Verified: Tunnel no longer exists")
            return True
        else:
            print(f"    [WARN] Tunnel still appears in list")
            return False
            
    except CloudflareAPIError as e:
        error_msg = str(e)
        
        # Check if it's already deleted
        if "not found" in error_msg.lower() or "404" in error_msg:
            print(f"    [OK] Tunnel already deleted")
            return True
        
        # Check if it's a 400 error about active connections
        if "400" in error_msg or "active connections" in error_msg.lower():
            print(f"    [ERROR] Tunnel still has active connections")
            print(f"    [INFO] This usually means cloudflared is still running somewhere")
            print(f"    [INFO] Please ensure all cloudflared processes are stopped")
            print(f"\n    Error details: {error_msg}")
            return False
        
        print(f"    [ERROR] Failed to delete tunnel: {error_msg}")
        return False
    except Exception as e:
        print(f"    [ERROR] Unexpected error: {e}")
        return False


def main():
    """Main entry point."""
    # The tunnel ID from the user's report
    tunnel_id = "c9187679-cc9e-412c-aa56-c05025f8fec6"
    
    print("\n" + "=" * 60)
    print("HOSTIFY - Force Tunnel Cleanup Utility")
    print("=" * 60)
    print(f"\nTarget Tunnel ID: {tunnel_id}")
    
    # Check for API token - accept from args, env, or prompt
    api_token = None
    
    # Try command line argument first
    if len(sys.argv) > 1:
        api_token = sys.argv[1]
        print("\n[+] Using API token from command line argument")
    
    # Try environment variable (check both common names)
    elif os.getenv("CF_API_TOKEN"):
        api_token = os.getenv("CF_API_TOKEN")
        print("\n[+] Using API token from CF_API_TOKEN environment variable")
    
    elif os.getenv("CLOUDFLARE_API_TOKEN"):
        api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        print("\n[+] Using API token from CLOUDFLARE_API_TOKEN environment variable")
    
    # Prompt user
    else:
        print("\n[!] CF_API_TOKEN not found in environment")
        print("\nPlease enter your Cloudflare API token:")
        print("(You can get this from: https://dash.cloudflare.com/profile/api-tokens)")
        api_token = input("\nAPI Token: ").strip()
        
        if not api_token:
            print("\n[ERROR] No API token provided")
            sys.exit(1)
    
    # Set it in environment for the Cloudflare class to use
    os.environ["CF_API_TOKEN"] = api_token
    
    # Run cleanup
    success = force_delete_tunnel(tunnel_id)
    
    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] Cleanup completed successfully!")
        print("\nThe tunnel has been removed from your Cloudflare account.")
    else:
        print("[FAILED] Cleanup encountered errors")
        print("\nPlease check the errors above and try again.")
        print("\nIf the tunnel still shows in your dashboard:")
        print("1. Ensure no cloudflared processes are running")
        print("2. Wait a few minutes for Cloudflare to sync")
        print("3. Try deleting manually from the dashboard")
    print("=" * 60 + "\n")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
