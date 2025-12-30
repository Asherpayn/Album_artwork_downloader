"""Spotify API client wrapper."""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Optional, List, Dict, Any


class SpotifyClient:
    """Wrapper for Spotify API operations."""

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize Spotify client with credentials.

        Args:
            client_id: Spotify client ID
            client_secret: Spotify client secret
        """
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def test_credentials(self) -> bool:
        """
        Test if credentials are valid by making a simple search.

        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            self.sp.search(q="test", type="album", limit=1)
            return True
        except spotipy.exceptions.SpotifyException:
            return False

    def search_albums(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for albums matching the query.

        Args:
            query: Album name to search for
            limit: Maximum number of results (default: 10)

        Returns:
            List of album dictionaries from Spotify API
        """
        results = self.sp.search(q=query, type='album', limit=limit)
        return results['albums']['items']

    @staticmethod
    def get_album_image_url(album: Dict[str, Any]) -> Optional[str]:
        """
        Extract the largest image URL from an album.

        Args:
            album: Album dictionary from Spotify API

        Returns:
            Image URL if available, None otherwise
        """
        if not album or not album.get('images'):
            return None
        return album['images'][0]['url']

    @staticmethod
    def get_artist_name(album: Dict[str, Any]) -> str:
        """
        Extract the primary artist name from an album.

        Args:
            album: Album dictionary from Spotify API

        Returns:
            Artist name or "Unknown Artist" if not available
        """
        if album and album.get('artists') and len(album['artists']) > 0:
            return album['artists'][0]['name']
        return "Unknown Artist"
