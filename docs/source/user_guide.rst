User Guide
==========

This guide covers advanced usage patterns and best practices for Hostify.

Understanding Hostify
---------------------

Hostify uses Cloudflare Tunnels to expose your local applications to the internet without requiring port forwarding or a public IP address. It handles all the complexity of:

- Creating and managing Cloudflare tunnels
- Configuring DNS records
- Managing the cloudflared binary
- Monitoring connection health
- Cleaning up resources on shutdown

Hosting Modes
-------------

Hostify supports two hosting modes:

1. **Existing Server Mode** - Connect to an already-running local server
2. **Static Files Mode** - Serve static HTML/CSS/JS files

Existing Server Mode
~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <h3>Existing Server Mode <span class="mode-badge">MODE</span></h3>

Use this when you have an application already running locally (Flask, Node.js, PHP, etc.):

.. code-block:: python

   from hostify import Host

   # Your app is running on port 3000
   Host(domain="app.example.com", port=3000).serve()

**Requirements:**

- Your application must be running before starting Hostify
- The port must be accessible on localhost
- Port must be between 1-65535

Static Files Mode
~~~~~~~~~~~~~~~~~

.. raw:: html

   <h3>Static Files Mode <span class="mode-badge">MODE</span></h3>

.. raw:: html

   <div class="info-box">
   <strong>Use this mode if:</strong>
   <ul>
     <li>You have a static site (HTML/CSS/JS)</li>
     <li>You want zero config hosting</li>
     <li>You're using an old PC or local machine</li>
   </ul>
   </div>

.. raw:: html

   <p class="context-line">This will serve your local <code>./public</code> folder at <code>mysite.example.com</code>.</p>

.. code-block:: python

   from hostify import Host

   Host(
       domain="mysite.example.com",
       path="./public"  # Directory containing index.html, etc.
   ).serve()

**Features:**

.. raw:: html

   <ul class="features">
   <li>🚀 Starts a built-in HTTP server automatically</li>
   <li>🎯 Finds an available port automatically</li>
   <li>📄 Serves index.html as the default page</li>
   <li>📦 Supports all static file types (HTML, CSS, JS, images, etc.)</li>
   </ul>

Configuration Options
---------------------

Domain Configuration
~~~~~~~~~~~~~~~~~~~~

The domain must be:

- A valid domain or subdomain
- Already added to your Cloudflare account
- Properly configured with Cloudflare nameservers

Examples:

.. code-block:: python

   # Subdomain
   Host(domain="app.example.com", port=3000).serve()

   # Nested subdomain
   Host(domain="api.staging.example.com", port=8000).serve()

API Token Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Three ways to provide your Cloudflare API token:

**1. Environment Variable (Recommended):**

.. code-block:: bash

   export CF_API_TOKEN="your_token"

.. code-block:: python

   Host(domain="app.example.com", port=3000).serve()

**2. Direct Parameter:**

.. code-block:: python

   Host(
       domain="app.example.com",
       port=3000,
       api_token="your_token"
   ).serve()

**3. Configuration File:**

Create a ``.env`` file and load it:

.. code-block:: python

   import os
   from dotenv import load_dotenv
   from hostify import Host

   load_dotenv()  # Loads CF_API_TOKEN from .env
   Host(domain="app.example.com", port=3000).serve()

Advanced Patterns
-----------------

Multiple Applications
~~~~~~~~~~~~~~~~~~~~~

Host multiple applications on different subdomains:

.. code-block:: python

   import threading
   from hostify import Host

   def host_app1():
       Host(domain="app1.example.com", port=3000).serve()

   def host_app2():
       Host(domain="app2.example.com", port=4000).serve()

   # Start both in separate threads
   threading.Thread(target=host_app1).start()
   threading.Thread(target=host_app2).start()

.. warning::
   Each tunnel requires its own process. Make sure your applications are running on different ports.

Integration with Web Frameworks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Flask:**

.. code-block:: python

   from flask import Flask
   from hostify import Host
   import threading

   app = Flask(__name__)

   @app.route('/')
   def home():
       return "Hello from Flask!"

   if __name__ == '__main__':
       # Start Flask
       threading.Thread(
           target=lambda: app.run(port=5000, debug=False)
       ).start()
       
       # Host it
       Host(domain="flask.example.com", port=5000).serve()

**Django:**

.. code-block:: python

   # In a separate script (host_django.py)
   from hostify import Host

   # Django dev server running on port 8000
   Host(domain="django.example.com", port=8000).serve()

Run Django first:

.. code-block:: bash

   # Terminal 1
   python manage.py runserver

   # Terminal 2
   python host_django.py

**FastAPI:**

.. code-block:: python

   from fastapi import FastAPI
   import uvicorn
   from hostify import Host
   import threading

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"Hello": "World"}

   if __name__ == "__main__":
       # Start Uvicorn
       threading.Thread(
           target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000)
       ).start()
       
       # Host it
       Host(domain="fastapi.example.com", port=8000).serve()

Production Deployment
~~~~~~~~~~~~~~~~~~~~~

For production use, consider:

1. **Process Management:** Use systemd, supervisor, or PM2 to keep Hostify running
2. **Logging:** Redirect output to log files
3. **Monitoring:** Monitor tunnel health and restart if needed
4. **Security:** Keep API tokens secure (use environment variables, not hardcoded)

Example systemd service:

.. code-block:: ini

   [Unit]
   Description=Hostify Tunnel for MyApp
   After=network.target

   [Service]
   Type=simple
   User=myuser
   WorkingDirectory=/home/myuser/myapp
   Environment="CF_API_TOKEN=your_token"
   ExecStart=/usr/bin/python3 /home/myuser/myapp/host.py
   Restart=always

   [Install]
   WantedBy=multi-user.target

Best Practices
--------------

1. **Use Environment Variables** for API tokens
2. **Test Locally First** before hosting publicly
3. **Monitor Logs** for connection issues
4. **Use Subdomains** for different environments (dev.example.com, staging.example.com)
5. **Keep Hostify Updated** with ``pip install --upgrade hostify``
6. **Secure Your Application** - Hostify provides HTTPS, but you should still implement authentication

Security Considerations
-----------------------

- **HTTPS is Automatic:** All traffic is encrypted via Cloudflare
- **Firewall Friendly:** No inbound ports need to be opened
- **Token Security:** Keep your Cloudflare API token secure
- **Application Security:** Hostify doesn't add authentication - secure your app!

.. warning::
   Hosting makes your application publicly accessible. Ensure proper authentication and security measures are in place.

Performance Tips
----------------

- **Use Production Servers:** For Python apps, use Gunicorn/uWSGI instead of development servers
- **Enable Caching:** Configure Cloudflare caching rules for static assets
- **Monitor Resources:** Old PCs may have limited resources - monitor CPU/RAM usage
- **Optimize Assets:** Compress images and minify CSS/JS for faster loading

Troubleshooting
---------------

See the :doc:`troubleshooting` guide for common issues and solutions.
