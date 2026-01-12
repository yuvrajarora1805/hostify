Hostify Documentation
=====================

**Turn old PCs into production servers with one line of code.**

Host applications from old PCs or home machines using Cloudflare Tunnels. No port forwarding, no dynamic DNS, just pure simplicity.

.. image:: https://badge.fury.io/py/hostify.svg
   :target: https://badge.fury.io/py/hostify
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/hostify.svg
   :target: https://pypi.org/project/hostify/
   :alt: Python versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

Quick Example
-------------

.. code-block:: python

   from hostify import Host

   # Host your app in one line
   Host(domain="app.example.com", port=3000).serve()

That's it! Your app is now live at ``https://app.example.com`` with automatic HTTPS.

Key Features
------------

✅ **One-line API** - Simple and intuitive

✅ **Automatic HTTPS** - Secure by default via Cloudflare

✅ **No Port Forwarding** - Works behind NAT/firewalls

✅ **Cross-Platform** - Windows, Linux, macOS

✅ **Static Files** - Built-in HTTP server

✅ **Existing Servers** - Works with Flask, Node, PHP, etc.

✅ **Auto-Cleanup** - Graceful shutdown with Ctrl+C

✅ **Auto-Recovery** - Restarts on connection issues

Live Demos
----------

Check out these live examples hosted with Hostify:

- **Static Site:** https://hostify.yaspik.tech
- **Flask App:** https://app.yaspik.tech

Getting Started
---------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   user_guide
   examples
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   api

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   contributing
   changelog

Use Cases
---------

1. **Development** - Share local dev server with team
2. **Demos** - Show clients your work without deployment
3. **Old Hardware** - Turn old PCs into production servers
4. **Home Labs** - Host personal projects from home
5. **Testing** - Test webhooks and integrations locally

Community & Support
-------------------

- **GitHub:** https://github.com/yuvrajarora1805/hostify
- **Issues:** https://github.com/yuvrajarora1805/hostify/issues
- **PyPI:** https://pypi.org/project/hostify/

.. note::
   Made with ❤️ for developers who want to host from anywhere
   
   Created by Yuvraj Arora
   
   Uses Cloudflare Tunnel & Cloudflare APIs

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
