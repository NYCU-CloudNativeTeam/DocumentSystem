import time
import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        sender_email: str, 
        sender_password: str,
        sender_email_host: str = 'smtp.gmail.com',
        sender_email_port: int = 587,
    ):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_email_host = sender_email_host
        self.sender_email_port = sender_email_port

    def send(
        self,
        notification: Notification
    ):
        recipient = notification.recipient
        title = notification.title
        content = notification.content
    
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
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")