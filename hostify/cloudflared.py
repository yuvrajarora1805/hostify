"""
Cloudflared binary manager and tunnel runner.
"""

import os
import sys
import platform
import subprocess
import requests
import stat
from typing import Optional
from pathlib import Path


class CloudflaredError(Exception):
    """Custom exception for cloudflared errors."""
    pass


class Cloudflared:
    """
    Manager for cloudflared binary and tunnel processes.
    
    Handles:
    - OS detection
    - Binary download and caching
    - Tunnel process management
    - Log capture
    """
    
    # Cloudflared download URLs by platform
    DOWNLOAD_URLS = {
        "windows": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe",
        "linux": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
        "darwin": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64",
    }
    
    def __init__(self):
        """Initialize cloudflared manager."""
        self.process: Optional[subprocess.Popen] = None
        self._binary_path: Optional[str] = None
    
    def get_binary_path(self) -> str:
        """
        Get path to cloudflared binary, downloading if necessary.
        
        Returns:
            Path to cloudflared binary
        
        Raises:
            CloudflaredError: If download or setup fails
        """
        if self._binary_path and os.path.exists(self._binary_path):
            return self._binary_path
        
        # Determine cache directory
        cache_dir = os.path.expanduser("~/.hostify/bin")
        os.makedirs(cache_dir, exist_ok=True)
        
        # Determine binary name based on OS
        system = platform.system().lower()
        if system == "windows":
            binary_name = "cloudflared.exe"
        else:
            binary_name = "cloudflared"
        
        binary_path = os.path.join(cache_dir, binary_name)
        
        # Download if not exists
        if not os.path.exists(binary_path):
            print(f"Downloading cloudflared binary for {system}...")
            self._download_binary(binary_path)
            print(f"✓ Downloaded cloudflared to {binary_path}")
        
        self._binary_path = binary_path
        return binary_path
    
    def _download_binary(self, target_path: str) -> None:
        """
        Download cloudflared binary for current platform.
        
        Args:
            target_path: Path to save binary
        
        Raises:
            CloudflaredError: If download fails
        """
        system = platform.system().lower()
        
        if system not in self.DOWNLOAD_URLS:
            raise CloudflaredError(
                f"Unsupported platform: {system}. "
                f"Supported platforms: {', '.join(self.DOWNLOAD_URLS.keys())}"
            )
        
        url = self.DOWNLOAD_URLS[system]
        
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            # Download with progress
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\rDownloading: {progress:.1f}%", end='', flush=True)
            
            print()  # New line after progress
            
            # Make executable on Unix systems
            if system != "windows":
                st = os.stat(target_path)
                os.chmod(target_path, st.st_mode | stat.S_IEXEC)
        
        except requests.exceptions.RequestException as e:
            raise CloudflaredError(f"Failed to download cloudflared: {str(e)}")
        except Exception as e:
            raise CloudflaredError(f"Error setting up cloudflared: {str(e)}")
    
    def run_tunnel(
        self,
        tunnel_id: str,
        credentials_path: str,
        port: int,
        host: str = "localhost"
    ) -> subprocess.Popen:
        """
        Start cloudflared tunnel process.
        
        Args:
            tunnel_id: Tunnel ID
            credentials_path: Path to credentials JSON file
            port: Local port to tunnel
            host: Local host (default: localhost)
        
        Returns:
            Popen process object
        
        Raises:
            CloudflaredError: If tunnel fails to start
        """
        binary_path = self.get_binary_path()
        
        if not os.path.exists(credentials_path):
            raise CloudflaredError(f"Credentials file not found: {credentials_path}")
        
        # Build command
        cmd = [
            binary_path,
            "tunnel",
            "--credentials-file", credentials_path,
            "run",
            "--url", f"http://{host}:{port}",
            tunnel_id
        ]
        
        try:
            # Start process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            return self.process
        
        except Exception as e:
            raise CloudflaredError(f"Failed to start tunnel: {str(e)}")
    
    def stop_tunnel(self) -> None:
        """
        Stop the running tunnel process.
        """
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            
            self.process = None
    
    def is_running(self) -> bool:
        """
        Check if tunnel process is running.
        
        Returns:
            True if running, False otherwise
        """
        if not self.process:
            return False
        
        return self.process.poll() is None
    
    def get_logs(self, lines: int = 50) -> str:
        """
        Get recent log output from tunnel process.
        
        Args:
            lines: Number of lines to retrieve
        
        Returns:
            Log output string
        """
        if not self.process or not self.process.stdout:
            return ""
        
        # This is a simplified version - in production you'd want a proper log buffer
        try:
            output = []
            while len(output) < lines:
                line = self.process.stdout.readline()
                if not line:
                    break
                output.append(line)
            
            return "".join(output)
        except:
            return ""
