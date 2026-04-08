#!/usr/bin/env python
"""Setup script for multi-agent-task-system"""

from setuptools import setup, find_packages

setup(
    name="multi-agent-task-system",
    version="1.0.0",
    description="Multi-agent AI system for task management on Google Cloud",
    author="Multi-Agent Team",
    author_email="support@example.com",
    url="https://github.com/yourusername/multi-agent-task-system",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic==2.5.0",
        "google-cloud-firestore==2.13.0",
        "google-cloud-storage==2.10.0",
        "google-auth==2.25.0",
        "anthropic==0.10.0",
        "pydantic-settings==2.1.0",
        "python-dotenv==1.0.0",
        "httpx==0.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    zip_safe=False,
)
