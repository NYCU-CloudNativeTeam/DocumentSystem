import pytest
from unittest.mock import patch, MagicMock
from repo.email_repo import EmailRepo 

def test_email_send_failure():
    # Setup environment variables and recipient details
    recipient = "test@example.com"
    title = "Test Email"
    content = "This is a test email."
    
    with patch('repo.email_repo.os.getenv', side_effect=["sender@example.com", "password", "smtp.example.com", "587"]), \
         patch('repo.email_repo.smtplib.SMTP') as mock_smtp:
        # Mock the SMTP server to throw an exception on login
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("Login failed")
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Create EmailRepo instance
        email_repo = EmailRepo()

        # Call the send method
        try:
            email_repo.send(recipient, title, content)
            print("Test failed: Email should not be sent.")
        except Exception as e:
            print("Test passed: Caught an error during email sending.")

