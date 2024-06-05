import json
import os
from repo.email_repo import EmailRepo
from repo.rabbitmq_repo import RabbitMQPubliser
from model.NotificationModel import Notification

class NotificationService():
    def __init__(
        self, 
    ):
        # self.redis_repo = redis_repo
        self.email_repo = EmailRepo()
        self.strategies = {
            'email': self.email_repo,
            # for future dev
            # 'telegram': TelegramStrategy()
        }
        self.thirdy2queue = {
            'email': os.getenv("RABBITMQ_EMAIL_QUEUE")
        }
        self.rabbitmq_publisher = RabbitMQPubliser()

    def create_notifications(
        self, 
        title: str, 
        content: str, 
        recipient: str,
        notification_type
    ) -> Notification:
        # create and return Notificaiton Model
        return Notification(
            title = title,
            content = content,
            recipient = recipient,
            notification_type = notification_type
        )

    def send_notifications_to_thirdparty(
        self,
        notification: Notification
    ) -> None:
        # get notification mesage from RabbitMQ
        # and send it third-party

        # select repo base on notificiation type
        repo = self.strategies.get(notification.notification_type)
        if repo:
            try:
                repo.send(notification)
            except Exception as e:
                print(e)

    def publisher_to_queue(
        self,
        third_party: str,
        title: str, 
        content: str, 
        recipient: str,
    ):
        self.rabbitmq_publisher.send_message_to_queue(
            queue_name = self.thirdy2queue[third_party],
            message = {
                "title": title,
                "content": content,
                "recipient": recipient
            }
        )

    def listen_and_send_notifications(
        self, 
        notification_type: str
    ) -> None:
        """Listen to a Redis channel and send notifications using the appropriate strategy.
        """
        pubsub = self.redis_repo.subscribe(notification_type)
        repo = self.strategies.get(notification_type)

        if not repo:
            print(f"No strategy found for notification type: {notification_type}")
            return

        print(f"Listening for '{notification_type}' notifications")
        for message in pubsub.listen():
            if message['type'] == 'message':
                notification_data = json.loads(message['data'].decode('utf-8'))
                notification = Notification.from_dict(notification_data)
                repo.send(notification)
