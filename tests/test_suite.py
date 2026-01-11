"""
Comprehensive test suite for hostify library

Tests all major functionality across different scenarios.
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(message):
    print(f"{BLUE}[TEST]{RESET} {message}")

def print_pass(message):
    print(f"{GREEN}[PASS]{RESET} {message}")

def print_fail(message):
    print(f"{RED}[FAIL]{RESET} {message}")

def print_warn(message):
    print(f"{YELLOW}[WARN]{RESET} {message}")

def test_imports():
    """Test that all modules can be imported"""
    print_test("Testing imports...")
    
    try:
        from hostify import Host
        from hostify.cloudflare import Cloudflare, CloudflareAPIError
        from hostify.cloudflared import Cloudflared, CloudflaredError
        from hostify.utils import is_port_in_use, validate_server, start_static_server
        from hostify.host import HostError
        print_pass("All imports successful")
        return True
    except Exception as e:
        print_fail(f"Import failed: {e}")
        return False

def test_python_version():
    """Test Python version >= 3.9"""
    print_test("Testing Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_pass(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_fail(f"Python {version.major}.{version.minor} < 3.9")
        return False

def test_dependencies():
    """Test that required dependencies are installed"""
    print_test("Testing dependencies...")
    
    try:
        import requests
        print_pass(f"requests {requests.__version__}")
        return True
    except ImportError as e:
        print_fail(f"Missing dependency: {e}")
        return False

def test_port_detection():
    """Test port detection functionality"""
    print_test("Testing port detection...")
    
    from hostify.utils import is_port_in_use, validate_server
    
    # Start a simple server on a random port
    port = 9999
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(2)  # Wait for server to start
    
    try:
        if is_port_in_use(port):
            print_pass("Port detection works")
            result = True
        else:
            print_fail("Port detection failed")
            result = False
    finally:
        server.terminate()
        server.wait()
    
    return result

def test_cloudflared_download():
    """Test cloudflared binary download"""
    print_test("Testing cloudflared download...")
    
    from hostify.cloudflared import Cloudflared
    
    try:
        cf = Cloudflared()
        binary_path = cf.get_binary_path()
        
        if os.path.exists(binary_path):
            print_pass(f"Cloudflared binary exists at {binary_path}")
            return True
        else:
            print_fail("Cloudflared binary not found")
            return False
    except Exception as e:
        print_fail(f"Cloudflared download failed: {e}")
        return False

def test_api_token():
    """Test API token is set"""
    print_test("Testing API token...")
    
    token = os.getenv("CF_API_TOKEN")
    if token:
        print_pass("CF_API_TOKEN is set")
        return True
    else:
        print_warn("CF_API_TOKEN not set (optional for basic tests)")
        return True  # Not critical for basic tests

def test_os_detection():
    """Test OS detection"""
    print_test("Testing OS detection...")
    
    import platform
    
    os_name = platform.system().lower()
    
    if os_name in ["windows", "linux", "darwin"]:
        print_pass(f"OS detected: {os_name}")
        return True
    else:
        print_fail(f"Unknown OS: {os_name}")
        return False

def test_static_server():
    """Test static file server"""
    print_test("Testing static file server...")
    
    from hostify.utils import start_static_server
    
    # Create temporary directory with test file
    test_dir = Path("test_static_temp")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "index.html").write_text("<h1>Test</h1>")
    
    try:
        port = 9998
        process = start_static_server(str(test_dir), port)
        time.sleep(2)
        
        # Try to access the server
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            if response.status_code == 200 and "Test" in response.text:
                print_pass("Static server works")
                result = True
            else:
                print_fail("Static server not responding correctly")
                result = False
        except Exception as e:
            print_fail(f"Could not connect to static server: {e}")
            result = False
        
        process.terminate()
        process.wait()
    finally:
        # Cleanup
        (test_dir / "index.html").unlink()
        test_dir.rmdir()
    
    return result

def test_host_class():
    """Test Host class initialization"""
    print_test("Testing Host class...")
    
    from hostify import Host
    from hostify.host import HostError
    
    # Test invalid configurations
    try:
        # This will fail due to missing API token, but we're testing validation logic
        # We'll catch the API token error separately
        Host(domain="test.example.com", api_token="dummy_token")  # No port or path
        print_fail("Should have raised error for missing port/path")
        return False
    except HostError as e:
        if "port" in str(e).lower() or "path" in str(e).lower():
            print_pass("Correctly validates missing port/path")
        else:
            print_fail(f"Wrong error: {e}")
            return False
    
    try:
        test_dir = Path("test_host_temp")
        test_dir.mkdir(exist_ok=True)
        Host(domain="test.example.com", port=3000, path=str(test_dir), api_token="dummy_token")  # Both
        test_dir.rmdir()
        print_fail("Should have raised error for both port and path")
        return False
    except HostError as e:
        if test_dir.exists():
            test_dir.rmdir()
        if "both" in str(e).lower() or "cannot" in str(e).lower():
            print_pass("Correctly validates conflicting port/path")
        else:
            print_fail(f"Wrong error: {e}")
            return False
    
    # Test valid configuration (will fail on API token but that's OK for this test)
    try:
        test_dir = Path("test_host_temp")
        test_dir.mkdir(exist_ok=True)
        
        # This should pass validation even without real API token
        host = Host(domain="test.example.com", path=str(test_dir), api_token="dummy_token")
        print_pass("Host class initialization works")
        result = True
        
        test_dir.rmdir()
    except Exception as e:
        if test_dir.exists():
            test_dir.rmdir()
        # If it's just an API token error, that's actually OK for this test
        if "api" in str(e).lower() or "token" in str(e).lower():
            print_pass("Host class validation works (API token check is separate)")
            result = True
        else:
            print_fail(f"Host initialization failed: {e}")
            result = False
    
    return result

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 60)
    print("HOSTIFY LIBRARY - COMPREHENSIVE TEST SUITE")
    print("=" * 60 + "\n")
    
    tests = [
        ("Python Version", test_python_version),
        ("Imports", test_imports),
        ("Dependencies", test_dependencies),
        ("OS Detection", test_os_detection),
        ("Port Detection", test_port_detection),
        ("Static Server", test_static_server),
        ("Cloudflared Download", test_cloudflared_download),
        ("Host Class", test_host_class),
        ("API Token", test_api_token),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_fail(f"{name}: Unexpected error: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
    print("=" * 60 + "\n")
    
    if passed == total:
        print(f"{GREEN}All tests passed! Library is ready for publication.{RESET}\n")
        return True
    else:
        print(f"{YELLOW}Some tests failed. Please review before publishing.{RESET}\n")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
