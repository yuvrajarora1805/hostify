"""
Example: Host an application running on a port

This script hosts an application that's already running on a local port.
Works with Flask, Node.js, PHP, or any HTTP server.
"""

from hostify import Host

# INSTRUCTIONS:
# 1. Start your application first (e.g., Flask on port 5000)
# 2. Update the domain and port below
# 3. Set your CF_API_TOKEN environment variable
# 4. Run: python example_port.py

# IMPORTANT: Your application must be running BEFORE you run this script!

Host(
    domain="app.yaspik.tech",  # Change this to your subdomain
    port=5000                   # Change this to your app's port
).serve()

# Your app is now live at https://app.yaspik.tech
# Press Ctrl+C to stop

# Example applications that work:
# - Flask: app.run(port=5000)
# - Node/Express: app.listen(3000)
# - PHP: php -S localhost:8000
# - Python HTTP server: python -m http.server 8000
