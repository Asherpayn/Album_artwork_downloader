#!/bin/bash
# Build script for Album Artwork Downloader using PyInstaller

set -e  # Exit on error

echo "🔨 Building Album Artwork Downloader..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the executable using the spec file
echo "📦 Building executable..."
pyinstaller main.spec

# Check if build was successful
if [ -f "dist/AlbumArtworkDownloader" ]; then
    echo "✅ Build successful!"
    echo "📍 Executable location: dist/AlbumArtworkDownloader"
    echo ""
    echo "To run the application:"
    echo "  ./dist/AlbumArtworkDownloader"
else
    echo "❌ Build failed!"
    exit 1
fi
