import json
from datetime import datetime
from typing import Optional


class Notification:
    def __init__(
        self, 
        title: str,
        content: str,
        recipient: str = '',
        notification_type: str = '', 
        timestamp: Optional[datetime] = None
    ):
        self.title = title
        self.content = content
        self.recipient = recipient
        self.notification_type = notification_type
        self.timestamp = timestamp if timestamp else datetime.now()

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "recipient": self.recipient,
            "notification_type": self.notification_type,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            content=data['content'],
            recipient=data.get('recipient', ''),
            notification_type=data.get('notification_type', ''),
            timestamp=datetime.fromisoformat(data['timestamp'])
        )