"""Main application orchestration."""
import sys
import os
from typing import Optional
from config import CredentialsManager, ALBUM_ARTWORKS_DIR, SEARCH_LIMIT
from output import ConsoleOutput
from spotify_client import SpotifyClient
from album_service import AlbumSelector, AlbumDownloader, FilenameUtil


class AlbumArtworkApp:
    """Main application class orchestrating all components."""

    def __init__(self,
                 output: ConsoleOutput,
                 credentials_manager: CredentialsManager,
                 spotify_client: Optional[SpotifyClient] = None,
                 album_selector: Optional[AlbumSelector] = None,
                 album_downloader: Optional[AlbumDownloader] = None,
                 artworks_dir: str = ALBUM_ARTWORKS_DIR):
        """
        Initialize application with dependencies.

        Args:
            output: Console output handler
            credentials_manager: Credentials manager
            spotify_client: Spotify client (will be created if None)
            album_selector: Album selector (will be created if None)
            album_downloader: Album downloader (will be created if None)
            artworks_dir: Directory to save album artworks
        """
        self.output = output
        self.credentials_manager = credentials_manager
        self.artworks_dir = artworks_dir

        # Initialize Spotify client if not provided
        if spotify_client is None:
            client_id, client_secret = credentials_manager.get_or_prompt(output)
            spotify_client = SpotifyClient(client_id, client_secret)

            if not spotify_client.test_credentials():
                output.error(
                    "Invalid Spotify credentials. "
                    "Please check your Client ID and Client Secret."
                )
                raise ValueError("Invalid Spotify credentials")

        self.spotify_client = spotify_client
        self.album_selector = album_selector or AlbumSelector(output)
        self.album_downloader = album_downloader or AlbumDownloader(output)

    def find_and_select_album(self, album_name: str) -> Optional[dict]:
        """
        Search for and select an album.

        Args:
            album_name: Name of album to search for

        Returns:
            Selected album dictionary or None
        """
        albums = self.spotify_client.search_albums(album_name, limit=SEARCH_LIMIT)
        return self.album_selector.choose_from_list(
            albums,
            self.spotify_client.get_artist_name
        )

    def download_album_artwork(self, album: dict) -> bool:
        """
        Download artwork for an album.

        Args:
            album: Album dictionary from Spotify

        Returns:
            True if download successful, False otherwise
        """
        image_url = self.spotify_client.get_album_image_url(album)
        if not image_url:
            self.output.info("No album artwork found.")
            return False

        artist_name = self.spotify_client.get_artist_name(album)
        self.output.info(f"Selected album: {album['name']} by {artist_name}")

        safe_album_name = FilenameUtil.sanitize(album['name'])
        save_path = os.path.join(self.artworks_dir, f"{safe_album_name}.jpg")

        return self.album_downloader.download(image_url, save_path)

    def run(self):
        """Run the main application loop."""
        self.output.info("Welcome to Album Artwork Downloader!")
        self.output.info(
            "This program downloads the album artwork of a given album from Spotify."
        )
        self.output.info("You can type 'exit' to quit the program at any time.")

        # Ensure output directory exists
        if not FilenameUtil.ensure_directory(self.artworks_dir, self.output):
            return

        while True:
            album_name = self.output.prompt(
                "Enter the album name (or type 'exit' to quit): "
            ).strip()

            if album_name.lower() == 'exit':
                self.output.info("Exiting the program.")
                break

            if not album_name:
                self.output.info("Please enter a valid album name.")
                continue

            album = self.find_and_select_album(album_name)
            if album:
                self.download_album_artwork(album)
            else:
                self.output.info("No matching album found.")


def main():
    """Entry point for the application."""
    output = ConsoleOutput()
    credentials_manager = CredentialsManager()

    try:
        app = AlbumArtworkApp(output, credentials_manager)
        app.run()
    except ValueError:
        # Invalid credentials already reported
        sys.exit(1)
    except KeyboardInterrupt:
        output.info("\nExiting the program.")
        sys.exit(0)


if __name__ == "__main__":
    main()
