"""
Example: Host a Flask application

This example shows a complete Flask app with hostify.
"""

# Step 1: Create your Flask app (save as flask_app.py)
# --------------------------------------------------------
# from flask import Flask
# 
# app = Flask(__name__)
# 
# @app.route('/')
# def home():
#     return """
#     <h1>Hello from my old PC!</h1>
#     <p>This Flask app is running on an old computer and accessible via Cloudflare Tunnels.</p>
#     """
# 
# @app.route('/api/status')
# def status():
#     return {"status": "running", "message": "Flask + Hostify = ❤️"}
# 
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


# Step 2: Host it with hostify (save as host_flask.py)
# --------------------------------------------------------
from hostify import Host

# Make sure flask_app.py is running first!
# python flask_app.py

Host(
    domain="flask.example.com",
    port=5000
).serve()

# Your Flask app is now live at https://flask.example.com
# Press Ctrl+C to stop
