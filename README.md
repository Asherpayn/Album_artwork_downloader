# Album Artwork Downloader

A program that allows you to download album artwork from Spotify, useful for adding artwork to mp3 files or albums on iPods.

**my attempt at "vibe coding"**
I created this as I needed to get album artwork for my iPod. iTunes does have a similar function but I only have a Windows XP laptop that isn't supported by Apple. So it *also* barely works.

## Quick Start

### Installation

```bash
# Install required dependencies
pip3 install -r requirements.txt
```

**Required Python packages:**
- `spotipy>=2.22.0` - for interacting with the Spotify API
- `requests>=2.28.0` - for making HTTP requests
- `Pillow>=9.0.0` - for image processing

**Optional (for testing):**
- `pytest>=7.0.0` - test runner
- `pytest-cov>=4.0.0` - test coverage reports

### Spotify API Setup

You will need a Spotify account and API credentials:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create an App"
3. Fill in the details:
   - **App Name**: "Album Artwork Downloader" (or your choice)
   - **Redirect URI**: `http://localhost:8080/callback` (required but unused)
4. Click "Create"
5. On the app dashboard, copy your:
   - **Client ID**: A unique identifier for your app
   - **Client Secret**: A secret key for authentication

### Running the Application

```bash
python3 app.py
```

On first run, you'll be prompted to enter your Spotify credentials. They'll be saved to `~/.spotify_credentials.json` for future use.

## Testing

The application now includes a comprehensive test suite with 58 tests:

```bash
# Run all tests
python3 -m unittest discover tests -v

# Run specific test modules
python3 -m unittest tests.test_output -v
python3 -m unittest tests.test_config -v
python3 -m unittest tests.test_spotify_client -v
python3 -m unittest tests.test_album_service -v
python3 -m unittest tests.test_app -v
python3 -m unittest tests.test_integration -v

# Using pytest (optional, requires installation)
pytest tests/ -v

# Generate coverage report
pytest tests/ --cov=. --cov-report=html
```

**Expected result**: All 58 tests pass in ~0.02 seconds

## Building Executables

The project uses **PyInstaller** to create standalone executable binaries that can run without Python installed.

### Quick Build

```bash
# Run the build script (recommended)
./build.sh
```

The script will:
- Install PyInstaller if needed
- Clean previous builds
- Build the executable using the configured spec file
- Report the output location

### Manual Build

```bash
# Install PyInstaller
pip3 install pyinstaller

# Build using spec file
pyinstaller main.spec

# Executable will be at: dist/AlbumArtworkDownloader
```

### Running the Executable

```bash
./dist/AlbumArtworkDownloader
```

The executable is a single binary file that includes all dependencies (spotipy, requests, Pillow) - no Python installation required on the target machine!

### Build Configuration

- **Entry point**: `app.py`
- **Spec file**: `main.spec` (PyInstaller configuration)
- **Output name**: `AlbumArtworkDownloader`
- **Icon**: `icon.icon`
- **Build artifacts**: `build/` and `dist/` directories

## Architecture

The application has been refactored into a modular architecture:

- **app.py** - Main application orchestration and entry point
- **config.py** - Configuration and credentials management
- **output.py** - Console output utilities
- **spotify_client.py** - Spotify API wrapper
- **album_service.py** - Business logic services
- **tests/** - Comprehensive test suite (58 tests)

For detailed refactoring documentation, see [README_REFACTORING.md](README_REFACTORING.md)

## Programmatic Usage

You can now use the application as a library:

```python
from app import AlbumArtworkApp
from output import ConsoleOutput
from config import CredentialsManager

# Create app instance
output = ConsoleOutput()
creds_manager = CredentialsManager()
app = AlbumArtworkApp(output, creds_manager)

# Search and download
album = app.find_and_select_album("Abbey Road")
if album:
    app.download_album_artwork(album)
```
