import os
import requests
import json
from fuzzywuzzy import process
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
from io import BytesIO

# File path to store Spotify API credentials persistently
CREDENTIALS_FILE = os.path.expanduser("~/.spotify_credentials.json")

# Save Spotify API credentials to a file
def save_credentials(client_id, client_secret):
    credentials = {"client_id": client_id, "client_secret": client_secret}
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(credentials, f)

# Load Spotify API credentials from a file if available
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return None

# Retrieve Spotify API credentials, prompting the user if not saved
def get_spotify_credentials():
    creds = load_credentials()
    if creds:
        print("Using saved Spotify credentials.")
        return creds["client_id"], creds["client_secret"]
    
    client_id = input("Your Spotify Client ID: ")
    client_secret = input("Your Spotify Client Secret: ")
    save_credentials(client_id, client_secret)
    return client_id, client_secret

print("Welcome to Album Artwork Downloader!")
print("This program downloads the album artwork of a given album from Spotify.")
print("You can type 'exit' to quit the program at any time.")

# Get Spotify API credentials
SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET = get_spotify_credentials()

# Initialize Spotipy client
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Test if Spotify API credentials are valid by making a simple request
def test_credentials():
    try:
        sp.search(q="test", type="album", limit=1)
    except spotipy.exceptions.SpotifyException as e:
        print("Invalid Spotify credentials. Please check your Client ID and Client Secret.")

# Prompt user to choose an album from a list if multiple results are found
def choose_album(albums):
    if not albums:
        return None
    
    print("Multiple albums found:")
    for idx, album in enumerate(albums):
        print(f"{idx + 1}. {album['name']} by {album['artists'][0]['name']}")
    
    try:
        choice = int(input("Enter the number of the album you want to select: ")) - 1
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
    if album and album['images']:
        image_url = album['images'][0]['url']
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(save_path)
            print(f"Album artwork saved to {save_path}")
        else:
            print("Failed to download album artwork.")
    else:
        print("No album artwork found.")

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
        os.makedirs(albumartworks_dir)
        print(f"Created directory: {albumartworks_dir}")
    
    while True:
        album_name = input("Enter the album name (or type 'exit' to quit): ")
        if album_name.lower() == 'exit':
            print("Exiting the program.")
            break

        album = find_closest_album(album_name)
        if album:
            print(f"Selected album: {album['name']} by {album['artists'][0]['name']}")
            safe_album_name = sanitize_filename(album['name'])
            save_path = os.path.expanduser(f"~/Pictures/albumartworks/{safe_album_name}.jpg")
            download_album_artwork(album, save_path)
        else:
            print("No matching album found.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the program.")
