Installation
============

**Latest Version: 0.2.0** - Now with CLI support!

Requirements
------------

- Python >= 3.9
- Cloudflare account with a domain
- Cloudflare API token

Install Hostify
---------------

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

**Windows (PowerShell):**

.. code-block:: powershell

   $env:CF_API_TOKEN="your_token_here"

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

Test your installation:

.. code-block:: python

   from hostify import Host
   print("Hostify installed successfully!")

.. note::
   If you encounter any issues, check the :doc:`troubleshooting` guide.
