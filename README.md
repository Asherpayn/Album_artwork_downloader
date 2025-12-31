# Album Artwork Downloader

A program that allows you to download album artwork from Spotify, useful for adding artwork to mp3 files or albums on iPods.

**My attempt at vibe coding**
I created this as I needed to get album artwork for my iPod. iTunes does have a similar function but I only have a Windows XP laptop that isn't supported by Apple. So it *also* barely works.
The following text and code will be 90% Claude-Code and 10% me looking through and changing a few bits.

### Future features

- [x] Rearrange everything to look more nicer, over the current massive monolith
- [x] Add tests
- [ ] add batch downloading from a text file (one album per line)

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

The application now includes 58 tests:

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

The project uses **PyInstaller** to create standalone executable applications that can run without Python installed.

### Quick Build

```bash
# Run the build script (recommended)
./build.sh
```

The script will:
- Install PyInstaller if needed
- Clean previous builds
- Build the application bundle using the configured spec file
- Create a compressed `.tar.gz` archive for distribution
- Report file sizes and locations

### Manual Build

```bash
# Install PyInstaller
pip3 install pyinstaller

# Build using spec file
pyinstaller main.spec

# Application will be at: dist/AlbumArtworkDownloader/
```

### Running Locally

```bash
./dist/AlbumArtworkDownloader/AlbumArtworkDownloader
```
### Distribution

The build creates `dist/AlbumArtworkDownloader.tar.gz` with maximum compression.

**Installation (optional):**

Add the folder to your PATH for easy access from anywhere:

```bash
# Extract to wherever you want
tar -xzf AlbumArtworkDownloader.tar.gz
mv AlbumArtworkDownloader ~/Applications/  # or anywhere

# Add to PATH in ~/.zshrc
export PATH="$HOME/Applications/AlbumArtworkDownloader:$PATH"
```

Then run with just: `AlbumArtworkDownloader`
