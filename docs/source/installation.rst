Installation
============

.. raw:: html

   <p class="hero-subtext">Get Hostify up and running in under 2 minutes.</p>

**Latest Version: 0.2.0** - Now with CLI support!

Requirements
------------

.. raw:: html

   <div class="requirements-card">
   <p><strong>🐍 Python</strong> >= 3.9</p>
   <p><strong>☁️ Cloudflare</strong> account with a domain</p>
   <p><strong>🔑 API Token</strong> from Cloudflare</p>
   </div>

Install Hostify
---------------

.. raw:: html

   <div class="code-label">Terminal</div>

Install from PyPI using pip:

.. code-block:: bash

   pip install hostify

Cloudflare Setup
----------------

Step 1: Get API Token
~~~~~~~~~~~~~~~~~~~~~~

1. Go to `Cloudflare API Tokens <https://dash.cloudflare.com/profile/api-tokens>`_
2. Click "Create Token"
3. Use "Edit Cloudflare Zero Trust" template or create custom token with:
   
   - Account → Cloudflare Tunnel → Edit
   - Zone → DNS → Edit
   - Zone → Zone → Read

4. Copy the token

.. tip::
   For detailed Cloudflare setup instructions, see the `Cloudflare Setup Guide <https://github.com/yuvrajarora1805/hostify/blob/main/CLOUDFLARE_SETUP.md>`_

Step 2: Set Environment Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <div class="code-label">Windows PowerShell</div>

**Windows (PowerShell):**

.. code-block:: powershell

   $env:CF_API_TOKEN="your_token_here"

.. raw:: html

   <div class="code-label">Linux/macOS Terminal</div>

**Linux/Mac:**

.. code-block:: bash

   export CF_API_TOKEN="your_token_here"

**Permanent Setup:**

For Linux/Mac, add to ``~/.bashrc`` or ``~/.zshrc``:

.. code-block:: bash

   echo 'export CF_API_TOKEN="your_token_here"' >> ~/.bashrc

For Windows, use System Environment Variables:

.. code-block:: powershell

   setx CF_API_TOKEN "your_token_here"

Step 3: Add Domain to Cloudflare
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure your domain is added to Cloudflare and nameservers are configured.

Verify Installation
-------------------

.. raw:: html

   <div class="code-label">Python</div>

Test your installation:

.. code-block:: python

   from hostify import Host
   print("Hostify installed successfully!")

.. note::
   If you encounter any issues, check the :doc:`troubleshooting` guide.

.. raw:: html

   <div class="success-message">
   ✨ Hostify is now ready. Your local machine just became a server.
   </div>

