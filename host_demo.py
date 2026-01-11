"""
Host the Hostify demo site on hostify.yaspik.tech

This script demonstrates hosting a static website using hostify.
"""

from hostify import Host

print("=" * 60)
print("  Hosting Hostify Demo Site")
print("=" * 60)
print()
print("Domain: hostify.yaspik.tech")
print("Path:   ./demo_site")
print()
print("Starting hostify...")
print()

# Host the demo site
Host(
    domain="hostify.yaspik.tech",
    path="./demo_site"
).serve()
