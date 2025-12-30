"""Configuration and credentials management."""
import json
import os
from typing import Optional, Tuple

# Configuration constants
CREDENTIALS_FILE = os.path.expanduser("~/.spotify_credentials.json")
ALBUM_ARTWORKS_DIR = os.path.expanduser("~/Pictures/albumartworks")
SEARCH_LIMIT = 10
DOWNLOAD_TIMEOUT = 10


class CredentialsManager:
    """Manages Spotify API credentials with file persistence."""

    def __init__(self, credentials_file: str = CREDENTIALS_FILE):
        """
        Initialize credentials manager.

        Args:
            credentials_file: Path to credentials file (default: CREDENTIALS_FILE)
        """
        self.credentials_file = credentials_file

    def save(self, client_id: str, client_secret: str) -> bool:
        """
        Save Spotify API credentials to file.

        Args:
            client_id: Spotify client ID
            client_secret: Spotify client secret

        Returns:
            True if saved successfully, False otherwise
        """
        if not client_id or not client_secret:
            return False

        credentials = {"client_id": client_id, "client_secret": client_secret}
        try:
            with open(self.credentials_file, "w") as f:
                json.dump(credentials, f)
            return True
        except IOError:
            return False

    def load(self) -> Optional[dict]:
        """
        Load Spotify API credentials from file.

        Returns:
            Dictionary with 'client_id' and 'client_secret' if found,
            None if file doesn't exist or is corrupted
        """
        if not os.path.exists(self.credentials_file):
            return None

        try:
            with open(self.credentials_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def get_or_prompt(self, output, input_fn=input) -> Tuple[str, str]:
        """
        Get credentials from file or prompt user.

        Args:
            output: ConsoleOutput instance for messaging
            input_fn: Input function (for testing, default: built-in input)

        Returns:
            Tuple of (client_id, client_secret)
        """
        creds = self.load()
        if creds:
            output.info("Using saved Spotify credentials.")
            return creds["client_id"], creds["client_secret"]

        while True:
            client_id = output.prompt("Your Spotify Client ID: ").strip()
            client_secret = output.prompt("Your Spotify Client Secret: ").strip()

            if self.save(client_id, client_secret):
                return client_id, client_secret
            else:
                output.error("Error: Client ID and Client Secret cannot be empty.")
