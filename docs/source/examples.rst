Examples
========

Real-world examples of using Hostify with different frameworks and use cases.

Basic Examples
--------------

Static Website
~~~~~~~~~~~~~~

Host a simple static website:

.. code-block:: python

   from hostify import Host

   Host(
       domain="mysite.example.com",
       path="./website"
   ).serve()

Directory structure:

.. code-block:: text

   website/
   ├── index.html
   ├── style.css
   ├── script.js
   └── images/
       └── logo.png

Existing Local Server
~~~~~~~~~~~~~~~~~~~~~

Connect to a server already running on port 3000:

.. code-block:: python

   from hostify import Host

   Host(domain="app.example.com", port=3000).serve()

Web Framework Examples
----------------------

Flask Application
~~~~~~~~~~~~~~~~~

Complete Flask example with routing:

.. code-block:: python

   from flask import Flask, render_template, jsonify
   from hostify import Host
   import threading

   app = Flask(__name__)

   @app.route('/')
   def home():
       return render_template('index.html')

   @app.route('/api/data')
   def get_data():
       return jsonify({'message': 'Hello from Flask!'})

   if __name__ == '__main__':
       # Start Flask in background
       flask_thread = threading.Thread(
           target=lambda: app.run(host='127.0.0.1', port=5000, debug=False)
       )
       flask_thread.daemon = True
       flask_thread.start()
       
       # Give Flask time to start
       import time
       time.sleep(2)
       
       # Host with Hostify
       Host(domain="flask.example.com", port=5000).serve()

Django Project
~~~~~~~~~~~~~~

For Django, run the development server first, then host it:

**host_django.py:**

.. code-block:: python

   from hostify import Host

   # Django dev server should be running on port 8000
   Host(domain="django.example.com", port=8000).serve()

**Usage:**

.. code-block:: bash

   # Terminal 1: Start Django
   python manage.py runserver

   # Terminal 2: Host with Hostify
   python host_django.py

FastAPI Application
~~~~~~~~~~~~~~~~~~~

Modern async API with FastAPI:

.. code-block:: python

   from fastapi import FastAPI
   from fastapi.responses import HTMLResponse
   import uvicorn
   from hostify import Host
   import threading
   import time

   app = FastAPI()

   @app.get("/")
   async def root():
       return {"message": "Hello World"}

   @app.get("/items/{item_id}")
   async def read_item(item_id: int):
       return {"item_id": item_id}

   if __name__ == "__main__":
       # Start Uvicorn server
       uvicorn_thread = threading.Thread(
           target=lambda: uvicorn.run(
               app,
               host="127.0.0.1",
               port=8000,
               log_level="info"
           )
       )
       uvicorn_thread.daemon = True
       uvicorn_thread.start()
       
       # Wait for server to start
       time.sleep(3)
       
       # Host with Hostify
       Host(domain="fastapi.example.com", port=8000).serve()

Streamlit Dashboard
~~~~~~~~~~~~~~~~~~~

Host a Streamlit data dashboard:

**app.py:**

.. code-block:: python

   import streamlit as st
   import pandas as pd
   import numpy as np

   st.title('My Dashboard')
   
   chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c']
   )
   
   st.line_chart(chart_data)

**host_streamlit.py:**

.. code-block:: python

   import subprocess
   import time
   from hostify import Host

   # Start Streamlit
   streamlit_process = subprocess.Popen(
       ['streamlit', 'run', 'app.py', '--server.port=8501'],
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE
   )

   # Wait for Streamlit to start
   time.sleep(5)

   try:
       # Host with Hostify
       Host(domain="dashboard.example.com", port=8501).serve()
   finally:
       streamlit_process.terminate()

Node.js Application
~~~~~~~~~~~~~~~~~~~

Host a Node.js/Express server:

**server.js:**

.. code-block:: javascript

   const express = require('express');
   const app = express();
   const port = 3000;

   app.get('/', (req, res) => {
       res.send('Hello from Node.js!');
   });

   app.listen(port, () => {
       console.log(`Server running on port ${port}`);
   });

**host_node.py:**

.. code-block:: python

   from hostify import Host

   # Node server should be running on port 3000
   Host(domain="node.example.com", port=3000).serve()

**Usage:**

.. code-block:: bash

   # Terminal 1: Start Node.js
   node server.js

   # Terminal 2: Host with Hostify
   python host_node.py

Advanced Examples
-----------------

Multiple Environments
~~~~~~~~~~~~~~~~~~~~~

Host dev and staging environments:

.. code-block:: python

   import threading
   from hostify import Host

   def host_dev():
       Host(domain="dev.example.com", port=3000).serve()

   def host_staging():
       Host(domain="staging.example.com", port=4000).serve()

   # Start both
   dev_thread = threading.Thread(target=host_dev)
   staging_thread = threading.Thread(target=host_staging)

   dev_thread.start()
   staging_thread.start()

   dev_thread.join()
   staging_thread.join()

API with Custom Token
~~~~~~~~~~~~~~~~~~~~~

Use different API tokens for different domains:

.. code-block:: python

   from hostify import Host

   # Production domain with production token
   Host(
       domain="api.production.com",
       port=8000,
       api_token="prod_token_here"
   ).serve()

Documentation Site
~~~~~~~~~~~~~~~~~~

Host Sphinx documentation:

.. code-block:: python

   from hostify import Host

   # Build docs first, then serve the _build/html directory
   Host(
       domain="docs.example.com",
       path="./docs/_build/html"
   ).serve()

Portfolio Website
~~~~~~~~~~~~~~~~~

Host a personal portfolio:

.. code-block:: python

   from hostify import Host

   Host(
       domain="portfolio.yourname.com",
       path="./portfolio-site"
   ).serve()

**portfolio-site/** structure:

.. code-block:: text

   portfolio-site/
   ├── index.html
   ├── about.html
   ├── projects.html
   ├── css/
   │   └── style.css
   ├── js/
   │   └── main.js
   └── images/
       ├── profile.jpg
       └── projects/

Webhook Testing
~~~~~~~~~~~~~~~

Test webhooks locally:

.. code-block:: python

   from flask import Flask, request
   from hostify import Host
   import threading

   app = Flask(__name__)

   @app.route('/webhook', methods=['POST'])
   def webhook():
       data = request.json
       print(f"Received webhook: {data}")
       return {'status': 'success'}, 200

   if __name__ == '__main__':
       # Start Flask
       threading.Thread(
           target=lambda: app.run(port=5000, debug=False)
       ).start()
       
       import time
       time.sleep(2)
       
       # Host publicly for webhook testing
       Host(domain="webhook.example.com", port=5000).serve()

Now you can configure webhooks to point to ``https://webhook.example.com/webhook``!

Demo/Presentation Server
~~~~~~~~~~~~~~~~~~~~~~~~

Quickly share your work with clients:

.. code-block:: python

   from hostify import Host

   # Your demo app is running on port 3000
   Host(domain="demo.example.com", port=3000).serve()

Share ``https://demo.example.com`` with your client - no deployment needed!

Tips for Examples
-----------------

1. **Always test locally first** before hosting publicly
2. **Use unique subdomains** for each project
3. **Keep API tokens secure** - never commit them to version control
4. **Monitor resource usage** on old hardware
5. **Use process managers** (systemd, PM2) for production deployments

Next Steps
----------

- Check the :doc:`user_guide` for advanced patterns
- Read the :doc:`troubleshooting` guide if you encounter issues
- Explore the :doc:`api` reference for all available options
