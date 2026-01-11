"""
Example: Host a static website

This example shows how to host static files from a directory.
"""

from hostify import Host

# Serve static files from the current directory
# Replace with your actual domain and path
Host(
    domain="mysite.example.com",
    path="./public"  # Directory containing your static files (index.html, etc.)
).serve()

# That's it! Your site will be live at https://mysite.example.com
# Press Ctrl+C to stop
