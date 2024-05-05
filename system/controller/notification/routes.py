import os

from flask import Blueprint, jsonify, current_app, request

from .schema import MessageSchema
from ..util import validate_json
from service.NotificationService import NotificationService
from repo.RedisRepo import RedisRepo
from repo.EmailRepo import EmailRepo

# define auth as blueprint name
notify = Blueprint('notify', __name__)

@notify.route('/send_notification', methods=['POST'])
@validate_json(MessageSchema)
def send_notification(validated_data):
    """The API to send message by third-party base on you specify.

    Args:
        The request body defines the following fields:
        - recipient (str, required): The email or phone number of the message recipient.
        - title (str, required): The subject or title of the message.
        - content (str, required): The body or main content of the message.
        - notification_type (str, optional): The type of notification, which defaults to "email".

    Example:
        curl -X POST http://127.0.0.1:5000/api/notify/send_notification \
            --header "Content-Type: application/json" \
            --data '{"recipient":"<EMAIL>", "title":"test", "content":"hi", "notification_type": "email"}'
    """
    current_app.logger.info(validated_data)

    # get user name and message
    recipient = validated_data['recipient']
    title = validated_data['title']
    content = validated_data['content']
    notification_type = validated_data['notification_type']

    # get redis info
    redis_host = current_app.config["REDIS_HOST"],
    redis_port = current_app.config["REDIS_PORT"]

    # get email info from .env
    email_sender = os.getenv('EMAIL_SENDER')
    email_passwd = os.getenv('EMAIL_PASS')
    email_host = os.getenv('EMAIL_HOST')
    email_port = os.getenv('EMAIL_PORT')

    current_app.logger.info(
        f"Send notification to {recipient} by {notification_type} third-part "
        f"with title: {title} and message: {content}"
    )

    email_repo = EmailRepo(
        sender_email = email_sender,
        sender_password = email_passwd,
        sender_email_host = email_host,
        sender_email_port = email_port
    )

    redis_repo = RedisRepo(
        host = redis_host,
        port = redis_port
    )

    # create notify service instance
    notification_service = NotificationService(
        redis_repo = redis_repo,
        email_repo = email_repo
    )

    try:
        notification= notification_service.create_notifications(
            title = title,
            content = content,
            recipient = recipient,
            notification_type = notification_type
        )
        notification_service.send_notifications(notification)
    except Exception as e:
        current_app.logger.error("Send notification failed")
        current_app.logger.error(e)
        return jsonify({"error": "Send notification failed"}), 500

    current_app.logger.info("Send notification successfully")
    return jsonify({"message": "Send notification successfully"}), 200