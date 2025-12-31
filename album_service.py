"""Album selection and download services."""
import os
import requests
from PIL import Image
from io import BytesIO
from typing import Optional, List, Dict, Any, Callable


class AlbumSelector:
    """Handles album selection from search results."""

    def __init__(self, output, input_fn=input):
        """
        Initialize album selector.

        Args:
            output: ConsoleOutput instance
            input_fn: Input function (for testing, default: built-in input)
        """
        self.output = output
        self.input_fn = input_fn

    def choose_from_list(self, albums: List[Dict[str, Any]],
                        get_artist_name: Callable) -> Optional[Dict[str, Any]]:
        """
        Prompt user to choose an album from a list.

        Args:
            albums: List of album dictionaries
            get_artist_name: Function to extract artist name from album

        Returns:
            Selected album or None if no albums provided
        """
        if not albums:
            return None

        self.output.info("Multiple albums found:")
        from output import RED, RESET
        for idx, album in enumerate(albums):
            color = RED if idx < 10 else RESET
            artist_name = get_artist_name(album)
            self.output._print(
                f"{color}{idx + 1}. {album['name']} by {artist_name}{RESET}"
            )

        try:
            choice_str = self.output.prompt(
                "Enter the number of the album you want to select: "
            )
            choice = int(choice_str) - 1
            if 0 <= choice < len(albums):
                return albums[choice]
        except ValueError:
            pass

        self.output.info("Invalid choice. Defaulting to the first album.")
        return albums[0]


class AlbumDownloader:
    """Handles album artwork download operations."""

    def __init__(self, output, timeout: int = 10):
        """
        Initialize album downloader.

        Args:
            output: ConsoleOutput instance
            timeout: HTTP request timeout in seconds
        """
        self.output = output
        self.timeout = timeout

    def download(self, image_url: str, save_path: str) -> bool:
        """
        Download album artwork from URL and save to file.

        Args:
            image_url: URL of the album artwork image
            save_path: Local path to save the image

        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(image_url, timeout=self.timeout)
            response.raise_for_status()

            try:
                img = Image.open(BytesIO(response.content))
                img.save(save_path)
                self.output.success(f"Album artwork saved to {save_path}")
                return True
            except Exception as e:
                self.output.error(f"Error: Failed to process image: {e}")
                return False

        except requests.exceptions.Timeout:
            self.output.error(
                "Error: Download timed out. Please check your internet connection."
            )
            return False
        except requests.exceptions.ConnectionError:
            self.output.error(
                "Error: Connection failed. Please check your internet connection."
            )
            return False
        except requests.exceptions.RequestException as e:
            self.output.error(f"Error: Failed to download album artwork: {e}")
            return False


class FilenameUtil:
    """Utility for filename operations."""

    @staticmethod
    def sanitize(filename: str) -> str:
        """
        Sanitize a filename by replacing invalid characters.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename safe for filesystem
        """
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    @staticmethod
    def ensure_directory(directory: str, output) -> bool:
        """
        Ensure directory exists, creating if necessary.

        Args:
            directory: Directory path
            output: ConsoleOutput instance

        Returns:
            True if directory exists or was created, False on error
        """
        if os.path.exists(directory):
            return True

        try:
            os.makedirs(directory)
            output.info(f"Created directory: {directory}")
            return True
        except OSError as e:
            output.error(
                f"Error: Unable to create directory {directory}: {e}"
            )
            return False
