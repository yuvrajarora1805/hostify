"""
Main Host class - the primary developer API for hostify.
"""

import os
import sys
import time
import signal
import atexit
from typing import Optional

from .cloudflare import Cloudflare, CloudflareAPIError
from .cloudflared import Cloudflared, CloudflaredError
from .utils import is_port_in_use, start_static_server, validate_server


class HostError(Exception):
    """Custom exception for Host errors."""
    pass


class Host:
    """
    Main class for hosting applications via Cloudflare Tunnels.
    
    Simple one-line API:
        Host(domain="app.example.com", port=3000).serve()
    
    Or with static files:
        Host(domain="app.example.com", path="./public").serve()
    """
    
    def __init__(
        self,
        domain: str,
        port: Optional[int] = None,
        path: Optional[str] = None,
        api_token: Optional[str] = None
    ):
        """
        Initialize Host instance.
        
        Args:
            domain: Full domain or subdomain (e.g., "app.example.com")
            port: Port of existing local server (mutually exclusive with path)
            path: Path to static files to serve (mutually exclusive with port)
            api_token: Cloudflare API token (optional, reads from CF_API_TOKEN env var)
        
        Raises:
            HostError: If configuration is invalid
        """
        # Validate inputs
        if not domain:
            raise HostError("Domain is required")
        
        if port is None and path is None:
            raise HostError("Either 'port' or 'path' must be specified")
        
        if port is not None and path is not None:
            raise HostError("Cannot specify both 'port' and 'path'")
        
        if port is not None and (port < 1 or port > 65535):
            raise HostError(f"Invalid port: {port}. Must be between 1 and 65535")
        
        if path is not None and not os.path.exists(path):
            raise HostError(f"Path does not exist: {path}")
        
        if path is not None and not os.path.isdir(path):
            raise HostError(f"Path is not a directory: {path}")
        
        self.domain = domain
        self.port = port
        self.path = path
        
        # Initialize components
        self.cf = Cloudflare(api_token)
        self.cloudflared = Cloudflared()
        
        # State tracking
        self.tunnel_id: Optional[str] = None
        self.dns_record_id: Optional[str] = None
        self.zone_id: Optional[str] = None
        self.credentials_path: Optional[str] = None
        self.static_server_process = None
        
        # Register cleanup handlers
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def serve(self) -> None:
        """
        Start hosting the application.
        
        This method:
        1. Validates the local server or starts static server
        2. Creates Cloudflare tunnel
        3. Creates DNS record
        4. Starts cloudflared process
        5. Monitors and keeps alive
        
        Raises:
            HostError: If setup fails
        """
        try:
            print(f"[HOSTIFY] Starting tunnel for {self.domain}")
            print("=" * 60)
            
            # Step 1: Setup local server
            self._setup_local_server()
            
            # Step 2: Create tunnel
            print(f"\n[+] Creating Cloudflare tunnel...")
            self._create_tunnel()
            
            # Step 3: Create DNS record
            print(f"[+] Setting up DNS for {self.domain}...")
            self._create_dns()
            
            # Step 4: Start tunnel
            print(f"[+] Starting tunnel connection...")
            self._start_tunnel()
            
            # Step 5: Wait for tunnel to be ready
            print(f"[+] Waiting for tunnel to connect...")
            time.sleep(5)  # Give tunnel time to establish
            
            # Success!
            print("\n" + "=" * 60)
            print(f"[SUCCESS] Your site is now live at:")
            print(f"   https://{self.domain}")
            print("=" * 60)
            print("\n[INFO] Press Ctrl+C to stop the tunnel and clean up\n")
            
            # Keep alive
            self._keep_alive()
        
        except KeyboardInterrupt:
            print("\n\n[STOP] Shutting down...")
            self.cleanup()
        except Exception as e:
            print(f"\n[ERROR] {str(e)}")
            self.cleanup()
            raise HostError(f"Failed to start hosting: {str(e)}")
    
    def _setup_local_server(self) -> None:
        """Setup or validate local server."""
        if self.path:
            # Start static file server
            # Find available port
            self.port = 8000
            while is_port_in_use(self.port):
                self.port += 1
            
            print(f"[+] Starting static file server on port {self.port}...")
            print(f"    Serving: {os.path.abspath(self.path)}")
            
            self.static_server_process = start_static_server(self.path, self.port)
            
            # Give server more time to start and retry validation
            max_retries = 5
            for i in range(max_retries):
                time.sleep(1)
                if validate_server(self.port):
                    break
            else:
                # Check if process is still running
                if self.static_server_process.poll() is not None:
                    # Process died, get error output
                    stderr = self.static_server_process.stderr.read() if self.static_server_process.stderr else ""
                    raise HostError(f"Static server failed to start: {stderr}")
            
            print(f"    [OK] Server running on http://localhost:{self.port}")
        
        else:
            # Validate existing server
            print(f"[+] Checking for server on port {self.port}...")
            
            if not validate_server(self.port):
                raise HostError(
                    f"No server found on port {self.port}. "
                    f"Make sure your application is running first."
                )
            
            print(f"    [OK] Server detected on http://localhost:{self.port}")
    
    def _create_tunnel(self) -> None:
        """Create Cloudflare tunnel."""
        try:
            # Generate unique tunnel name
            tunnel_name = f"hostify-{self.domain.replace('.', '-')}-{int(time.time())}"
            
            # Create tunnel
            self.tunnel_id, credentials = self.cf.create_tunnel(tunnel_name)
            
            # Save credentials
            self.credentials_path = self.cf.save_credentials(self.tunnel_id, credentials)
            
            print(f"    [OK] Tunnel created: {self.tunnel_id}")
            print(f"    [OK] Credentials saved: {self.credentials_path}")
            
            # Configure tunnel route
            print(f"    [+] Configuring tunnel route...")
            self.cf.configure_tunnel_route(
                self.tunnel_id,
                self.domain,
                f"http://localhost:{self.port}"
            )
            print(f"    [OK] Route configured for {self.domain}")
        
        except CloudflareAPIError as e:
            raise HostError(f"Failed to create tunnel: {str(e)}")
    
    def _create_dns(self) -> None:
        """Create DNS record."""
        try:
            # Get zone ID
            self.zone_id = self.cf.get_zone_id(self.domain)
            
            # Check for existing record
            existing = self.cf.find_existing_record(self.zone_id, self.domain)
            if existing:
                print(f"    [WARN] DNS record already exists for {self.domain}")
                print(f"    [INFO] Existing record will be used")
                self.dns_record_id = existing["id"]
            else:
                # Create new record
                self.dns_record_id = self.cf.create_dns_record(
                    self.zone_id,
                    self.domain,
                    self.tunnel_id
                )
                print(f"    [OK] DNS record created: {self.dns_record_id}")
        
        except CloudflareAPIError as e:
            raise HostError(f"Failed to create DNS record: {str(e)}")
    
    def _start_tunnel(self) -> None:
        """Start cloudflared tunnel process."""
        try:
            self.cloudflared.run_tunnel(
                self.tunnel_id,
                self.credentials_path,
                self.port
            )
            
            print(f"    [OK] Tunnel process started")
        
        except CloudflaredError as e:
            raise HostError(f"Failed to start tunnel: {str(e)}")
    
    def _keep_alive(self) -> None:
        """Keep the tunnel alive and monitor status."""
        try:
            while True:
                if not self.cloudflared.is_running():
                    print("[WARN] Tunnel process stopped unexpectedly")
                    print("[INFO] Attempting to restart...")
                    
                    self._start_tunnel()
                    time.sleep(5)
                    
                    if self.cloudflared.is_running():
                        print("[OK] Tunnel restarted successfully")
                    else:
                        raise HostError("Failed to restart tunnel")
                
                time.sleep(10)  # Check every 10 seconds
        
        except KeyboardInterrupt:
            raise  # Re-raise to be caught by serve()
    
    def cleanup(self) -> None:
        """
        Clean up all resources.
        
        This method:
        1. Stops cloudflared process
        2. Deletes DNS record
        3. Deletes tunnel
        4. Stops static server if running
        """
        print("\n[CLEANUP] Cleaning up resources...")
        
        # Stop cloudflared
        if self.cloudflared:
            try:
                self.cloudflared.stop_tunnel()
                print("    [OK] Stopped tunnel process")
            except Exception as e:
                print(f"    [WARN] Error stopping tunnel: {str(e)}")
        
        # Delete DNS record
        if self.dns_record_id and self.zone_id:
            try:
                # Only delete if we created it (not existing)
                self.cf.delete_dns_record(self.zone_id, self.dns_record_id)
                print("    [OK] Deleted DNS record")
            except Exception as e:
                print(f"    [WARN] Error deleting DNS record: {str(e)}")
        
        # Delete tunnel
        if self.tunnel_id:
            try:
                self.cf.delete_tunnel(self.tunnel_id)
                print("    [OK] Deleted tunnel")
            except Exception as e:
                print(f"    [WARN] Error deleting tunnel: {str(e)}")
        
        # Delete credentials file
        if self.credentials_path and os.path.exists(self.credentials_path):
            try:
                os.remove(self.credentials_path)
                print("    [OK] Deleted credentials file")
            except Exception as e:
                print(f"    [WARN] Error deleting credentials: {str(e)}")
        
        # Stop static server
        if self.static_server_process:
            try:
                self.static_server_process.terminate()
                self.static_server_process.wait(timeout=5)
                print("    [OK] Stopped static file server")
            except Exception as e:
                print(f"    [WARN] Error stopping static server: {str(e)}")
        
        print("\n[SUCCESS] Cleanup complete!\n")
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals."""
        raise KeyboardInterrupt
