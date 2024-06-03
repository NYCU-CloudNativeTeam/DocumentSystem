import json
import threading
import logging
import os
from typing import Dict, Union

import pika
from flask import current_app

class RabbitMQPubliser():
    def __init__(
        self,
    ):
        """
        Initializes the RabbitMQPublisher with the host and port.
        """
        self.host = os.getenv("RABBITMQ_HOST")
        self.port = 5672

    def create_connection(self) -> pika.BlockingConnection:
        """Creates a connection to the RabbitMQ server.

        Returns:
            BlockingConnection: A connection to the RabbitMQ server.
        """
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = self.host, 
                    port = self.port, 
                )
            )
        except Exception as e:
            current_app.logger.error(f"Failed to create connection: {e}")
            raise

    def create_queue(
        self, 
        queue_name: str
    ):
        """Creates a queue on the RabbitMQ server.

        Args:
            queue_name: The name of the queue to be created.
        """
        try:
            with self.create_connection() as connection:
                channel = connection.channel()
                channel.queue_declare(queue=queue_name)
        except Exception as e:
            current_app.logger.error(f"Failed to create queue '{queue_name}': {e}")
            raise

    def send_message_to_queue(
        self, 
        queue_name: str, 
        message: Union[Dict, str]
    ):
        """Sends a message to a specified queue on the RabbitMQ server.

        Args:
            queue_name: The name of the queue to send the message to.
            message: The message to be sent.
        """
        try:
            with self.create_connection() as connection:
                channel = connection.channel()
                channel.queue_declare(queue=queue_name)
                # Serialize the message to JSON if it's a dict
                message_json = json.dumps(message) if isinstance(message, dict) else message
                channel.basic_publish(exchange='', routing_key=queue_name, body=message_json)
        except Exception as e:
            current_app.logger.error(f"Failed to send message to queue '{queue_name}': {e}")
            raise

    def delete_queue(
        self, 
        queue_name: str
    ):
        """Deletes a queue from the RabbitMQ server.

        Args:
            queue_name (str): The name of the queue to be deleted.
        """
        try:
            with self.create_connection() as connection:
                channel = connection.channel()
                channel.queue_declare(queue=queue_name)
                channel.queue_delete(queue=queue_name)
        except Exception as e:
            current_app.logger.error(f"Failed to delete queue '{queue_name}': {e}")
            raise