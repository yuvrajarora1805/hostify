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

## [0.2.0] - 2026-01-12

### Added
- **CLI Tool**: Complete command-line interface for Hostify
  - `hostify static <directory> <domain>` - Host static sites from the command line
  - `hostify port <port> <domain>` - Host existing servers via CLI
  - `hostify version` - Display version information
  - `hostify --help` - Show comprehensive help
- Graceful shutdown handling with Ctrl+C
- User-friendly error messages and validation
- Environment variable validation for `CLOUDFLARE_API_TOKEN`
- Signal handlers for clean cleanup on exit
- Comprehensive CLI documentation

### Changed
- Updated all version references to 0.2.0
- Enhanced user experience with direct terminal access
- Improved error handling and user feedback

### Documentation
- Added CLI usage examples to README
- Updated installation instructions for CLI usage
- Added CLI command reference

---

---

## [0.2.1] - 2026-01-16

### Fixed
- **Tunnel Deletion**: Fixed 400 Bad Request error when deleting tunnels with active connections
  - Added force deletion option to clean up connections before deleting tunnel
  - Improved error handling for already-deleted resources (404 errors)
  - Better cleanup process that handles orphaned tunnels gracefully
- **API Token Support**: Added support for `CLOUDFLARE_API_TOKEN` environment variable
  - Library now accepts both `CF_API_TOKEN` and `CLOUDFLARE_API_TOKEN`
  - Improved API token detection and error messages
  - Better compatibility with different Cloudflare setups

### Changed
- Enhanced `delete_tunnel()` method with optional `force` parameter
- Updated cleanup process to use force deletion by default
- Improved error messages for API token configuration

### Added
- Force cleanup utility script for manually removing orphaned tunnels
- Better handling of tunnel connection cleanup

---

## [Unreleased]

---

## [0.1.1] - 2026-01-11

### Changed
- Updated README with correct GitHub repository URLs
- Added Star History badge with correct username
- Updated all documentation links

---

## [0.1.0] - 2026-01-11

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

[0.1.0]: https://github.com/yuvrajarora1805/hostify/releases/tag/v0.1.0
