CLI Reference
=============

Hostify provides a powerful command-line interface for quick and easy hosting.

Installation
------------

The CLI is automatically installed when you install Hostify:

.. code-block:: bash

   pip install hostify

Available Commands
------------------

hostify static
~~~~~~~~~~~~~~

Host a static website from a directory.

**Syntax:**

.. code-block:: bash

   hostify static <directory> <domain>

**Arguments:**

* ``directory`` - Path to the directory containing static files (HTML, CSS, JS)
* ``domain`` - Domain name to host on (e.g., ``mysite.example.com``)

**Example:**

.. code-block:: bash

   hostify static ./my-website mysite.example.com

This will:

1. Start a local HTTP server for your static files
2. Create a Cloudflare tunnel
3. Configure DNS automatically
4. Make your site live at ``https://mysite.example.com``

hostify port
~~~~~~~~~~~~

Host an existing server running on a port.

**Syntax:**

.. code-block:: bash

   hostify port <port> <domain>

**Arguments:**

* ``port`` - Port number where your server is running (1-65535)
* ``domain`` - Domain name to host on (e.g., ``app.example.com``)

**Example:**

.. code-block:: bash

   # Terminal 1: Start your Flask app
   python app.py

   # Terminal 2: Host it with Hostify
   hostify port 5000 flask-app.example.com

hostify version
~~~~~~~~~~~~~~~

Display version information.

**Syntax:**

.. code-block:: bash

   hostify version

**Output:**

.. code-block:: text

   Hostify v0.2.0
   Effortless application hosting using Cloudflare Tunnels

   Repository: https://github.com/yuvrajarora1805/hostify
   Documentation: https://hostify.readthedocs.io

hostify --help
~~~~~~~~~~~~~~

Show comprehensive help information.

**Syntax:**

.. code-block:: bash

   hostify --help

Environment Setup
-----------------

Before using the CLI, set your Cloudflare API token:

**Windows (PowerShell):**

.. code-block:: powershell

   $env:CLOUDFLARE_API_TOKEN="your-token-here"

**Linux/macOS:**

.. code-block:: bash

   export CLOUDFLARE_API_TOKEN="your-token-here"

**Permanent Setup:**

Add to your shell profile (``~/.bashrc``, ``~/.zshrc``, etc.):

.. code-block:: bash

   export CLOUDFLARE_API_TOKEN="your-token-here"

For Windows, use System Environment Variables or add to PowerShell profile.

CLI Examples
------------

Example 1: Static Portfolio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   hostify static ./portfolio portfolio.example.com

Example 2: Flask Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Start Flask on port 5000
   python app.py

   # In another terminal
   hostify port 5000 flask-app.example.com

Example 3: React Dev Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Start React (usually port 3000)
   npm start

   # In another terminal
   hostify port 3000 react-app.example.com

Example 4: Django Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Start Django on port 8000
   python manage.py runserver

   # In another terminal
   hostify port 8000 django-app.example.com

Stopping the Server
-------------------

Press ``Ctrl+C`` in the terminal where Hostify is running. This will:

1. Stop the tunnel process
2. Delete the DNS record
3. Delete the tunnel
4. Clean up all resources
5. Stop the static server (if applicable)

All cleanup is automatic and graceful.

Error Handling
--------------

CLOUDFLARE_API_TOKEN not set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see this error:

.. code-block:: text

   [!] Error: CLOUDFLARE_API_TOKEN environment variable not set.

**Solution:** Set your Cloudflare API token as shown in the Environment Setup section above.

Directory does not exist
~~~~~~~~~~~~~~~~~~~~~~~~~

If you see:

.. code-block:: text

   [!] Error: Directory 'path' does not exist.

**Solution:** Check that the directory path is correct and the directory exists.

Invalid port number
~~~~~~~~~~~~~~~~~~~

If you see:

.. code-block:: text

   [!] Error: Invalid port number

**Solution:** Ensure the port is between 1 and 65535 and your server is running on that port.

Tips & Best Practices
---------------------

1. **Always start your server first** before using ``hostify port``
2. **Use absolute paths** or ensure you're in the correct directory for ``hostify static``
3. **Keep the terminal open** - closing it will stop hosting
4. **Use Ctrl+C to stop** - don't just close the terminal
5. **Check DNS propagation** - it may take 30-60 seconds for the site to be fully accessible

See Also
--------

* :doc:`quickstart` - Getting started guide
* :doc:`examples` - More usage examples
* :doc:`troubleshooting` - Common issues and solutions
