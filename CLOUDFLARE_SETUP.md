# Cloudflare API Token Setup Guide

This guide walks you through creating a Cloudflare API token for hostify.

## Prerequisites

- A Cloudflare account (free tier works!)
- A domain added to Cloudflare

## Step-by-Step Instructions

### 1. Log in to Cloudflare

Go to [https://dash.cloudflare.com](https://dash.cloudflare.com) and log in.

### 2. Navigate to API Tokens

1. Click on your profile icon (top right)
2. Select **"My Profile"**
3. Click on **"API Tokens"** in the left sidebar
4. Click **"Create Token"**

### 3. Create Custom Token

1. Click **"Create Custom Token"** (at the bottom)
2. Give it a name: `Hostify Token`

### 4. Set Permissions

Add the following permissions:

| Section | Subsection | Permission |
|---------|------------|------------|
| **Account** | Cloudflare Tunnel | **Edit** |
| **Zone** | DNS | **Edit** |
| **Zone** | Zone | **Read** |

**Important**: Make sure to select the correct account and zone resources!

### 5. Configure Resources

- **Account Resources**: Select your account
- **Zone Resources**: 
  - Either select "All zones" 
  - Or select specific zones you want to use

### 6. Optional: Set IP Filtering

For extra security, you can restrict the token to specific IP addresses.
- Leave blank to allow from any IP (recommended for home use)

### 7. Create and Copy Token

1. Click **"Continue to summary"**
2. Review the permissions
3. Click **"Create Token"**
4. **IMPORTANT**: Copy the token immediately - you won't see it again!

### 8. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:CF_API_TOKEN="your_token_here"
```

To make it permanent:
```powershell
[System.Environment]::SetEnvironmentVariable('CF_API_TOKEN', 'your_token_here', 'User')
```

**Linux/Mac (Bash):**
```bash
export CF_API_TOKEN="your_token_here"
```

To make it permanent, add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export CF_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### 9. Verify Token

Test your token with this Python script:

```python
from hostify.cloudflare import Cloudflare

try:
    cf = Cloudflare()
    account_id = cf.get_account_id()
    print(f"✓ Token works! Account ID: {account_id}")
except Exception as e:
    print(f"✗ Token error: {e}")
```

## Troubleshooting

### "API token not found"

Make sure you've set the environment variable:
```bash
# Check if it's set (Linux/Mac)
echo $CF_API_TOKEN

# Check if it's set (Windows PowerShell)
echo $env:CF_API_TOKEN
```

### "Insufficient permissions"

Go back to the API token page and verify all three permissions are set:
- Account → Cloudflare Tunnel → Edit
- Zone → DNS → Edit  
- Zone → Zone → Read

### "Zone not found"

Make sure your domain is added to Cloudflare:
1. Go to Cloudflare Dashboard
2. Click "Add a Site"
3. Follow the instructions to add your domain
4. Update nameservers at your domain registrar

## Security Best Practices

1. **Never commit tokens to git** - they're in `.gitignore` by default
2. **Use environment variables** - don't hardcode tokens in scripts
3. **Rotate tokens periodically** - create new tokens every few months
4. **Use minimal permissions** - only grant what's needed
5. **Set IP restrictions** - if you have a static IP

## Need Help?

- [Cloudflare API Tokens Documentation](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [Cloudflare Tunnels Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
