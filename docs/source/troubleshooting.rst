Troubleshooting
===============

Common issues and their solutions.

Installation Issues
-------------------

"pip install hostify" fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Installation fails with error messages.

**Solutions:**

1. **Update pip:**

   .. code-block:: bash

      python -m pip install --upgrade pip

2. **Use Python 3.9+:**

   .. code-block:: bash

      python --version  # Should be 3.9 or higher

3. **Try with --user flag:**

   .. code-block:: bash

      pip install --user hostify

Import Error
~~~~~~~~~~~~

**Problem:** ``ModuleNotFoundError: No module named 'hostify'``

**Solutions:**

1. **Verify installation:**

   .. code-block:: bash

      pip show hostify

2. **Check Python environment:**

   .. code-block:: bash

      which python
      which pip

3. **Reinstall:**

   .. code-block:: bash

      pip uninstall hostify
      pip install hostify

Configuration Issues
--------------------

"Cloudflare API token not found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Error message about missing API token.

**Solutions:**

1. **Set environment variable:**

   .. code-block:: bash

      # Linux/Mac
      export CF_API_TOKEN="your_token"

      # Windows PowerShell
      $env:CF_API_TOKEN="your_token"

2. **Pass token directly:**

   .. code-block:: python

      Host(
          domain="app.example.com",
          port=3000,
          api_token="your_token_here"
      ).serve()

3. **Verify token is set:**

   .. code-block:: bash

      # Linux/Mac
      echo $CF_API_TOKEN

      # Windows PowerShell
      echo $env:CF_API_TOKEN

"No Cloudflare accounts found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** API token doesn't have correct permissions.

**Solution:**

Create a new token with these permissions:

- Account → Cloudflare Tunnel → Edit
- Zone → DNS → Edit
- Zone → Zone → Read

See :doc:`installation` for detailed instructions.

"Zone not found for domain"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Domain is not configured in Cloudflare.

**Solutions:**

1. **Add domain to Cloudflare:**
   
   - Go to Cloudflare dashboard
   - Click "Add a Site"
   - Follow the setup wizard

2. **Update nameservers:**
   
   - Point your domain's nameservers to Cloudflare
   - Wait for DNS propagation (can take up to 24 hours)

3. **Verify domain is active:**
   
   - Check Cloudflare dashboard
   - Domain status should be "Active"

Server Issues
-------------

"No server found on port X"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Hostify can't connect to your local server.

**Solutions:**

1. **Start your application first:**

   .. code-block:: bash

      # Terminal 1: Start your app
      python app.py

      # Terminal 2: Run Hostify
      python host.py

2. **Verify server is running:**

   .. code-block:: bash

      # Linux/Mac
      lsof -i :3000

      # Windows
      netstat -ano | findstr :3000

3. **Test server locally:**

   Open browser and visit ``http://localhost:3000``

4. **Check firewall:**

   Ensure localhost connections are allowed

"Port already in use"
~~~~~~~~~~~~~~~~~~~~~

**Problem:** The port you're trying to use is occupied.

**Solutions:**

1. **Find what's using the port:**

   .. code-block:: bash

      # Linux/Mac
      lsof -i :3000

      # Windows
      netstat -ano | findstr :3000

2. **Kill the process:**

   .. code-block:: bash

      # Linux/Mac
      kill -9 <PID>

      # Windows
      taskkill /PID <PID> /F

3. **Use a different port:**

   .. code-block:: python

      Host(domain="app.example.com", port=3001).serve()

Connection Issues
-----------------

Site shows 404 or "Not Found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Domain loads but shows 404 error.

**Solutions:**

1. **Wait for tunnel to connect:**
   
   Wait 30-60 seconds after starting Hostify

2. **Check server is responding:**

   .. code-block:: bash

      curl http://localhost:3000

3. **Verify DNS propagation:**

   .. code-block:: bash

      nslookup app.example.com

4. **Check Cloudflare dashboard:**
   
   - Verify tunnel is active
   - Check DNS record exists

"Tunnel process stopped unexpectedly"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Tunnel keeps disconnecting.

**Solutions:**

1. **Check internet connection:**
   
   Ensure stable internet connectivity

2. **Check cloudflared logs:**
   
   Look for error messages in the output

3. **Restart Hostify:**
   
   Press Ctrl+C and run again

4. **Update Hostify:**

   .. code-block:: bash

      pip install --upgrade hostify

Site loads slowly
~~~~~~~~~~~~~~~~~

**Problem:** Website takes a long time to load.

**Solutions:**

1. **Check local server performance:**
   
   Test ``http://localhost:3000`` directly

2. **Optimize application:**
   
   - Compress images
   - Minify CSS/JS
   - Enable caching

3. **Check hardware resources:**
   
   Monitor CPU/RAM usage on host machine

4. **Use production server:**
   
   Replace development servers with Gunicorn/uWSGI

Cleanup Issues
--------------

"Failed to delete tunnel"
~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Cleanup fails when stopping Hostify.

**Solutions:**

1. **Manual cleanup via Cloudflare dashboard:**
   
   - Go to Zero Trust → Networks → Tunnels
   - Delete orphaned tunnels manually

2. **Check API token permissions:**
   
   Ensure token has "Edit" permission for Tunnels

3. **Ignore if tunnel was already deleted:**
   
   This warning is usually harmless

DNS record not deleted
~~~~~~~~~~~~~~~~~~~~~~

**Problem:** DNS record remains after stopping.

**Solutions:**

1. **Manual deletion:**
   
   - Go to Cloudflare dashboard
   - Navigate to DNS settings
   - Delete the CNAME record

2. **Verify API token permissions:**
   
   Ensure token has "Edit" permission for DNS

Platform-Specific Issues
------------------------

Windows: "cloudflared.exe not found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Windows can't find the cloudflared binary.

**Solutions:**

1. **Check antivirus:**
   
   Antivirus may be blocking the download

2. **Manual download:**
   
   Download from https://github.com/cloudflare/cloudflared/releases

3. **Add to PATH:**
   
   Place cloudflared.exe in a directory in your PATH

Linux: Permission denied
~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Permission errors when running Hostify.

**Solutions:**

1. **Check file permissions:**

   .. code-block:: bash

      chmod +x ~/.hostify/cloudflared

2. **Run with proper permissions:**

   .. code-block:: bash

      # Don't use sudo unless necessary
      python host.py

macOS: "cloudflared cannot be opened"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** macOS security blocks cloudflared.

**Solutions:**

1. **Allow in Security & Privacy:**
   
   - System Preferences → Security & Privacy
   - Click "Allow Anyway" for cloudflared

2. **Remove quarantine attribute:**

   .. code-block:: bash

      xattr -d com.apple.quarantine ~/.hostify/cloudflared

Getting Help
------------

If you're still experiencing issues:

1. **Check GitHub Issues:**
   
   https://github.com/yuvrajarora1805/hostify/issues

2. **Create a new issue:**
   
   Include:
   
   - Python version (``python --version``)
   - Hostify version (``pip show hostify``)
   - Operating system
   - Full error message
   - Steps to reproduce

3. **Enable debug logging:**

   .. code-block:: python

      import logging
      logging.basicConfig(level=logging.DEBUG)
      
      from hostify import Host
      Host(domain="app.example.com", port=3000).serve()

Common Error Messages
---------------------

Quick reference for error messages:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Error Message
     - Solution
   * - "Domain is required"
     - Provide a domain parameter
   * - "Either 'port' or 'path' must be specified"
     - Specify either port OR path
   * - "Cannot specify both 'port' and 'path'"
     - Use only one: port OR path
   * - "Invalid port"
     - Use port between 1-65535
   * - "Path does not exist"
     - Check the path to your static files
   * - "Path is not a directory"
     - Path must point to a directory, not a file
   * - "Failed to create tunnel"
     - Check API token and permissions
   * - "Failed to create DNS record"
     - Verify domain is in Cloudflare
