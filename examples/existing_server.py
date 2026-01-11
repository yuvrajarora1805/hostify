"""
Example: Host an existing server

This example shows how to host an application that's already running
on a local port (Flask, Node.js, PHP, etc.)
"""

from hostify import Host

# Your application should already be running on port 3000
# For example:
#   - Flask: app.run(port=3000)
#   - Node: app.listen(3000)
#   - PHP: php -S localhost:3000

# Replace with your actual domain
Host(
    domain="app.example.com",
    port=3000  # Port where your app is running
).serve()

# That's it! Your app will be live at https://app.example.com
# Press Ctrl+C to stop
