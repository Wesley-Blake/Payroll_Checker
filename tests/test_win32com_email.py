import pytest
from unittest.mock import patch, MagicMock
from helpers.win32com_email import email


class TestWin32ComEmail:
    """Test cases for email function"""

    @patch('win32com.client.Dispatch')
    @patch('builtins.open')
    def test_email_success(self, mock_open, mock_dispatch):
        """Test successful email sending"""
        # Mock the file read
        mock_file = MagicMock()
        mock_file.readline.return_value = 'attachment_path\n'
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock Outlook
        mock_outlook = MagicMock()
        mock_mail = MagicMock()
        mock_outlook.CreateItem.return_value = mock_mail
        mock_dispatch.return_value = mock_outlook

        # Mock attachment exists
        with patch('pathlib.Path.is_file', return_value=True):
            email("cc@example.com", ["bcc1@example.com"], "202401", "Test body")

        # Assertions
        mock_dispatch.assert_called_with('outlook.application')
        mock_outlook.CreateItem.assert_called_with(0)
        assert mock_mail.CC == "cc@example.com"
        assert mock_mail.BCC == "bcc1@example.com"
        assert mock_mail.Subject == "Pay Period: BW202401"
        mock_mail.Attachments.Add.assert_called_with('attachment_path')
        assert mock_mail.Body == "Test body"
        mock_mail.Send.assert_called_once()

    @patch('win32com.client.Dispatch')
    def test_email_outlook_failure(self, mock_dispatch):
        """Test failure to create Outlook application"""
        mock_dispatch.side_effect = Exception("Outlook error")

        with pytest.raises(SystemExit, match="Failed to create Outlook application: Outlook error"):
            email("cc@example.com", ["bcc1@example.com"], "202401", "Test body")