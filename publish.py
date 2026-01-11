"""
Quick Publish Script for Hostify

This script automates the process of building and publishing to PyPI.
Run this after you've made changes and are ready to publish a new version.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"\n[ERROR] {description} failed!")
        return False
    
    print(f"\n[SUCCESS] {description} completed!")
    return True

def main():
    print("\n" + "="*60)
    print("  HOSTIFY - QUICK PUBLISH SCRIPT")
    print("="*60)
    
    # Step 1: Run tests
    if not run_command("python tests/test_suite.py", "Running Tests"):
        print("\n[ABORT] Tests failed. Fix issues before publishing.")
        return False
    
    # Step 2: Clean old builds
    print("\n[INFO] Cleaning old builds...")
    if os.path.exists("dist"):
        import shutil
        shutil.rmtree("dist")
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")
    
    # Step 3: Build package
    if not run_command("python -m build", "Building Package"):
        return False
    
    # Step 4: Check package
    if not run_command("twine check dist/*", "Checking Package"):
        print("\n[WARN] Package check had warnings. Review before uploading.")
    
    # Step 5: Ask for confirmation
    print("\n" + "="*60)
    print("  READY TO PUBLISH")
    print("="*60)
    print("\nPackage built successfully!")
    print("\nOptions:")
    print("  1. Upload to TestPyPI (recommended first)")
    print("  2. Upload to PyPI (production)")
    print("  3. Cancel")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        print("\n[INFO] Uploading to TestPyPI...")
        if run_command("twine upload --repository testpypi dist/*", "Upload to TestPyPI"):
            print("\n[SUCCESS] Uploaded to TestPyPI!")
            print("Test installation with:")
            print("  pip install --index-url https://test.pypi.org/simple/ hostify")
    
    elif choice == "2":
        confirm = input("\n[WARN] Upload to PyPI? This cannot be undone! (yes/no): ").strip().lower()
        if confirm == "yes":
            if run_command("twine upload dist/*", "Upload to PyPI"):
                print("\n[SUCCESS] Published to PyPI!")
                print("Install with: pip install hostify")
                print("View at: https://pypi.org/project/hostify/")
        else:
            print("\n[CANCEL] Upload cancelled.")
    
    else:
        print("\n[CANCEL] Publishing cancelled.")
    
    print("\n" + "="*60)
    print("  DONE")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Check if required tools are installed
    try:
        import build
        import twine
    except ImportError:
        print("\n[ERROR] Required tools not installed!")
        print("Install with: pip install build twine")
        sys.exit(1)
    
    main()
