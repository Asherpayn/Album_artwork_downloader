"""
Album Artwork Downloader - Build Instructions

This project uses PyInstaller to create a standalone executable.

To build the executable:
    1. Install PyInstaller: pip install pyinstaller
    2. Run the build script: ./build.sh

    Or manually: pyinstaller main.spec

The executable will be created at: dist/AlbumArtworkDownloader

To run:
    ./dist/AlbumArtworkDownloader

Configuration:
    - Entry point: app.py
    - Spec file: main.spec
    - Icon: icon.icon
    - Dependencies: See requirements.txt

For development:
    pip install -r requirements.txt
    python app.py
"""

# This file is kept for reference but py2app has been replaced with PyInstaller
# See main.spec for the PyInstaller configuration
