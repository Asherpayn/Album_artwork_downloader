"""Tests for Spotify client."""
import unittest
from unittest.mock import Mock, patch
import spotipy
from spotify_client import SpotifyClient


class TestSpotifyClient(unittest.TestCase):
    """Test cases for SpotifyClient class."""

    def setUp(self):
        """Set up test fixtures with mocked Spotify."""
        with patch('spotify_client.spotipy.Spotify'):
            self.client = SpotifyClient("test_id", "test_secret")

    @patch('spotify_client.SpotifyClientCredentials')
    @patch('spotify_client.spotipy.Spotify')
    def test_initialization_creates_spotify_instance(self, mock_spotify, mock_auth):
        """Test that initialization creates Spotify client with credentials."""
        client = SpotifyClient("id", "secret")
        mock_auth.assert_called_once_with(
            client_id="id",
            client_secret="secret"
        )
        mock_spotify.assert_called_once()

    def test_test_credentials_returns_true_on_success(self):
        """Test that valid credentials return True."""
        self.client.sp = Mock()
        self.client.sp.search.return_value = {}
        self.assertTrue(self.client.test_credentials())

    def test_test_credentials_returns_false_on_exception(self):
        """Test that invalid credentials return False."""
        self.client.sp = Mock()
        self.client.sp.search.side_effect = spotipy.exceptions.SpotifyException(
            400, "msg", {}
        )
        self.assertFalse(self.client.test_credentials())

    def test_search_albums_returns_items(self):
        """Test that search returns album items."""
        mock_results = {
            'albums': {
                'items': [
                    {'name': 'Album 1'},
                    {'name': 'Album 2'}
                ]
            }
        }
        self.client.sp = Mock()
        self.client.sp.search.return_value = mock_results

        albums = self.client.search_albums("test query")
        self.assertEqual(len(albums), 2)
        self.assertEqual(albums[0]['name'], 'Album 1')
        self.client.sp.search.assert_called_once_with(
            q="test query",
            type='album',
            limit=10
        )

    def test_search_albums_with_custom_limit(self):
        """Test search with custom result limit."""
        mock_results = {'albums': {'items': []}}
        self.client.sp = Mock()
        self.client.sp.search.return_value = mock_results

        self.client.search_albums("test", limit=5)
        self.client.sp.search.assert_called_once_with(
            q="test",
            type='album',
            limit=5
        )

    def test_get_album_image_url_returns_first_image(self):
        """Test that first image URL is returned."""
        album = {
            'images': [
                {'url': 'https://example.com/large.jpg'},
                {'url': 'https://example.com/small.jpg'}
            ]
        }
        url = SpotifyClient.get_album_image_url(album)
        self.assertEqual(url, 'https://example.com/large.jpg')

    def test_get_album_image_url_returns_none_for_no_images(self):
        """Test that None is returned when no images available."""
        self.assertIsNone(SpotifyClient.get_album_image_url(None))
        self.assertIsNone(SpotifyClient.get_album_image_url({}))
        self.assertIsNone(SpotifyClient.get_album_image_url({'images': []}))

    def test_get_artist_name_returns_first_artist(self):
        """Test that first artist name is returned."""
        album = {
            'artists': [
                {'name': 'Artist 1'},
                {'name': 'Artist 2'}
            ]
        }
        name = SpotifyClient.get_artist_name(album)
        self.assertEqual(name, 'Artist 1')

    def test_get_artist_name_returns_unknown_for_missing(self):
        """Test that 'Unknown Artist' is returned for missing artists."""
        self.assertEqual(
            SpotifyClient.get_artist_name(None),
            "Unknown Artist"
        )
        self.assertEqual(
            SpotifyClient.get_artist_name({}),
            "Unknown Artist"
        )
        self.assertEqual(
            SpotifyClient.get_artist_name({'artists': []}),
            "Unknown Artist"
        )

    def test_get_artist_name_with_single_artist(self):
        """Test getting artist name with single artist."""
        album = {'artists': [{'name': 'Solo Artist'}]}
        self.assertEqual(SpotifyClient.get_artist_name(album), 'Solo Artist')


if __name__ == '__main__':
    unittest.main()
