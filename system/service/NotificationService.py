from repo.EmailRepo import EmailRepo
from repo.RedisRepo import RedisRepo
from model.NotificationModel import Notification

import json

class NotificationService():
    def __init__(
        self, 
        redis_repo: RedisRepo,
        email_repo: EmailRepo,
    ):
        self.redis_repo = redis_repo
        self.email_repo = email_repo
        self.strategies = {
            'email': email_repo,
            # for future dev
            # 'telegram': TelegramStrategy()
        }

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

    def send_notifications(
        self, 
        notification: Notification
    ) -> None:
        # select repo base on notificiation type
        repo = self.strategies.get(notification.notification_type)
        if repo:
            try:
                repo.send(notification)
            except Exception as e:
                print(e)

    def get_notifications(
        self
    ):
        """Get notification from Redis.
        Since we maybe support multiple notification service,
        and we can save each type notification of each service in different
        channel of Redis service.
        """
        pass

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
