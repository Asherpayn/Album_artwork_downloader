"""Tests for configuration and credentials management."""
import json
import os
import tempfile
import unittest
from unittest.mock import Mock
from config import CredentialsManager, CREDENTIALS_FILE


class TestCredentialsManager(unittest.TestCase):
    """Test cases for CredentialsManager class."""

    def setUp(self):
        """Set up test fixtures with temporary file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_file.close()
        self.manager = CredentialsManager(self.temp_file.name)
        self.mock_output = Mock()

    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_save_valid_credentials(self):
        """Test saving valid credentials to file."""
        result = self.manager.save("test_id", "test_secret")
        self.assertTrue(result)

        with open(self.temp_file.name, 'r') as f:
            data = json.load(f)
        self.assertEqual(data["client_id"], "test_id")
        self.assertEqual(data["client_secret"], "test_secret")

    def test_save_empty_client_id_returns_false(self):
        """Test that empty client ID returns False."""
        self.assertFalse(self.manager.save("", "secret"))

    def test_save_empty_client_secret_returns_false(self):
        """Test that empty client secret returns False."""
        self.assertFalse(self.manager.save("id", ""))

    def test_save_both_empty_returns_false(self):
        """Test that both empty returns False."""
        self.assertFalse(self.manager.save("", ""))

    def test_load_existing_credentials(self):
        """Test loading existing credentials from file."""
        self.manager.save("test_id", "test_secret")
        creds = self.manager.load()
        self.assertEqual(creds["client_id"], "test_id")
        self.assertEqual(creds["client_secret"], "test_secret")

    def test_load_nonexistent_file(self):
        """Test loading from non-existent file returns None."""
        os.unlink(self.temp_file.name)
        self.assertIsNone(self.manager.load())

    def test_load_corrupted_file(self):
        """Test loading corrupted JSON file returns None."""
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json{")
        self.assertIsNone(self.manager.load())

    def test_load_empty_file(self):
        """Test loading empty file returns None."""
        with open(self.temp_file.name, 'w') as f:
            f.write("")
        self.assertIsNone(self.manager.load())

    def test_get_or_prompt_uses_saved(self):
        """Test get_or_prompt returns saved credentials."""
        self.manager.save("saved_id", "saved_secret")
        client_id, client_secret = self.manager.get_or_prompt(self.mock_output)
        self.assertEqual(client_id, "saved_id")
        self.assertEqual(client_secret, "saved_secret")
        self.mock_output.info.assert_called_once_with("Using saved Spotify credentials.")

    def test_get_or_prompt_prompts_when_no_saved(self):
        """Test get_or_prompt asks for credentials when none saved."""
        os.unlink(self.temp_file.name)

        mock_prompt_responses = ["new_id", "new_secret"]
        self.mock_output.prompt = Mock(side_effect=mock_prompt_responses)

        client_id, client_secret = self.manager.get_or_prompt(self.mock_output)

        self.assertEqual(client_id, "new_id")
        self.assertEqual(client_secret, "new_secret")
        self.assertEqual(self.mock_output.prompt.call_count, 2)

    def test_get_or_prompt_retries_on_empty_credentials(self):
        """Test get_or_prompt retries when user provides empty credentials."""
        os.unlink(self.temp_file.name)

        # First attempt: empty credentials, second attempt: valid
        mock_prompt_responses = ["", "", "valid_id", "valid_secret"]
        self.mock_output.prompt = Mock(side_effect=mock_prompt_responses)

        client_id, client_secret = self.manager.get_or_prompt(self.mock_output)

        self.assertEqual(client_id, "valid_id")
        self.assertEqual(client_secret, "valid_secret")
        self.mock_output.error.assert_called_once()

    def test_credentials_file_default_location(self):
        """Test that default credentials file is in user home."""
        manager = CredentialsManager()
        self.assertTrue(manager.credentials_file.startswith(os.path.expanduser("~")))
        self.assertTrue(manager.credentials_file.endswith(".spotify_credentials.json"))


if __name__ == '__main__':
    unittest.main()
