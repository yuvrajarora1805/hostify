#!/usr/bin/env python3
"""
Hostify CLI - Command-line interface for hosting applications via Cloudflare Tunnels.

This module provides a user-friendly CLI for the Hostify library, enabling users
to host static sites and existing servers directly from the command line.
"""

import argparse
import os
import sys
import signal
from pathlib import Path
from typing import Optional

from .host import Host
from . import __version__


class HostifyCLI:
    """Main CLI handler for Hostify commands."""
    
    def __init__(self):
        self.host: Optional[Host] = None
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print("\n\n[!] Received shutdown signal. Cleaning up...")
        if self.host:
            try:
                self.host.stop()
                print("[+] Cleanup completed successfully.")
            except Exception as e:
                print(f"[!] Error during cleanup: {e}")
        sys.exit(0)
    
    def _get_api_token(self) -> str:
        """Get Cloudflare API token from environment variable."""
        token = os.getenv("CLOUDFLARE_API_TOKEN")
        if not token:
            print("[!] Error: CLOUDFLARE_API_TOKEN environment variable not set.")
            print("\nPlease set your Cloudflare API token:")
            print("  Windows (PowerShell): $env:CLOUDFLARE_API_TOKEN='your-token-here'")
            print("  Windows (CMD):        set CLOUDFLARE_API_TOKEN=your-token-here")
            print("  Linux/macOS:          export CLOUDFLARE_API_TOKEN='your-token-here'")
            print("\nFor setup instructions, visit:")
            print("  https://github.com/yuvrajarora1805/hostify/blob/main/CLOUDFLARE_SETUP.md")
            sys.exit(1)
        return token
    
    def host_static(self, directory: str, domain: str):
        """
        Host a static site from a directory.
        
        Args:
            directory: Path to the directory containing static files
            domain: Domain name to host on (e.g., mysite.example.com)
        """
        # Validate directory
        dir_path = Path(directory).resolve()
        if not dir_path.exists():
            print(f"[!] Error: Directory '{directory}' does not exist.")
            sys.exit(1)
        
        if not dir_path.is_dir():
            print(f"[!] Error: '{directory}' is not a directory.")
            sys.exit(1)
        
        # Get API token
        api_token = self._get_api_token()
        
        # Start hosting
        print(f"\n[*] Starting static site hosting...")
        print(f"[*] Directory: {dir_path}")
        print(f"[*] Domain: {domain}")
        print(f"[*] Press Ctrl+C to stop hosting\n")
        
        try:
            self.host = Host(
                path=str(dir_path),
                domain=domain,
                api_token=api_token
            )
            self.host.serve()
            
            # serve() method will handle the rest
            
        except Exception as e:
            print(f"\n[!] Error: {e}")
            sys.exit(1)
    
    def host_port(self, port: int, domain: str):
        """
        Host an existing server running on a port.
        
        Args:
            port: Port number where the server is running
            domain: Domain name to host on (e.g., app.example.com)
        """
        # Validate port
        try:
            port_num = int(port)
            if not (1 <= port_num <= 65535):
                raise ValueError("Port must be between 1 and 65535")
        except ValueError as e:
            print(f"[!] Error: Invalid port number - {e}")
            sys.exit(1)
        
        # Get API token
        api_token = self._get_api_token()
        
        # Start hosting
        print(f"\n[*] Starting port-based hosting...")
        print(f"[*] Port: {port_num}")
        print(f"[*] Domain: {domain}")
        print(f"[*] Press Ctrl+C to stop hosting\n")
        
        try:
            self.host = Host(
                port=port_num,
                domain=domain,
                api_token=api_token
            )
            self.host.serve()
            
            # serve() method will handle the rest
            
        except Exception as e:
            print(f"\n[!] Error: {e}")
            sys.exit(1)
    
    def show_version(self):
        """Display version information."""
        print(f"Hostify v{__version__}")
        print("Effortless application hosting using Cloudflare Tunnels")
        print("\nRepository: https://github.com/yuvrajarora1805/hostify")
        print("Documentation: https://hostify.readthedocs.io")


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="hostify",
        description="Effortless application hosting using Cloudflare Tunnels",
        epilog="For more information, visit: https://github.com/yuvrajarora1805/hostify",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Static site hosting command
    static_parser = subparsers.add_parser(
        "static",
        help="Host a static site from a directory",
        description="Host static files (HTML, CSS, JS) from a directory via Cloudflare Tunnel"
    )
    static_parser.add_argument(
        "directory",
        help="Path to the directory containing static files"
    )
    static_parser.add_argument(
        "domain",
        help="Domain name to host on (e.g., mysite.example.com)"
    )
    
    # Port-based hosting command
    port_parser = subparsers.add_parser(
        "port",
        help="Host an existing server running on a port",
        description="Tunnel an existing server (Flask, Django, etc.) via Cloudflare"
    )
    port_parser.add_argument(
        "port",
        type=int,
        help="Port number where your server is running (1-65535)"
    )
    port_parser.add_argument(
        "domain",
        help="Domain name to host on (e.g., app.example.com)"
    )
    
    # Version command
    subparsers.add_parser(
        "version",
        help="Show version information"
    )
    
    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Initialize CLI handler
    cli = HostifyCLI()
    
    # Execute command
    try:
        if args.command == "static":
            cli.host_static(args.directory, args.domain)
        elif args.command == "port":
            cli.host_port(args.port, args.domain)
        elif args.command == "version":
            cli.show_version()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
