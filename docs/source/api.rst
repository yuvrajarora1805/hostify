API Reference
=============

This page contains the complete API documentation for Hostify.

Host Class
----------

.. autoclass:: hostify.Host
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

The ``Host`` class is the main entry point for using Hostify. It manages the entire lifecycle of hosting your application through Cloudflare Tunnels.

Constructor Parameters
~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: Host(domain, port=None, path=None, api_token=None)

   Initialize a Host instance.

   :param str domain: Full domain or subdomain (e.g., "app.example.com"). **Required.**
   :param int port: Port number where your application is running (1-65535). Mutually exclusive with ``path``.
   :param str path: Path to directory containing static files to serve. Mutually exclusive with ``port``.
   :param str api_token: Cloudflare API token. If not provided, reads from ``CF_API_TOKEN`` environment variable.
   :raises HostError: If configuration is invalid (e.g., both port and path specified, or neither specified).

   .. note::
      You must specify either ``port`` OR ``path``, but not both.

Methods
~~~~~~~

.. py:method:: serve()

   Start hosting the application.

   This method:
   
   1. Validates the local server or starts static server
   2. Creates Cloudflare tunnel
   3. Creates DNS record
   4. Starts cloudflared process
   5. Monitors and keeps the connection alive

   :raises HostError: If setup fails at any step.
   :return: None (blocks until Ctrl+C is pressed)

   **Example:**

   .. code-block:: python

      from hostify import Host

      host = Host(domain="app.example.com", port=3000)
      host.serve()  # Blocks until Ctrl+C

.. py:method:: cleanup()

   Clean up all resources.

   This method is called automatically when you press Ctrl+C or when the program exits. It:
   
   1. Stops cloudflared process
   2. Deletes DNS record
   3. Deletes tunnel
   4. Stops static server if running

   You typically don't need to call this manually.

   :return: None

Exceptions
----------

.. autoclass:: hostify.HostError
   :members:
   :show-inheritance:

   Custom exception raised when Hostify encounters an error.

   **Common causes:**

   - Invalid configuration (missing domain, both port and path specified, etc.)
   - Cloudflare API errors (invalid token, zone not found, etc.)
   - Local server not running on specified port
   - Tunnel connection failures

Cloudflare Module
-----------------

.. autoclass:: hostify.cloudflare.Cloudflare
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: hostify.cloudflare.CloudflareAPIError
   :members:
   :show-inheritance:

Cloudflared Module
------------------

.. autoclass:: hostify.cloudflared.Cloudflared
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: hostify.cloudflared.CloudflaredError
   :members:
   :show-inheritance:

Utility Functions
-----------------

.. automodule:: hostify.utils
   :members:
   :undoc-members:
   :show-inheritance:

Type Hints
----------

All functions and methods in Hostify include type hints for better IDE support and type checking.

Example with type hints:

.. code-block:: python

   from hostify import Host
   from typing import Optional

   def create_host(
       domain: str,
       port: Optional[int] = None,
       path: Optional[str] = None
   ) -> Host:
       return Host(domain=domain, port=port, path=path)

   host = create_host("app.example.com", port=3000)
   host.serve()
