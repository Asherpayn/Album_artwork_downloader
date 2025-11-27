import json
import os
from io import BytesIO

import requests
import spotipy
from PIL import Image
from spotipy.oauth2 import SpotifyClientCredentials

# ANSI escape codes for color formatting
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# File path to store Spotify API credentials persistently
CREDENTIALS_FILE = os.path.expanduser("~/.spotify_credentials.json")


# Save Spotify API credentials to a file
def save_credentials(client_id, client_secret):
    if not client_id or not client_secret:
        print(RED + "Error: Client ID and Client Secret cannot be empty." + RESET)
        return False
    credentials = {"client_id": client_id, "client_secret": client_secret}
    try:
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials, f)
        return True
    except IOError as e:
        print(RED + f"Error: Cannot save credentials: {e}" + RESET)
        return False


# Load Spotify API credentials from a file if available
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(YELLOW + "Warning: Corrupted credentials file. Please re-enter your credentials." + RESET)
            return None
        except IOError as e:
            print(YELLOW + f"Warning: Cannot read credentials file: {e}" + RESET)
            return None
    return None


# Retrieve Spotify API credentials, prompting the user if not saved
def get_spotify_credentials():
    creds = load_credentials()
    if creds:
        print("Using saved Spotify credentials.")
        return creds["client_id"], creds["client_secret"]

    while True:
        client_id = input(GREEN + "Your Spotify Client ID: " + RESET).strip()
        client_secret = input(GREEN + "Your Spotify Client Secret: " + RESET).strip()
        if save_credentials(client_id, client_secret):
            return client_id, client_secret


print("Welcome to Album Artwork Downloader!")
print("This program downloads the album artwork of a given album from Spotify.")
print("You can type 'exit' to quit the program at any time.")

# Get Spotify API credentials
SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET = get_spotify_credentials()

# Test if Spotify API credentials are valid by making a simple request
def test_credentials(sp):
    try:
        sp.search(q="test", type="album", limit=1)
        return True
    except spotipy.exceptions.SpotifyException:
        print(RED + "Invalid Spotify credentials. Please check your Client ID and Client Secret." + RESET)
        return False


# Initialize Spotipy client
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Validate credentials immediately
if not test_credentials(sp):
    print("Exiting due to invalid credentials.")
    exit(1)


# Prompt user to choose an album from a list if multiple results are found
def choose_album(albums):
    if not albums:
        return None

    print("Multiple albums found:")
    for idx, album in enumerate(albums):
        color = RED if idx < 10 else RESET
        artist_name = album['artists'][0]['name'] if album.get('artists') else "Unknown Artist"
        print(color + f"{idx + 1}. {album['name']} by {artist_name}" + RESET)

    try:
        choice = int(input(GREEN + "Enter the number of the album you want to select: " + RESET)) - 1
        if 0 <= choice < len(albums):
            return albums[choice]
    except ValueError:
        pass

    print("Invalid choice. Defaulting to the first album.")
    return albums[0]


# Search Spotify for an album matching the provided name
def find_closest_album(album_name):
    results = sp.search(q=album_name, type='album', limit=10)
    albums = results['albums']['items']
    return choose_album(albums)


# Download and save the album artwork to the specified location
def download_album_artwork(album, save_path):
    if not album or not album.get('images'):
        print("No album artwork found.")
        return

    image_url = album['images'][0]['url']
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        try:
            img = Image.open(BytesIO(response.content))
            img.save(save_path)
            print(f"Album artwork saved to {save_path}")
        except Exception as e:
            print(RED + f"Error: Failed to process image: {e}" + RESET)
    except requests.exceptions.Timeout:
        print(RED + "Error: Download timed out. Please check your internet connection." + RESET)
    except requests.exceptions.ConnectionError:
        print(RED + "Error: Connection failed. Please check your internet connection." + RESET)
    except requests.exceptions.RequestException as e:
        print(RED + f"Error: Failed to download album artwork: {e}" + RESET)


# Sanitize a filename by replacing invalid characters
def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


# Main program loop that prompts the user for album names and downloads artwork
def main():
    albumartworks_dir = os.path.expanduser("~/Pictures/albumartworks")
    if not os.path.exists(albumartworks_dir):
        try:
            os.makedirs(albumartworks_dir)
            print(f"Created directory: {albumartworks_dir}")
        except OSError as e:
            print(RED + f"Error: Unable to create directory {albumartworks_dir}: {e}" + RESET)
            return

    while True:
        album_name = input(GREEN + "Enter the album name (or type 'exit' to quit): " + RESET).strip()
        if album_name.lower() == 'exit':
            print("Exiting the program.")
            break

        if not album_name:
            print("Please enter a valid album name.")
            continue

        album = find_closest_album(album_name)
        if album:
            artist_name = album['artists'][0]['name'] if album.get('artists') else "Unknown Artist"
            print(f"Selected album: {album['name']} by {artist_name}")
            safe_album_name = sanitize_filename(album['name'])
            save_path = os.path.join(albumartworks_dir, f"{safe_album_name}.jpg")
            download_album_artwork(album, save_path)
        else:
            print("No matching album found.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the program.")
