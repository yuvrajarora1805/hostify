Quick Start
===========

This guide will get you up and running with Hostify in under 5 minutes.

Basic Usage
-----------

The simplest way to use Hostify:

.. code-block:: python

   from hostify import Host

   # Host your app in one line
   Host(domain="app.example.com", port=3000).serve()

That's it! Your application running on port 3000 is now live at ``https://app.example.com``.

Step-by-Step Tutorial
----------------------

Step 1: Install Hostify
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install hostify

Step 2: Set Up Cloudflare
~~~~~~~~~~~~~~~~~~~~~~~~~~

Get your Cloudflare API token and set it as an environment variable:

.. code-block:: bash

   export CF_API_TOKEN="your_cloudflare_api_token"

See :doc:`installation` for detailed setup instructions.

Step 3: Start Your Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure your application is already running. For example, if you have a Flask app:

.. code-block:: bash

   python app.py

Your app should now be running on a local port (e.g., port 5000).

Step 4: Host It with Hostify
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file ``host.py``:

.. code-block:: python

   from hostify import Host

   Host(
       domain="myapp.example.com",
       port=5000
   ).serve()

Run it:

.. code-block:: bash

   python host.py

You'll see output like:

.. code-block:: text

   [HOSTIFY] Starting tunnel for myapp.example.com
   ============================================================
   [+] Checking for server on port 5000...
       [OK] Server detected on http://localhost:5000
   [+] Creating Cloudflare tunnel...
       [OK] Tunnel created: abc123...
   [+] Setting up DNS for myapp.example.com...
       [OK] DNS record created
   [+] Starting tunnel connection...
       [OK] Tunnel process started
   
   ============================================================
   [SUCCESS] Your site is now live at:
      https://myapp.example.com
   ============================================================

Step 5: Access Your Site
~~~~~~~~~~~~~~~~~~~~~~~~~

Open your browser and visit ``https://myapp.example.com`` - your local app is now live on the internet!

Press ``Ctrl+C`` to stop the tunnel. Hostify will automatically clean up all resources.

Common Patterns
---------------

Host Static Files
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hostify import Host

   Host(
       domain="mysite.example.com",
       path="./public"
   ).serve()

Host Flask Application
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from flask import Flask
   from hostify import Host
   import threading

   app = Flask(__name__)

   @app.route('/')
   def home():
       return "<h1>Hello World!</h1>"

   if __name__ == '__main__':
       # Start Flask in background
       threading.Thread(target=lambda: app.run(port=5000)).start()
       
       # Host it with hostify
       Host(domain="flask.example.com", port=5000).serve()

Custom API Token
~~~~~~~~~~~~~~~~

If you don't want to use environment variables:

.. code-block:: python

   from hostify import Host

   Host(
       domain="app.example.com",
       port=8000,
       api_token="your_cloudflare_api_token"
   ).serve()

Next Steps
----------

- Read the :doc:`user_guide` for advanced usage
- Check out :doc:`examples` for more real-world scenarios
- Explore the :doc:`api` reference for all available options
