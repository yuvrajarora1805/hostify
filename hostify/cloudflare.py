"""
Cloudflare API wrapper for tunnel and DNS management.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Tuple


class CloudflareAPIError(Exception):
    """Custom exception for Cloudflare API errors."""
    pass


class Cloudflare:
    """
    Cloudflare API client for managing tunnels and DNS records.
    
    Requires CF_API_TOKEN environment variable with permissions:
    - Account → Cloudflare Tunnel → Edit
    - Zone → DNS → Edit
    - Zone → Read
    """
    
    BASE_URL = "https://api.cloudflare.com/client/v4"
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize Cloudflare API client.
        
        Args:
            api_token: Cloudflare API token. If None, reads from CF_API_TOKEN env var.
        
        Raises:
            CloudflareAPIError: If API token is not provided.
        """
        self.api_token = api_token or os.getenv("CF_API_TOKEN")
        if not self.api_token:
            raise CloudflareAPIError(
                "Cloudflare API token not found. Set CF_API_TOKEN environment variable "
                "or pass api_token parameter."
            )
        
        # Cache for account and zone IDs
        self._account_id = None
        self._zone_cache = {}
    
    def get_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary with Authorization header.
        """
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make HTTP request to Cloudflare API.
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
        
        Returns:
            JSON response data
        
        Raises:
            CloudflareAPIError: If request fails
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        kwargs.setdefault("headers", self.get_headers())
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success", False):
                errors = data.get("errors", [])
                error_msg = "; ".join([e.get("message", str(e)) for e in errors])
                raise CloudflareAPIError(f"API request failed: {error_msg}")
            
            return data.get("result", data)
        
        except requests.exceptions.RequestException as e:
            raise CloudflareAPIError(f"Request failed: {str(e)}")
    
    def get_accounts(self) -> List[Dict]:
        """
        Get all Cloudflare accounts.
        
        Returns:
            List of account dictionaries.
        """
        return self._make_request("GET", "/accounts")
    
    def get_account_id(self) -> str:
        """
        Get the first available account ID.
        
        Returns:
            Account ID string.
        
        Raises:
            CloudflareAPIError: If no accounts found.
        """
        if self._account_id:
            return self._account_id
        
        accounts = self.get_accounts()
        if not accounts:
            raise CloudflareAPIError("No Cloudflare accounts found for this API token.")
        
        self._account_id = accounts[0]["id"]
        return self._account_id
    
    def get_zone_id(self, domain: str) -> str:
        """
        Get zone ID for a domain.
        
        Args:
            domain: Domain name (e.g., "example.com")
        
        Returns:
            Zone ID string.
        
        Raises:
            CloudflareAPIError: If zone not found.
        """
        # Check cache first
        if domain in self._zone_cache:
            return self._zone_cache[domain]
        
        # Extract root domain (handle subdomains)
        parts = domain.split(".")
        if len(parts) > 2:
            # Try with last two parts first (e.g., example.com from app.example.com)
            root_domain = ".".join(parts[-2:])
        else:
            root_domain = domain
        
        # Search for zone
        zones = self._make_request("GET", "/zones", params={"name": root_domain})
        
        if not zones:
            raise CloudflareAPIError(
                f"Zone not found for domain '{domain}'. "
                f"Make sure '{root_domain}' is added to your Cloudflare account."
            )
        
        zone_id = zones[0]["id"]
        self._zone_cache[domain] = zone_id
        self._zone_cache[root_domain] = zone_id
        
        return zone_id
    
    def list_dns_records(self, zone_id: str, record_type: Optional[str] = None) -> List[Dict]:
        """
        List DNS records for a zone.
        
        Args:
            zone_id: Zone ID
            record_type: Optional filter by record type (A, CNAME, etc.)
        
        Returns:
            List of DNS record dictionaries.
        """
        params = {}
        if record_type:
            params["type"] = record_type
        
        return self._make_request("GET", f"/zones/{zone_id}/dns_records", params=params)
    
    def create_tunnel(self, name: str) -> Tuple[str, Dict]:
        """
        Create a new Cloudflare Tunnel.
        
        Args:
            name: Tunnel name
        
        Returns:
            Tuple of (tunnel_id, credentials_dict)
        """
        account_id = self.get_account_id()
        
        data = {"name": name, "tunnel_secret": self._generate_tunnel_secret()}
        result = self._make_request(
            "POST",
            f"/accounts/{account_id}/cfd_tunnel",
            json=data
        )
        
        tunnel_id = result["id"]
        credentials = {
            "AccountTag": account_id,
            "TunnelSecret": data["tunnel_secret"],
            "TunnelID": tunnel_id
        }
        
        return tunnel_id, credentials
    
    def delete_tunnel(self, tunnel_id: str) -> None:
        """
        Delete a Cloudflare Tunnel.
        
        Args:
            tunnel_id: Tunnel ID to delete
        """
        account_id = self.get_account_id()
        self._make_request("DELETE", f"/accounts/{account_id}/cfd_tunnel/{tunnel_id}")
    
    def list_tunnels(self) -> List[Dict]:
        """
        List all tunnels for the account.
        
        Returns:
            List of tunnel dictionaries.
        """
        account_id = self.get_account_id()
        return self._make_request("GET", f"/accounts/{account_id}/cfd_tunnel")
    
    def configure_tunnel_route(self, tunnel_id: str, hostname: str, service: str) -> Dict:
        """
        Configure a route for a tunnel (public hostname).
        
        Args:
            tunnel_id: Tunnel ID
            hostname: Hostname to route (e.g., "app.example.com")
            service: Service URL (e.g., "http://localhost:8000")
        
        Returns:
            Route configuration dict
        """
        account_id = self.get_account_id()
        
        data = {
            "config": {
                "ingress": [
                    {
                        "hostname": hostname,
                        "service": service
                    },
                    {
                        "service": "http_status:404"
                    }
                ]
            }
        }
        
        result = self._make_request(
            "PUT",
            f"/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations",
            json=data
        )
        
        return result
    
    def create_dns_record(self, zone_id: str, subdomain: str, tunnel_id: str) -> str:
        """
        Create a CNAME DNS record pointing to a tunnel.
        
        Args:
            zone_id: Zone ID
            subdomain: Full subdomain (e.g., "app.example.com")
            tunnel_id: Tunnel ID
        
        Returns:
            DNS record ID
        """
        data = {
            "type": "CNAME",
            "name": subdomain,
            "content": f"{tunnel_id}.cfargotunnel.com",
            "ttl": 1,  # Auto
            "proxied": True
        }
        
        result = self._make_request("POST", f"/zones/{zone_id}/dns_records", json=data)
        return result["id"]
    
    def delete_dns_record(self, zone_id: str, record_id: str) -> None:
        """
        Delete a DNS record.
        
        Args:
            zone_id: Zone ID
            record_id: DNS record ID
        """
        self._make_request("DELETE", f"/zones/{zone_id}/dns_records/{record_id}")
    
    def find_existing_record(self, zone_id: str, subdomain: str) -> Optional[Dict]:
        """
        Find existing DNS record for a subdomain.
        
        Args:
            zone_id: Zone ID
            subdomain: Subdomain to search for
        
        Returns:
            DNS record dict if found, None otherwise
        """
        records = self.list_dns_records(zone_id)
        for record in records:
            if record["name"] == subdomain:
                return record
        return None
    
    def save_credentials(self, tunnel_id: str, credentials: Dict) -> str:
        """
        Save tunnel credentials to local file.
        
        Args:
            tunnel_id: Tunnel ID
            credentials: Credentials dictionary
        
        Returns:
            Path to saved credentials file
        """
        # Create credentials directory
        creds_dir = os.path.expanduser("~/.hostify/tunnels")
        os.makedirs(creds_dir, exist_ok=True)
        
        # Save credentials
        creds_path = os.path.join(creds_dir, f"{tunnel_id}.json")
        with open(creds_path, "w") as f:
            json.dump(credentials, f, indent=2)
        
        return creds_path
    
    def _generate_tunnel_secret(self) -> str:
        """
        Generate a random tunnel secret.
        
        Returns:
            Base64-encoded secret string
        """
        import base64
        import secrets
        
        # Generate 32 random bytes
        secret_bytes = secrets.token_bytes(32)
        return base64.b64encode(secret_bytes).decode("utf-8")
