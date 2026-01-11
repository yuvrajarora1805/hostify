# Hostify - Host from Anywhere

**Turn old PCs into production servers with one line of code.**

Host applications from old PCs or home machines using Cloudflare Tunnels. No port forwarding, no dynamic DNS, just pure simplicity.

[![PyPI version](https://badge.fury.io/py/hostify.svg)](https://badge.fury.io/py/hostify)
[![Python](https://img.shields.io/pypi/pyversions/hostify.svg)](https://pypi.org/project/hostify/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Quick Start

```python
from hostify import Host

# Host your app in one line
Host(domain="app.example.com", port=3000).serve()
```

That's it! Your app is now live at `https://app.example.com` with automatic HTTPS.

---

## 📦 Installation

```bash
pip install hostify
```

**Requirements:**
- Python >= 3.9
- Cloudflare account with a domain
- Cloudflare API token ([setup guide](CLOUDFLARE_SETUP.md))

---

## 🎯 Features

- ✅ **One-line API** - Simple and intuitive
- ✅ **Automatic HTTPS** - Secure by default via Cloudflare
- ✅ **No Port Forwarding** - Works behind NAT/firewalls
- ✅ **Cross-Platform** - Windows, Linux, macOS
- ✅ **Static Files** - Built-in HTTP server
- ✅ **Existing Servers** - Works with Flask, Node, PHP, etc.
- ✅ **Auto-Cleanup** - Graceful shutdown with Ctrl+C
- ✅ **Auto-Recovery** - Restarts on connection issues

---

## 💡 Use Cases

1. **Development** - Share local dev server with team
2. **Demos** - Show clients your work without deployment
3. **Old Hardware** - Turn old PCs into production servers
4. **Home Labs** - Host personal projects from home
5. **Testing** - Test webhooks and integrations locally

---

## 📖 Usage Examples

### Example 1: Host Static Files

```python
from hostify import Host

# Serve static HTML/CSS/JS files
Host(
    domain="mysite.example.com",
    path="./public"
).serve()
```

### Example 2: Host Flask App

```python
from flask import Flask
from hostify import Host

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello World!</h1>"

if __name__ == '__main__':
    # Start Flask in background
    import threading
    threading.Thread(target=lambda: app.run(port=5000)).start()
    
    # Host it with hostify
    Host(domain="flask.example.com", port=5000).serve()
```

### Example 3: Host Existing Server

```python
from hostify import Host

# Your Node.js/PHP/Python server is already running on port 3000
Host(domain="app.example.com", port=3000).serve()
```

### Example 4: Custom API Token

```python
from hostify import Host

Host(
    domain="app.example.com",
    port=8000,
    api_token="your_cloudflare_api_token"
).serve()
```

---

## 🔧 Setup Guide

### Step 1: Install Hostify

```bash
pip install hostify
```

### Step 2: Get Cloudflare API Token

1. Go to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Click "Create Token"
3. Use "Edit Cloudflare Zero Trust" template or create custom token with:
   - Account → Cloudflare Tunnel → Edit
   - Zone → DNS → Edit
   - Zone → Zone → Read
4. Copy the token

**Detailed guide:** [CLOUDFLARE_SETUP.md](CLOUDFLARE_SETUP.md)

### Step 3: Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:CF_API_TOKEN="your_token_here"
```

**Linux/Mac:**
```bash
export CF_API_TOKEN="your_token_here"
```

**Permanent (add to profile):**
```bash
# Linux/Mac: Add to ~/.bashrc or ~/.zshrc
echo 'export CF_API_TOKEN="your_token_here"' >> ~/.bashrc

# Windows: Use System Environment Variables
setx CF_API_TOKEN "your_token_here"
```

### Step 4: Add Domain to Cloudflare

Make sure your domain is added to Cloudflare and nameservers are configured.

### Step 5: Run Hostify

```python
from hostify import Host

Host(domain="app.yourdomain.com", port=3000).serve()
```

---

## 🎨 Live Demos

Check out these live examples hosted with hostify:

- **Static Site:** https://hostify.yaspik.tech
- **Flask App:** https://app.yaspik.tech

---

## 📚 API Reference

### `Host` Class

```python
Host(
    domain: str,           # Required: Full domain (e.g., "app.example.com")
    port: int = None,      # Port of existing server (mutually exclusive with path)
    path: str = None,      # Path to static files (mutually exclusive with port)
    api_token: str = None  # Optional: Cloudflare API token
)
```

**Methods:**
- `.serve()` - Start hosting (blocks until Ctrl+C)

**Parameters:**
- **domain** (required): Full domain or subdomain (e.g., "app.example.com")
- **port** (optional): Port number where your app is running (1-65535)
- **path** (optional): Path to directory with static files
- **api_token** (optional): Cloudflare API token (defaults to `CF_API_TOKEN` env var)

**Note:** You must specify either `port` OR `path`, not both.

---

## 🔍 How It Works

1. **Creates Cloudflare Tunnel** - Establishes secure connection
2. **Configures DNS** - Automatically creates CNAME record
3. **Routes Traffic** - Configures tunnel to route domain to your local server
4. **Manages Binary** - Downloads and runs cloudflared automatically
5. **Monitors Connection** - Auto-restarts on failures
6. **Cleans Up** - Removes all resources on Ctrl+C

---

## 🛠️ Troubleshooting

### "No server found on port X"
**Solution:** Make sure your application is running before starting hostify.

```bash
# Terminal 1: Start your app
python app.py

# Terminal 2: Host it
python host.py
```

### "Zone not found for domain"
**Solution:** Ensure your domain is added to Cloudflare and nameservers are configured.

### "No Cloudflare accounts found"
**Solution:** Check your API token has the correct permissions:
- Account → Cloudflare Tunnel → Edit
- Zone → DNS → Edit
- Zone → Zone → Read

### Site shows 404
**Solution:** Wait 30-60 seconds for tunnel to fully connect and DNS to propagate.

### "Cloudflare API token not found"
**Solution:** Set the `CF_API_TOKEN` environment variable or pass `api_token` parameter.

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
python tests/test_suite.py
```

Expected output:
```
Results: 9/9 tests passed (100%)
All tests passed! Library is ready for publication.
```

---

## 📁 Project Structure

```
hostify/
├── hostify/              # Main package
│   ├── __init__.py      # Package exports
│   ├── cloudflare.py    # Cloudflare API wrapper
│   ├── cloudflared.py   # Binary manager
│   ├── host.py          # Main Host class
│   └── utils.py         # Utilities
├── examples/            # Usage examples
├── tests/               # Test suite
└── docs/                # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built on [Cloudflare Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- Inspired by the need for simple, accessible hosting solutions

---

## 📞 Support

- **Documentation:** [Full Docs](INSTALL.md)
- **Issues:** [GitHub Issues](https://github.com/yuvrajarora1805/hostify/issues)
- **Cloudflare Setup:** [Setup Guide](CLOUDFLARE_SETUP.md)

---

## 🔮 Roadmap

- [ ] Multiple domain support
- [ ] Web dashboard for management
- [ ] Authentication system
- [ ] Custom cloudflared configuration
- [ ] Load balancing
- [ ] Health checks and monitoring
- [ ] CLI tool

---

**Made with ❤️ for developers who want to host from anywhere**

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=yuvrajarora1805/hostify&type=Date)](https://star-history.com/#yuvrajarora1805/hostify&Date)
