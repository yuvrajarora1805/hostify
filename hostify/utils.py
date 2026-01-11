"""
Utility functions for hostify.
"""

import socket
import subprocess
import sys
from typing import Optional


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """
    Check if a port is in use by trying to connect to it.
    
    Args:
        port: Port number to check
        host: Host to check (default: localhost)
    
    Returns:
        True if port is in use (server is listening), False otherwise
    """
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0  # 0 means connection successful (port is in use)
    except:
        return False


def validate_server(port: int, host: str = "127.0.0.1") -> bool:
    """
    Validate that a server is running on the specified port.
    
    Args:
        port: Port number to check
        host: Host to check (default: localhost)
    
    Returns:
        True if server is accessible, False otherwise
    """
    return is_port_in_use(port, host)


def start_static_server(path: str, port: int) -> subprocess.Popen:
    """
    Start a simple HTTP server for static files.
    
    Args:
        path: Path to directory to serve
        port: Port to serve on
    
    Returns:
        Popen process object
    """
    import os
    
    if not os.path.isdir(path):
        raise ValueError(f"Path '{path}' is not a directory")
    
    # Use Python's built-in HTTP server
    cmd = [
        sys.executable,
        "-m",
        "http.server",
        str(port),
        "--directory",
        path
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process


def get_home_dir() -> str:
    """
    Get user's home directory.
    
    Returns:
        Path to home directory
    """
    import os
    return os.path.expanduser("~")


def ensure_dir(path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
    """
    import os
    os.makedirs(path, exist_ok=True)
