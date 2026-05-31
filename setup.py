from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="timetrack-cli",
    version="1.0.0",
    author="TimeTrack Team",
    author_email="contact@timetrack.dev",
    description="A powerful command-line time tracking tool for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/timetrack-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Scheduling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "tabulate>=0.9.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "timetrack=timetrack.cli:main",
            "tt=timetrack.cli:main",
        ],
    },
)
