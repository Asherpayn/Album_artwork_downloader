import os
import requests
from fuzzywuzzy import process
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
from io import BytesIO

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

print("Welcome to Album Artwork Downloader!")
print("This program downloads the album artwork of a given album from Spotify.")
print("You can type 'exit' to quit the program at any time.")
print("Please enter the name of the album you'd like to download the artwork for:")

# Spotify API credentials
SPOTIPY_CLIENT_ID = input(GREEN + "Your spotify client id: " + RESET)
SPOTIPY_CLIENT_SECRET = input(GREEN + "Your spotify client secret: " + RESET)

# Initialize Spotipy client
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Test the credentials
def test_credentials():
    try:
        sp.search(q="test", type="album", limit=1)  # Test the credentials
    except spotipy.exceptions.SpotifyException as e:
        print("Invalid Spotify credentials. Please check your Client ID and Client Secret.")
    return

def choose_album(albums):
    if not albums:
        return None
    
    print("Multiple albums found:")
    for idx, album in enumerate(albums):
        print(RED + f"{idx + 1}. {album['name']} by {album['artists'][0]['name']}" + RESET)
    
    try:
        choice = int(input(GREEN + "Enter the number of the album you want to select: " + RESET)) - 1
        if 0 <= choice < len(albums):
            return albums[choice]
    except ValueError:
        pass
    
    print("Invalid choice. Defaulting to the first album.")
    return albums[0]

def find_closest_album(album_name):
    results = sp.search(q=album_name, type='album', limit=10)
    albums = results['albums']['items']
    return choose_album(albums)

def download_album_artwork(album, save_path):
    if album and album['images']:
        image_url = album['images'][0]['url']  # Get the highest resolution image
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(save_path)
            print(f"Album artwork saved to {save_path}")
        else:
            print("Failed to download album artwork.")
    else:
        print("No album artwork found.")

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def main():
    albumartworks_dir = os.path.expanduser("~/Pictures/albumartworks")
    if not os.path.exists(albumartworks_dir):
        os.makedirs(albumartworks_dir)
        print(f"Created directory: {albumartworks_dir}")
    
    while True:
        album_name = input(GREEN + "Enter the album name (or type 'exit' to quit): " + RESET)
        if album_name.lower() == 'exit':
            print("Exiting the program.")
            break

        album = find_closest_album(album_name)
        if album:
            print(f"Selected album: {album['name']} by {album['artists'][0]['name']}")
            # Sanitize the album name to create a safe filename
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
