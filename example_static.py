"""
Example: Host a static website

This script hosts static HTML/CSS/JS files from a directory.
"""

from hostify import Host

# INSTRUCTIONS:
# 1. Create a directory with your HTML files (e.g., ./my-site/)
# 2. Update the domain below to your actual subdomain
# 3. Set your CF_API_TOKEN environment variable
# 4. Run: python example_static.py

Host(
    domain="static.yaspik.tech",  # Change this to your subdomain
    path="./demo_site"             # Change this to your website directory
).serve()

# That's it! Your site will be live at https://static.yaspik.tech
# Press Ctrl+C to stop
