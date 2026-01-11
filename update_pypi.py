"""
Update PyPI with new README changes
This creates a patch release (0.1.0 -> 0.1.1) with updated documentation
"""

import re
import subprocess

def update_version_in_file(filepath, old_version, new_version):
    """Update version in a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(old_version, new_version)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {filepath}")

def main():
    old_version = "0.1.0"
    new_version = "0.1.1"
    
    print("\n" + "="*60)
    print("  UPDATING PYPI WITH NEW README")
    print("="*60 + "\n")
    
    # Update version in files
    print("Updating version numbers...")
    update_version_in_file("pyproject.toml", old_version, new_version)
    update_version_in_file("setup.py", old_version, new_version)
    update_version_in_file("hostify/__init__.py", old_version, new_version)
    
    # Update CHANGELOG
    print("\nUpdating CHANGELOG...")
    with open("CHANGELOG.md", 'r', encoding='utf-8') as f:
        changelog = f.read()
    
    new_entry = f"""## [0.1.1] - 2026-01-11

### Changed
- Updated README with correct GitHub repository URLs
- Added Star History badge with correct username
- Updated all documentation links

---

"""
    
    changelog = changelog.replace("## [Unreleased]", f"## [Unreleased]\n\n---\n\n{new_entry}## [0.1.0] - 2026-01-11")
    
    with open("CHANGELOG.md", 'w', encoding='utf-8') as f:
        f.write(changelog)
    
    print("✓ Updated CHANGELOG.md")
    
    # Build package
    print("\nBuilding package...")
    subprocess.run(["python", "-m", "build"], check=True)
    
    print("\n" + "="*60)
    print("  READY TO UPLOAD")
    print("="*60)
    print("\nVersion updated to 0.1.1")
    print("\nTo upload to PyPI, run:")
    print("  twine upload dist/*")
    print("\nOr just press Enter to upload now...")
    
    choice = input().strip()
    
    if choice == "" or choice.lower() in ["y", "yes"]:
        print("\nUploading to PyPI...")
        subprocess.run(["twine", "upload", "dist/*"], check=True)
        print("\n✓ Successfully uploaded to PyPI!")
        print("View at: https://pypi.org/project/hostify/0.1.1/")
    else:
        print("\nSkipped upload. Run manually with: twine upload dist/*")

if __name__ == "__main__":
    main()
