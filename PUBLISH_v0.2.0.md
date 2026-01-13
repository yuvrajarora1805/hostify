# Publishing Hostify v0.2.0 to PyPI

## ✅ Completed Steps

1. ✅ All code changes committed
2. ✅ Version updated to 0.2.0 in all files
3. ✅ Git tag v0.2.0 created
4. ✅ Pushed to GitHub: https://github.com/yuvrajarora1805/hostify
5. ✅ Package built successfully (`python -m build`)

## 🔄 Next Step: Upload to PyPI

### Option 1: Manual Upload (Recommended)

Run this command and enter your PyPI API token when prompted:

```bash
python -m twine upload dist/hostify-0.2.0*
```

**Where to get PyPI API token:**
1. Go to https://pypi.org/manage/account/token/
2. Create a new API token (if you don't have one)
3. Copy the token (starts with `pypi-`)
4. Paste it when prompted by twine

### Option 2: Using .pypirc File

Create a file at `~/.pypirc` (or `%USERPROFILE%\.pypirc` on Windows):

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Then run:
```bash
python -m twine upload dist/hostify-0.2.0*
```

### Option 3: Using Environment Variable

```powershell
# Windows PowerShell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-YOUR_TOKEN_HERE"
python -m twine upload dist/hostify-0.2.0*
```

```bash
# Linux/macOS
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
python -m twine upload dist/hostify-0.2.0*
```

---

## 📦 What Will Be Published

- **Package Name**: hostify
- **Version**: 0.2.0
- **Files**:
  - `hostify-0.2.0.tar.gz` (source distribution)
  - `hostify-0.2.0-py3-none-any.whl` (wheel distribution)

---

## ✅ After Publishing

1. Verify on PyPI: https://pypi.org/project/hostify/
2. Test installation:
   ```bash
   pip install hostify==0.2.0
   hostify version
   ```

3. Create GitHub Release:
   - Go to https://github.com/yuvrajarora1805/hostify/releases
   - Click "Draft a new release"
   - Choose tag: v0.2.0
   - Title: "v0.2.0 - CLI Tool Release"
   - Description: Copy from CHANGELOG.md

---

## 🎉 Release Checklist

- [x] Code committed
- [x] Version bumped to 0.2.0
- [x] CHANGELOG updated
- [x] Git tag created
- [x] Pushed to GitHub
- [x] Package built
- [ ] **Uploaded to PyPI** ← YOU ARE HERE
- [ ] GitHub Release created
- [ ] Verified installation

---

## 🚀 Quick Command

If you have your PyPI token ready, just run:

```bash
python -m twine upload dist/hostify-0.2.0*
```

And paste your token when prompted!
