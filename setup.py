from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hostify",
    version="0.2.0",
    author="Yuvraj Arora",
    author_email="yuvrajaroraw18@gmail.com",
    description="Effortless application hosting using Cloudflare Tunnels.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuvrajarora1805/hostify",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "hostify=hostify.cli:main",
        ],
    },
)
