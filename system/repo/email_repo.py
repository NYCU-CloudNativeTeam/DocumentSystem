import time
import os
import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app
from model.NotificationModel import Notification

class NotificationStrategy(ABC):
    """Using strategy pattern to support multiple notificiation service.
    """
    @abstractmethod
    def send(self, notification: Notification):
        raise NotImplementedError("Missing defined send function")


class EmailRepo(NotificationStrategy):
    def __init__(
        self,
    ):
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASS")
        self.sender_email_host = os.getenv("EMAIL_HOST")
        self.sender_email_port = os.getenv("EMAIL_PORT")

    def send(
        self,
        recipient,
        title,
        content
    ):
        # Create the MIMEMultipart object for the email
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = title

        # Attach the email body
        msg.attach(MIMEText(content, 'plain'))

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(self.sender_email_host, self.sender_email_port)
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(self.sender_email, self.sender_password)

            # Send the email
            server.sendmail(self.sender_email, recipient, msg.as_string())

            # Close the connection
            server.quit()
            current_app.logger.info("Email sent successfully.")
        except Exception as e:
            current_app.logger.info(f"Failed to send email. Error: {e}")
