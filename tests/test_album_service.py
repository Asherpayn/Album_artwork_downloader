"""Tests for album services."""
import os
import tempfile
import unittest
from unittest.mock import Mock, patch
from album_service import AlbumSelector, AlbumDownloader, FilenameUtil


class TestAlbumSelector(unittest.TestCase):
    """Test cases for AlbumSelector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_output = Mock()
        self.selector = AlbumSelector(self.mock_output)
        self.get_artist_name = lambda album: album.get('artist', 'Unknown')

    def test_choose_from_empty_list_returns_none(self):
        """Test that empty list returns None."""
        result = self.selector.choose_from_list([], self.get_artist_name)
        self.assertIsNone(result)

    def test_choose_valid_selection(self):
        """Test valid album selection."""
        albums = [
            {'name': 'Album 1', 'artist': 'Artist 1'},
            {'name': 'Album 2', 'artist': 'Artist 2'}
        ]
        self.mock_output.prompt = Mock(return_value="2")

        result = self.selector.choose_from_list(albums, self.get_artist_name)
        self.assertEqual(result['name'], 'Album 2')

    def test_choose_invalid_selection_defaults_to_first(self):
        """Test invalid input defaults to first album."""
        albums = [
            {'name': 'Album 1', 'artist': 'Artist 1'},
            {'name': 'Album 2', 'artist': 'Artist 2'}
        ]
        self.mock_output.prompt = Mock(return_value="invalid")

        result = self.selector.choose_from_list(albums, self.get_artist_name)
        self.assertEqual(result['name'], 'Album 1')

    def test_choose_out_of_range_defaults_to_first(self):
        """Test out of range selection defaults to first."""
        albums = [{'name': 'Album 1', 'artist': 'Artist 1'}]
        self.mock_output.prompt = Mock(return_value="99")

        result = self.selector.choose_from_list(albums, self.get_artist_name)
        self.assertEqual(result['name'], 'Album 1')

    def test_choose_first_album(self):
        """Test selecting first album."""
        albums = [{'name': 'Album 1', 'artist': 'Artist 1'}]
        self.mock_output.prompt = Mock(return_value="1")

        result = self.selector.choose_from_list(albums, self.get_artist_name)
        self.assertEqual(result['name'], 'Album 1')


class TestAlbumDownloader(unittest.TestCase):
    """Test cases for AlbumDownloader class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_output = Mock()
        self.downloader = AlbumDownloader(self.mock_output, timeout=5)
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        self.temp_file.close()

    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    @patch('album_service.requests.get')
    @patch('album_service.Image.open')
    def test_download_success(self, mock_image_open, mock_get):
        """Test successful download."""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.content = b'fake image data'
        mock_get.return_value = mock_response

        # Mock PIL Image
        mock_img = Mock()
        mock_image_open.return_value = mock_img

        result = self.downloader.download(
            "https://example.com/image.jpg",
            self.temp_file.name
        )

        self.assertTrue(result)
        mock_get.assert_called_once_with(
            "https://example.com/image.jpg",
            timeout=5
        )
        mock_img.save.assert_called_once_with(self.temp_file.name)

    @patch('album_service.requests.get')
    def test_download_timeout(self, mock_get):
        """Test download timeout handling."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()

        result = self.downloader.download(
            "https://example.com/image.jpg",
            self.temp_file.name
        )

        self.assertFalse(result)
        self.mock_output.error.assert_called_once()
        self.assertIn("timed out", self.mock_output.error.call_args[0][0])

    @patch('album_service.requests.get')
    def test_download_connection_error(self, mock_get):
        """Test connection error handling."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()

        result = self.downloader.download(
            "https://example.com/image.jpg",
            self.temp_file.name
        )

        self.assertFalse(result)
        self.assertIn("Connection failed", self.mock_output.error.call_args[0][0])

    @patch('album_service.requests.get')
    @patch('album_service.Image.open')
    def test_download_image_processing_error(self, mock_image_open, mock_get):
        """Test image processing error handling."""
        mock_response = Mock()
        mock_response.content = b'invalid image data'
        mock_get.return_value = mock_response
        mock_image_open.side_effect = Exception("Invalid image")

        result = self.downloader.download(
            "https://example.com/image.jpg",
            self.temp_file.name
        )

        self.assertFalse(result)
        self.assertIn("Failed to process image", self.mock_output.error.call_args[0][0])


class TestFilenameUtil(unittest.TestCase):
    """Test cases for FilenameUtil class."""

    def test_sanitize_removes_invalid_chars(self):
        """Test that invalid characters are removed."""
        dirty = 'album<>:"/\\|?*name'
        clean = FilenameUtil.sanitize(dirty)
        self.assertEqual(clean, 'album_________name')

    def test_sanitize_preserves_valid_chars(self):
        """Test that valid characters are preserved."""
        valid = 'Album Name - Artist (2023)'
        clean = FilenameUtil.sanitize(valid)
        self.assertEqual(clean, valid)

    def test_sanitize_handles_all_invalid_chars(self):
        """Test all invalid characters are handled."""
        for char in '<>:"/\\|?*':
            dirty = f'album{char}name'
            clean = FilenameUtil.sanitize(dirty)
            self.assertEqual(clean, 'album_name')

    def test_ensure_directory_creates_new(self):
        """Test creating new directory."""
        mock_output = Mock()
        temp_dir = tempfile.mkdtemp()
        new_dir = os.path.join(temp_dir, 'new_subdir')

        try:
            result = FilenameUtil.ensure_directory(new_dir, mock_output)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(new_dir))
            mock_output.info.assert_called_once()
        finally:
            if os.path.exists(new_dir):
                os.rmdir(new_dir)
            os.rmdir(temp_dir)

    def test_ensure_directory_existing_returns_true(self):
        """Test existing directory returns True."""
        mock_output = Mock()
        temp_dir = tempfile.mkdtemp()

        try:
            result = FilenameUtil.ensure_directory(temp_dir, mock_output)
            self.assertTrue(result)
            # Should not call info for existing directory
            mock_output.info.assert_not_called()
        finally:
            os.rmdir(temp_dir)

    def test_ensure_directory_handles_permission_error(self):
        """Test handling permission errors."""
        mock_output = Mock()

        with patch('album_service.os.makedirs') as mock_makedirs:
            mock_makedirs.side_effect = OSError("Permission denied")

            result = FilenameUtil.ensure_directory("/invalid/path", mock_output)

            self.assertFalse(result)
            mock_output.error.assert_called_once()


if __name__ == '__main__':
    unittest.main()
