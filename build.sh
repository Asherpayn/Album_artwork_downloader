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
if [ -d "dist/AlbumArtworkDownloader" ]; then
    echo "✅ Build successful!"
    echo "📍 Application location: dist/AlbumArtworkDownloader/"
    echo ""

    # Create compressed tarball for distribution
    echo "🗜️  Creating compressed distribution archive (max compression)..."
    cd dist
    GZIP=-9 tar -czf AlbumArtworkDownloader.tar.gz AlbumArtworkDownloader/
    cd ..

    # Show file size
    SIZE=$(du -h dist/AlbumArtworkDownloader.tar.gz | cut -f1)
    echo "✅ Distribution archive created: dist/AlbumArtworkDownloader.tar.gz ($SIZE)"
    echo ""
    echo "To run locally:"
    echo "  ./dist/AlbumArtworkDownloader/AlbumArtworkDownloader"
    echo ""
    echo "To distribute:"
    echo "  Share dist/AlbumArtworkDownloader.tar.gz"
    echo "  Recipients extract with: tar -xzf AlbumArtworkDownloader.tar.gz"
else
    echo "❌ Build failed!"
    exit 1
fi
