"""
Setup configuration for NHL API Client package
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nhl-stats-api-client",
    version="1.0.3",
    author="Mikhail Korotkov",
    author_email="ma.korotkov.eu@gmail.com",
    description="A comprehensive Python client for accessing NHL statistics and data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liahimratman/nhl-api-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="nhl hockey api statistics sports analytics",
    project_urls={
        "Bug Reports": "https://github.com/liahimratman/nhl-api-client/issues",
        "Source": "https://github.com/liahimratman/nhl-api-client",
        "Documentation": "https://github.com/liahimratman/nhl-api-client#readme",
    },
    include_package_data=True,
    package_data={
        "nhl_api_client": ["*.md", "*.txt"],
    },
) 