import json

import redis

from model.NotificationModel import Notification


class RedisRepo:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def publish(self, notification: Notification):
        """Publish a notification to the appropriate Redis channel based on notification_type."""
        channel = notification.notification_type
        message = json.dumps(notification.to_dict())
        self.redis.publish(channel, message)

    def subscribe(self, notification_type: str):
        """Subscribe to a specific notification type and consume messages."""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(notification_type)
        return pubsub