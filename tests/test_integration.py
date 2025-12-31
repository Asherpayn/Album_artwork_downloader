"""Integration tests for the full application."""
import os
import tempfile
import unittest
from unittest.mock import Mock, patch
from app import AlbumArtworkApp
from config import CredentialsManager
from output import ConsoleOutput


class TestFullIntegration(unittest.TestCase):
    """Test complete workflows without real API calls."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_creds = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_creds.close()

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_creds.name):
            os.unlink(self.temp_creds.name)
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)

    @patch('app.SpotifyClient')
    @patch('app.AlbumSelector')
    def test_complete_workflow_success(self, mock_selector_class, mock_spotify_class):
        """Test complete workflow from search to download."""
        # Setup mocks
        mock_spotify = Mock()
        mock_spotify.test_credentials.return_value = True
        test_album = {
            'name': 'Test Album',
            'artists': [{'name': 'Test Artist'}],
            'images': [{'url': 'https://example.com/image.jpg'}]
        }
        mock_spotify.search_albums.return_value = [test_album]
        mock_spotify.get_artist_name.return_value = "Test Artist"
        mock_spotify.get_album_image_url.return_value = "https://example.com/image.jpg"
        mock_spotify_class.return_value = mock_spotify

        # Mock selector to return first album automatically
        mock_selector = Mock()
        mock_selector.choose_from_list.return_value = test_album
        mock_selector_class.return_value = mock_selector

        output = ConsoleOutput()
        creds_manager = CredentialsManager(self.temp_creds.name)
        creds_manager.save("test_id", "test_secret")

        # Create app
        app = AlbumArtworkApp(
            output=output,
            credentials_manager=creds_manager,
            artworks_dir=self.temp_dir
        )

        # Test album search and selection
        album = app.find_and_select_album("Test Album")
        self.assertIsNotNone(album)
        self.assertEqual(album['name'], 'Test Album')

    @patch('app.SpotifyClient')
    def test_app_initialization_with_saved_credentials(self, mock_spotify_class):
        """Test that app can initialize with saved credentials."""
        mock_spotify = Mock()
        mock_spotify.test_credentials.return_value = True
        mock_spotify_class.return_value = mock_spotify

        output = ConsoleOutput()
        creds_manager = CredentialsManager(self.temp_creds.name)
        creds_manager.save("saved_id", "saved_secret")

        # Should not raise any exceptions
        app = AlbumArtworkApp(
            output=output,
            credentials_manager=creds_manager,
            artworks_dir=self.temp_dir
        )

        self.assertIsNotNone(app.spotify_client)

    def test_credentials_manager_integration(self):
        """Test credentials manager saves and loads correctly."""
        creds_manager = CredentialsManager(self.temp_creds.name)

        # Save credentials
        result = creds_manager.save("client_id_123", "secret_456")
        self.assertTrue(result)

        # Load credentials
        loaded = creds_manager.load()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded['client_id'], "client_id_123")
        self.assertEqual(loaded['client_secret'], "secret_456")


if __name__ == '__main__':
    unittest.main()
