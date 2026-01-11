# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-11

### Added
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

### Fixed
- Windows Unicode encoding issues (replaced emojis with ASCII)
- Port validation for detecting running servers
- Static server startup validation with retry logic
- Tunnel route configuration for proper hostname routing

### Tested
- Live deployment on hostify.yaspik.tech (static site)
- Live deployment on app.yaspik.tech (Flask app on port 5000)
- All core functionality verified
- Cross-platform compatibility confirmed

---

## [Unreleased]

### Planned Features
- Multiple domain support
- Web dashboard for management
- Authentication system
- Custom cloudflared configuration
- Load balancing support
- Health checks and monitoring
- Configuration file support
- CLI tool

---

[0.1.0]: https://github.com/yourusername/hostify/releases/tag/v0.1.0
