"""
Test script for hostify examples.

This script tests both:
1. Static file hosting
2. Existing server hosting

Usage:
    python test_examples.py
"""

import os
import sys
import time
import tempfile
import subprocess
from pathlib import Path


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_static_hosting():
    """Test static file hosting example."""
    print_section("TEST 1: Static File Hosting")
    
    # Create temporary directory with test files
    test_dir = tempfile.mkdtemp(prefix="hostify_test_")
    print(f"[+] Created test directory: {test_dir}")
    
    # Create test HTML file
    index_path = os.path.join(test_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Hostify Test - Static Site</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        h1 { margin-top: 0; }
        .status { 
            background: #4CAF50;
            padding: 10px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hostify Static Site Test</h1>
        <div class="status">[OK] Static file hosting is working!</div>
        <p>This page is being served by hostify's static file server.</p>
        <p><strong>Test Time:</strong> """ + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
</body>
</html>
        """)
    
    print(f"[+] Created test HTML file: {index_path}")
    
    # Create test script
    test_script = f"""
from hostify import Host

print("Starting static file hosting test...")
print("Directory: {test_dir}")

# IMPORTANT: Replace with your actual domain!
# For testing, you can use a subdomain like: test-static.yourdomain.com

Host(
    domain="test-static.example.com",  # WARNING: CHANGE THIS TO YOUR DOMAIN
    path="{test_dir}"
).serve()
"""
    
    script_path = os.path.join(test_dir, "run_static_test.py")
    with open(script_path, "w") as f:
        f.write(test_script)
    
    print(f"[+] Created test script: {script_path}")
    print("\n" + "!" * 60)
    print("IMPORTANT: To run this test, you need to:")
    print("1. Edit the script and change 'test-static.example.com' to your actual domain")
    print("2. Make sure CF_API_TOKEN environment variable is set")
    print("3. Run: python " + script_path)
    print("!" * 60 + "\n")
    
    return test_dir, script_path


def test_existing_server():
    """Test existing server hosting example."""
    print_section("TEST 2: Existing Server Hosting")
    
    # Create a simple Flask app for testing
    test_dir = tempfile.mkdtemp(prefix="hostify_server_test_")
    print(f"[+] Created test directory: {test_dir}")
    
    # Create Flask test app
    flask_app = """
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Hostify Test - Flask Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        h1 { margin-top: 0; }
        .status { 
            background: #4CAF50;
            padding: 10px;
            border-radius: 5px;
            margin: 20px 0;
        }
        button {
            background: white;
            color: #f5576c;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hostify Flask Server Test</h1>
        <div class="status">[OK] Flask server is working!</div>
        <p>This is a Flask application hosted via hostify.</p>
        <p><strong>Server Time:</strong> ''' + time.strftime("%Y-%m-%d %H:%M:%S") + '''</p>
        <button onclick="testAPI()">Test API Endpoint</button>
        <div id="result"></div>
    </div>
    
    <script>
        async function testAPI() {
            const response = await fetch('/api/status');
            const data = await response.json();
            document.getElementById('result').innerHTML = 
                '<div class="status" style="margin-top: 20px;">API Response: ' + 
                JSON.stringify(data, null, 2) + '</div>';
        }
    </script>
</body>
</html>
    '''

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'message': 'Flask + Hostify works great!',
        'timestamp': time.time()
    })

if __name__ == '__main__':
    print("Starting Flask test server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
"""
    
    flask_path = os.path.join(test_dir, "flask_test_app.py")
    with open(flask_path, "w") as f:
        f.write(flask_app)
    
    print(f"[+] Created Flask test app: {flask_path}")
    
    # Create hostify script for Flask app
    hostify_script = """
from hostify import Host

print("Starting Flask server hosting test...")

# IMPORTANT: Make sure flask_test_app.py is running first!
# Run in another terminal: python flask_test_app.py

# Replace with your actual domain!
Host(
    domain="test-flask.example.com",  # WARNING: CHANGE THIS TO YOUR DOMAIN
    port=5000
).serve()
"""
    
    hostify_path = os.path.join(test_dir, "run_flask_test.py")
    with open(hostify_path, "w") as f:
        f.write(hostify_script)
    
    print(f"[+] Created hostify script: {hostify_path}")
    
    print("\n" + "!" * 60)
    print("IMPORTANT: To run this test, you need to:")
    print("1. Install Flask: pip install flask")
    print("2. Terminal 1 - Start Flask: python " + flask_path)
    print("3. Terminal 2 - Edit domain in: " + hostify_path)
    print("4. Terminal 2 - Run hostify: python " + hostify_path)
    print("!" * 60 + "\n")
    
    return test_dir, flask_path, hostify_path


def verify_environment():
    """Verify that the environment is set up correctly."""
    print_section("Environment Verification")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        print("[X] Python 3.9+ required!")
        return False
    else:
        print("[OK] Python version OK")
    
    # Check if hostify is importable
    try:
        import hostify
        print(f"[OK] Hostify library found (version {hostify.__version__})")
    except ImportError:
        print("[X] Hostify library not found!")
        print("    Install with: pip install -e .")
        return False
    
    # Check for CF_API_TOKEN
    cf_token = os.getenv("CF_API_TOKEN")
    if cf_token:
        print(f"[OK] CF_API_TOKEN is set ({len(cf_token)} characters)")
    else:
        print("[!] CF_API_TOKEN not set (required for actual hosting)")
        print("    Set with: $env:CF_API_TOKEN='your_token_here'")
    
    # Check for requests library
    try:
        import requests
        print("[OK] Requests library installed")
    except ImportError:
        print("[X] Requests library not found!")
        print("    Install with: pip install requests")
        return False
    
    return True


def main():
    """Main test function."""
    print("\n" + "=" * 60)
    print("  HOSTIFY EXAMPLES TEST SUITE")
    print("=" * 60)
    
    # Verify environment
    if not verify_environment():
        print("\n[X] Environment verification failed!")
        print("Please fix the issues above and try again.")
        return
    
    print("\n[OK] Environment verification passed!")
    
    # Test 1: Static hosting
    static_dir, static_script = test_static_hosting()
    
    # Test 2: Existing server
    server_dir, flask_app, hostify_script = test_existing_server()
    
    # Summary
    print_section("Test Summary")
    print("[OK] Test files created successfully!\n")
    
    print("Static File Test:")
    print(f"   Directory: {static_dir}")
    print(f"   Script:    {static_script}\n")
    
    print("Flask Server Test:")
    print(f"   Directory: {server_dir}")
    print(f"   Flask App: {flask_app}")
    print(f"   Hostify:   {hostify_script}\n")
    
    print("Next Steps:")
    print("1. Edit the test scripts and replace 'example.com' with your actual domain")
    print("2. Make sure CF_API_TOKEN is set in your environment")
    print("3. Run the test scripts as instructed above")
    print("4. Access your domain via HTTPS to verify it works\n")
    
    print("Tips:")
    print("- Use subdomains for testing (e.g., test-static.yourdomain.com)")
    print("- Check Cloudflare dashboard to see tunnels being created")
    print("- Press Ctrl+C to stop and clean up")
    print("- Verify no tunnels remain in dashboard after stopping\n")
    
    print("=" * 60)
    print("  Test file generation complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
