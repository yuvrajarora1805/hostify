# Complete Setup and Publication Guide

This guide walks you through the entire process from installation to publishing your own hostify-powered application.

---

## 📋 Table of Contents

1. [Initial Setup](#initial-setup)
2. [Creating Your First App](#creating-your-first-app)
3. [Publishing to PyPI](#publishing-to-pypi)
4. [GitHub Setup](#github-setup)
5. [Advanced Configuration](#advanced-configuration)

---

## 1. Initial Setup

### Prerequisites

- Python 3.9 or higher
- Cloudflare account
- Domain added to Cloudflare

### Step 1.1: Install Hostify

```bash
pip install hostify
```

Or install from source:
```bash
git clone https://github.com/yourusername/hostify.git
cd hostify
pip install -e .
```

### Step 1.2: Create Cloudflare API Token

1. **Go to Cloudflare Dashboard**
   - Visit: https://dash.cloudflare.com/profile/api-tokens
   - Click "Create Token"

2. **Use Template or Create Custom**
   - **Option A:** Use "Edit Cloudflare Zero Trust" template
   - **Option B:** Create custom token with these permissions:
     - Account → Cloudflare Tunnel → Edit
     - Zone → DNS → Edit
     - Zone → Zone → Read

3. **Configure Resources**
   - Account Resources: Include → All accounts
   - Zone Resources: Include → All zones (or specific domain)

4. **Create and Copy Token**
   - Click "Continue to summary"
   - Click "Create Token"
   - **COPY THE TOKEN** (you won't see it again!)

### Step 1.3: Set Environment Variable

**Windows (PowerShell):**
```powershell
# Temporary (current session)
$env:CF_API_TOKEN="your_token_here"

# Permanent (system-wide)
setx CF_API_TOKEN "your_token_here"
```

**Linux/Mac:**
```bash
# Temporary (current session)
export CF_API_TOKEN="your_token_here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export CF_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 1.4: Verify Installation

```python
from hostify import Host
print("Hostify installed successfully!")
```

---

## 2. Creating Your First App

### Example 1: Static Website

**Step 2.1:** Create your website
```bash
mkdir my-website
cd my-website
echo "<h1>Hello World!</h1>" > index.html
```

**Step 2.2:** Create hosting script
```python
# host.py
from hostify import Host

Host(
    domain="mysite.yourdomain.com",
    path="."
).serve()
```

**Step 2.3:** Run it
```bash
python host.py
```

Your site is now live at `https://mysite.yourdomain.com`!

### Example 2: Flask Application

**Step 2.1:** Create Flask app
```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>My Flask App</h1>"

if __name__ == '__main__':
    app.run(port=5000)
```

**Step 2.2:** Create hosting script
```python
# host.py
from hostify import Host

Host(
    domain="flask.yourdomain.com",
    port=5000
).serve()
```

**Step 2.3:** Run both
```bash
# Terminal 1
python app.py

# Terminal 2
python host.py
```

Your Flask app is now live at `https://flask.yourdomain.com`!

---

## 3. Publishing to PyPI

If you want to publish your own library based on hostify or contribute to hostify itself:

### Step 3.1: Prepare Your Package

Ensure you have these files:
- `setup.py` or `pyproject.toml`
- `README.md`
- `LICENSE`
- `requirements.txt`
- `MANIFEST.in`

### Step 3.2: Install Build Tools

```bash
pip install build twine
```

### Step 3.3: Build Distribution

```bash
python -m build
```

This creates:
- `dist/hostify-0.1.0.tar.gz` (source)
- `dist/hostify-0.1.0-py3-none-any.whl` (wheel)

### Step 3.4: Test Locally

```bash
pip install dist/hostify-0.1.0-py3-none-any.whl
```

### Step 3.5: Upload to TestPyPI (Optional)

```bash
# Register at https://test.pypi.org
twine upload --repository testpypi dist/*
```

Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ hostify
```

### Step 3.6: Upload to PyPI

```bash
# Register at https://pypi.org
twine upload dist/*
```

Enter your PyPI username and password (or API token).

### Step 3.7: Verify Publication

```bash
pip install hostify
```

Check: https://pypi.org/project/hostify/

---

## 4. GitHub Setup

### Step 4.1: Initialize Git Repository

```bash
cd hostify
git init
git add .
git commit -m "Initial commit"
```

### Step 4.2: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named "hostify"
3. Don't initialize with README (you already have one)

### Step 4.3: Push to GitHub

```bash
git remote add origin https://github.com/yourusername/hostify.git
git branch -M main
git push -u origin main
```

### Step 4.4: Add GitHub Actions (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest
    - name: Run tests
      run: python tests/test_suite.py
```

---

## 5. Advanced Configuration

### Using Configuration File

Create `hostify.yaml`:
```yaml
domain: app.example.com
port: 3000
api_token: ${CF_API_TOKEN}
```

Load in Python:
```python
import yaml
from hostify import Host

with open('hostify.yaml') as f:
    config = yaml.safe_load(f)

Host(**config).serve()
```

### Multiple Domains

Host multiple apps:
```python
import threading
from hostify import Host

def host_app1():
    Host(domain="app1.example.com", port=3000).serve()

def host_app2():
    Host(domain="app2.example.com", port=4000).serve()

# Run in threads
t1 = threading.Thread(target=host_app1)
t2 = threading.Thread(target=host_app2)

t1.start()
t2.start()

t1.join()
t2.join()
```

### Custom Error Handling

```python
from hostify import Host, HostError

try:
    Host(domain="app.example.com", port=3000).serve()
except HostError as e:
    print(f"Hosting failed: {e}")
    # Send alert, log error, etc.
except KeyboardInterrupt:
    print("Shutting down gracefully...")
```

### Logging

```python
import logging
from hostify import Host

logging.basicConfig(level=logging.INFO)

Host(domain="app.example.com", port=3000).serve()
```

---

## 🎯 Quick Reference

### Common Commands

```bash
# Install
pip install hostify

# Build package
python -m build

# Run tests
python tests/test_suite.py

# Upload to PyPI
twine upload dist/*

# Install from source
pip install -e .
```

### Environment Variables

```bash
CF_API_TOKEN          # Cloudflare API token (required)
```

### File Structure

```
your-project/
├── app.py           # Your application
├── host.py          # Hostify script
├── requirements.txt # Dependencies
└── README.md        # Documentation
```

---

## 🆘 Getting Help

- **Documentation:** [README.md](README.md)
- **API Token Setup:** [CLOUDFLARE_SETUP.md](CLOUDFLARE_SETUP.md)
- **Installation Guide:** [INSTALL.md](INSTALL.md)
- **Publishing Guide:** [PUBLISHING.md](PUBLISHING.md)
- **Issues:** https://github.com/yourusername/hostify/issues

---

## ✅ Checklist

Before going live:

- [ ] Python >= 3.9 installed
- [ ] Cloudflare account created
- [ ] Domain added to Cloudflare
- [ ] API token created with correct permissions
- [ ] CF_API_TOKEN environment variable set
- [ ] Hostify installed (`pip install hostify`)
- [ ] Application tested locally
- [ ] Domain configured in script
- [ ] Script runs without errors

---

**You're all set! Happy hosting! 🚀**
