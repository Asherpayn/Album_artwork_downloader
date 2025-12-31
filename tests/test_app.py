"""Tests for main application."""
import unittest
from unittest.mock import Mock, patch
from app import AlbumArtworkApp


class TestAlbumArtworkApp(unittest.TestCase):
    """Test cases for AlbumArtworkApp class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_output = Mock()
        self.mock_credentials = Mock()
        self.mock_spotify = Mock()
        self.mock_selector = Mock()
        self.mock_downloader = Mock()

        self.app = AlbumArtworkApp(
            output=self.mock_output,
            credentials_manager=self.mock_credentials,
            spotify_client=self.mock_spotify,
            album_selector=self.mock_selector,
            album_downloader=self.mock_downloader,
            artworks_dir="/tmp/test_artworks"
        )

    def test_initialization_with_provided_dependencies(self):
        """Test initialization with all dependencies provided."""
        self.assertEqual(self.app.spotify_client, self.mock_spotify)
        self.assertEqual(self.app.album_selector, self.mock_selector)
        self.assertEqual(self.app.album_downloader, self.mock_downloader)

    @patch('app.SpotifyClient')
    def test_initialization_creates_spotify_client(self, mock_client_class):
        """Test initialization creates Spotify client when not provided."""
        self.mock_credentials.get_or_prompt.return_value = ("id", "secret")

        mock_client = Mock()
        mock_client.test_credentials.return_value = True
        mock_client_class.return_value = mock_client

        app = AlbumArtworkApp(
            output=self.mock_output,
            credentials_manager=self.mock_credentials
        )

        mock_client_class.assert_called_once_with("id", "secret")
        mock_client.test_credentials.assert_called_once()

    @patch('app.SpotifyClient')
    def test_initialization_fails_with_invalid_credentials(self, mock_client_class):
        """Test initialization raises ValueError with invalid credentials."""
        self.mock_credentials.get_or_prompt.return_value = ("id", "secret")

        mock_client = Mock()
        mock_client.test_credentials.return_value = False
        mock_client_class.return_value = mock_client

        with self.assertRaises(ValueError):
            app = AlbumArtworkApp(
                output=self.mock_output,
                credentials_manager=self.mock_credentials
            )

    def test_find_and_select_album(self):
        """Test finding and selecting an album."""
        mock_albums = [{'name': 'Test Album'}]
        self.mock_spotify.search_albums.return_value = mock_albums
        self.mock_selector.choose_from_list.return_value = mock_albums[0]

        result = self.app.find_and_select_album("test query")

        self.assertEqual(result, mock_albums[0])
        self.mock_spotify.search_albums.assert_called_once_with(
            "test query",
            limit=10
        )

    def test_download_album_artwork_success(self):
        """Test successful album artwork download."""
        album = {'name': 'Test Album', 'artists': [{'name': 'Test Artist'}]}
        self.mock_spotify.get_album_image_url.return_value = "https://example.com/image.jpg"
        self.mock_spotify.get_artist_name.return_value = "Test Artist"
        self.mock_downloader.download.return_value = True

        result = self.app.download_album_artwork(album)

        self.assertTrue(result)
        self.mock_downloader.download.assert_called_once()

    def test_download_album_artwork_no_image(self):
        """Test download when no image is available."""
        album = {'name': 'Test Album'}
        self.mock_spotify.get_album_image_url.return_value = None

        result = self.app.download_album_artwork(album)

        self.assertFalse(result)
        self.mock_output.info.assert_called_with("No album artwork found.")

    @patch('app.FilenameUtil.ensure_directory')
    def test_run_exits_on_exit_command(self, mock_ensure_dir):
        """Test that run exits when user types 'exit'."""
        mock_ensure_dir.return_value = True
        self.mock_output.prompt.return_value = "exit"

        self.app.run()

        self.mock_output.info.assert_any_call("Exiting the program.")

    @patch('app.FilenameUtil.ensure_directory')
    def test_run_handles_empty_input(self, mock_ensure_dir):
        """Test that run handles empty input gracefully."""
        mock_ensure_dir.return_value = True
        self.mock_output.prompt.side_effect = ["", "exit"]

        self.app.run()

        self.mock_output.info.assert_any_call("Please enter a valid album name.")

    @patch('app.FilenameUtil.ensure_directory')
    def test_run_returns_if_directory_creation_fails(self, mock_ensure_dir):
        """Test that run returns if directory cannot be created."""
        mock_ensure_dir.return_value = False

        self.app.run()

        # Should not prompt for album name
        self.mock_output.prompt.assert_not_called()

    @patch('app.FilenameUtil.ensure_directory')
    def test_run_handles_album_not_found(self, mock_ensure_dir):
        """Test handling when album is not found."""
        mock_ensure_dir.return_value = True
        self.mock_output.prompt.side_effect = ["test album", "exit"]
        self.mock_spotify.search_albums.return_value = []
        self.mock_selector.choose_from_list.return_value = None

        self.app.run()

        self.mock_output.info.assert_any_call("No matching album found.")


if __name__ == '__main__':
    unittest.main()
