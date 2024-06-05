# class RabbitMQConsumer(threading.Thread):
#     def __init__(
#         self,
#         host: str,
#         port: int,
#         queue_name: str,
#         callback = None,
#         logger: logging.Logger = None
#     ):
#         """Initializes the RabbitMQConsumer.

#         Args:
#             host (str): The RabbitMQ server host address.
#             port (int): The RabbitMQ server port number.
#             queue_name (str): The name of the queue to consume messages from.
#             callback (callable): A function to be called for each message received.
#         """
#         super(RabbitMQConsumer, self).__init__()
#         self.host = host
#         self.port = port
#         self.stop_consume = False
#         self.queue_name = queue_name
#         self.callback = callback

#         # if not specify loggger, create it
#         self.logger = logger or logging.getLogger(__name__)

#     def create_connection(self) -> pika.BlockingConnection:
#         """Creates a connection to the RabbitMQ server.

#         Returns:
#             pika.BlockingConnection: A connection to the RabbitMQ server.
#         """
#         try:
#             return pika.BlockingConnection(
#                 pika.ConnectionParameters(
#                     host = self.host, 
#                     port = self.port, 
#                 )
#             )
#         except Exception as e:
#             self.logger.error(f"Failed to create connection: {e}")
#             raise

#     def stop(self):
#         """Stops consuming messages from the queue."""
#         self.stop_consume = True

#     def run(self):
#         """Starts consuming messages from the queue."""
#         try:
#             with self.create_connection() as connection:
#                 channel = connection.channel()
#                 for message in channel.consume(
#                     queue=self.queue_name, 
#                     auto_ack=True, 
#                     inactivity_timeout=1
#                 ):
#                     if self.stop_consume:
#                         break
#                     if message is None:
#                         continue
#                     method_frame, properties, body = message
#                     if body:
#                         self.handle_message(body.decode())
#         except Exception as e:
#             self.logger.error(f"Consumer error: {e}")
#             raise 

#     def handle_message(self, body: str):
#         """Handles the processing of a message received from the queue.

#         Args:
#             body (str): The body of the message received from the queue.

#         Raises:
#             Exception: If an error occurs during message processing.

#         Returns:
#             None
#         """
#         try:
#             is_process_success = self.callback(body)
#             if is_process_success:
#                 self.logger.info('Message processing succeeded')
#             else:
#                 self.logger.warning('Message processing failed to prevent starvation')
#         except Exception as e:
#             self.logger.error(f"Failed to process message: {e}")
#             raise


import json
import pika
import logging
import os
from repo.email_repo import EmailRepo
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
class NotificationService:
    def __init__(self):
        load_dotenv()
        self.email_repo = EmailRepo()
        self.host = os.getenv("RABBITMQ_HOST")
        self.email_queue = os.getenv("RABBITMQ_EMAIL_QUEUE")

    def start_consuming(self):
        logger.info("start consuming email notificaiton task")
        logger.info(f"consuming from host: {self.host}, queue: {self.email_queue}")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.email_queue)

        def callback(ch, method, properties, body):
            if body:
                try:
                    data = json.loads(body)
                    logger.info(f"Receive message: {data}")
                    self.email_repo.send(
                        recipient=data['recipient'],
                        title=data['title'],
                        content=data['content']
                    )
                except Exception as e:
                    logger.error("Error when send to email")
                    logger.error(e)

        channel.basic_consume(
            queue=self.email_queue, 
            on_message_callback=callback, 
            auto_ack=True
        )
        logger.info('Service started. Waiting for messages')
        channel.start_consuming()

if __name__ == '__main__':
    service = NotificationService()
    service.start_consuming()