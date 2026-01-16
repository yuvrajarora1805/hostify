Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[0.2.1] - 2026-01-16
--------------------

Fixed
~~~~~

- **Tunnel Deletion**: Fixed 400 Bad Request error when deleting tunnels with active connections

  - Added force deletion option to clean up connections before deleting tunnel
  - Improved error handling for already-deleted resources (404 errors)
  - Better cleanup process that handles orphaned tunnels gracefully

- **API Token Support**: Added support for ``CLOUDFLARE_API_TOKEN`` environment variable

  - Library now accepts both ``CF_API_TOKEN`` and ``CLOUDFLARE_API_TOKEN``
  - Improved API token detection and error messages
  - Better compatibility with different Cloudflare setups

Changed
~~~~~~~

- Enhanced ``delete_tunnel()`` method with optional ``force`` parameter
- Updated cleanup process to use force deletion by default
- Improved error messages for API token configuration

Added
~~~~~

- Force cleanup utility script for manually removing orphaned tunnels
- Better handling of tunnel connection cleanup

[0.1.1] - 2026-01-11
--------------------

Changed
~~~~~~~

- Updated README with correct GitHub repository URLs
- Added Star History badge with correct username
- Updated all documentation links

[0.1.0] - 2026-01-11
--------------------

Added
~~~~~

- Initial release of hostify library
- One-line API for hosting applications via Cloudflare Tunnels
- Support for static file hosting
- Support for existing server hosting (port-based)
- Automatic cloudflared binary download and management
- Cross-platform support (Windows, Linux, macOS)
- Automatic HTTPS via Cloudflare
- Graceful shutdown with complete cleanup
- DNS record automation
- Tunnel route configuration
- Comprehensive test suite (9/9 tests passing)
- Full documentation (README, INSTALL, CLOUDFLARE_SETUP)
- Working examples (static_site.py, existing_server.py, flask_example.py)
- MIT License

Fixed
~~~~~

- Windows Unicode encoding issues (replaced emojis with ASCII)
- Port validation for detecting running servers
- Static server startup validation with retry logic
- Tunnel route configuration for proper hostname routing

Tested
~~~~~~

- Live deployment on hostify.yaspik.tech (static site)
- Live deployment on app.yaspik.tech (Flask app on port 5000)
- All core functionality verified
- Cross-platform compatibility confirmed

Planned Features
----------------

- Multiple domain support
- Web dashboard for management
- Authentication system
- Custom cloudflared configuration
- Load balancing support
- Health checks and monitoring
- Configuration file support
- CLI tool
